import h5py
import numpy as np

import struct

EIGER_KEYS_DEFAULT = {
    # old version (less than v1.3.0)
    'wavelength_pre1.3' : "entry/instrument/monochromator/wavelength",
    # new version (greater than v1.3.0)
    'wavelength_post1.3' : "entry/instrument/beam/incident_wavelength",
    'beam_center_x' : "entry/instrument/detector/beam_center_x",
    'beam_center_y' : "entry/instrument/detector/beam_center_x",
    'count_time' : "entry/instrument/detector/count_time",
    'x_pixel_size' : "entry/instrument/detector/x_pixel_size",
    'y_pixel_size' : "entry/instrument/detector/y_pixel_size",
    'frame_time' : "entry/instrument/detector/frame_time",
}

def get_header(filename, dims, EIGER_KEYS):
    '''
        Make the BNL compressed version 1.0 format header.
    '''
    print("dims is  {}".format(dims))
    # dims : image dims
    # make the header from the EIGER file
    f = h5py.File(filename)
    # read in bytes
    # header is always from zero
    cur = 0
    # this is version 2
    header = b"Version-COMP0002"
    header += struct.pack("@d", f[EIGER_KEYS['beam_center_x']].value)
    header += struct.pack("@d", f[EIGER_KEYS['beam_center_y']].value)
    header += struct.pack("@d", f[EIGER_KEYS['count_time']].value)
    # detector_distance
    header += struct.pack("@d", 0)
    # frame time
    header += struct.pack("@d", f[EIGER_KEYS['frame_time']].value)
    # incident wavelength
    header += struct.pack("@d", f[EIGER_KEYS['wavelength']].value)
    header += struct.pack("@d", f[EIGER_KEYS['x_pixel_size']].value)
    header += struct.pack("@d", f[EIGER_KEYS['y_pixel_size']].value)
    # bytes, we choose 2 here
    header += struct.pack("@I", 2)
    # nrows
    header += struct.pack("@I", dims[0])
    # ncols
    header += struct.pack("@I", dims[1])
    # rows begin
    header += struct.pack("@I", 0)
    # rows end
    header += struct.pack("@I", dims[0])
    # cols begin
    header += struct.pack("@I", 0)
    # cols end
    header += struct.pack("@I", dims[1])

    f.close()
    header += struct.pack("@916x")
    return header



def compress_file(filename, outfile="out.bin", version="v1.3.0"):
    '''
        Compress an EIGER hdf5 file into a BNL Multifile compressed format.

        Parameters
        ----------
        filename : str
            The filename of the EIGER file
        outfile: str, optional
        version : str, optional
            The version string of the hdf5 file
            Currently, only major changes occurred from the change to 1.3.0
            So just make sure "new" files have a version number string
            according to this format greater than this number and vice versa
            for older files
    '''

    # this is copied from default in order to allow to mutate the dict for
    # different version EIGER's
    EIGER_KEYS = EIGER_KEYS_DEFAULT.copy()

    # the prefix of the data keys. Currently the same for all versions
    dset_pref="data_"

    # resolve the version number
    if version >= "v1.3.0":
        EIGER_KEYS['wavelength'] = EIGER_KEYS['wavelength_post1.3']
        dset_root="/entry/data"
    else:
        # this will be very unlikely
        EIGER_KEYS['wavelength'] = EIGER_KEYS['wavelength_pre1.3']
        dset_root="/entry"

    f = h5py.File(filename)
    fout = open(outfile, "wb")

    # get the range of data sets byt just inspecting the keys
    dset_keys = list(f[dset_root].keys())
    dset_keys = [dset_key for dset_key in dset_keys if dset_key.startswith(dset_pref) ]
    dset_keys.sort()

    # dset key validation (not necessarily needed)
    # verify numbers are all in ascending order. If one is out of sequence,
    # then there likely is an issue
    Nkeys = len(dset_keys)
    nums = np.array([int(dset_key[5:]) for dset_key in dset_keys])

    if not np.allclose(nums, np.arange(1, Nkeys+1)):
        msg = "Error, keys don't increase in ascending"
        msg += " order from 1 to {}".format(Nkeys)
        raise ValueError(msg)
    dset_min = 1
    dset_max = Nkeys+1

    # get data set shape and number images
    key = dset_root + "/" + dset_pref + "{:06d}".format(dset_min)
    dset = f[key]
    dims = dset.shape[1:]
    nimgs = dset.shape[0]
    f.close()

    arr = np.zeros(dims, dtype=np.uint16)

    # close and re-open file, get header
    header = get_header(filename, dims, EIGER_KEYS=EIGER_KEYS)
    fout.write(header)

    f = h5py.File(filename)

    for dset_key in dset_keys:
        print("reading dataset {}".format(dset_key))
        for j in range(nimgs):

            dset = f[dset_root + "/" + dset_key]
            # this is an important trick to ensure the reading is blazingly
            # fast. Doing this incorrectly can result in a significant
            # reduction in performance! At least a factor of 10!
            dset.read_direct(arr, np.s_[j,:,:])

            #test = np.array(f[key][j])
            # TODO : Here we should use our own conditions to test
            w, = np.where((arr.ravel() > 0)*(arr.ravel() < 65535))

            #print("found {} items".format(len(w[0])))
            fout.write(np.uint32(len(w)))
            fout.write(w.astype(np.uint32))
            fout.write(arr.ravel()[w])

    fout.close()
    f.close()
