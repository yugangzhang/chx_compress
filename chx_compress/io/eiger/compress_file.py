import h5py
import numpy as np
#import numba

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

def get_header(filename, dims):
    '''
        Make the BNL compressed version 1.0 format header.
    '''
    # dims : image dims
    # make the header from the EIGER file
    f = h5py.File(filename)
    # read in bytes
    # header is always from zero
    cur = 0
    header = b"Version-COMP0001"
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



#@numba.jit()
def compress_file(filename, dset_min=1, dset_max=50, dset_root="/entry/data",
                  dset_pref="data_", outfile="out.bin", version="v1.3.0"):

    # this is copied from default in order to allow to mutate the dict for
    # different version EIGER's
    EIGER_KEYS = EIGER_KEYS_DEFAULT.copy()

    # resolve the version number
    if version >= "v1.3.0":
        EIGER_KEYS['wavelength'] = EIGER_KEYS['wavelength_post1.3']
    else:
        EIGER_KEYS['wavelength'] = EIGER_KEYS['wavelength_pre1.3']

    f = h5py.File(filename)
    fout = open(outfile, "wb")

    # get data set shape and number images
    key = dset_root + "/" + dset_pref + "{:06d}".format(dset_min)
    dset = f[key]
    dims = dset.shape[1:]
    nimgs = dset.shape[0]
    f.close()



    arr = np.zeros(dims, dtype=np.uint16)

    # close and re-open file, get header
    header = get_header(filename, dims)
    fout.write(header)

    f = h5py.File(filename)

    for i in range(dset_min, dset_max+1):
        print("reading dataset {}".format(i))
        for j in range(nimgs):
            key = dset_root + "/" + dset_pref + "{:06d}".format(i)
            dset = f[key]
            dset.read_direct(arr, np.s_[j,:,:])

            #test = np.array(f[key][j])
            w, = np.where((arr.ravel() > 0)*(arr.ravel() < 65535))
            #print("found {} items".format(len(w[0])))
            fout.write(np.uint32(len(w)))
            fout.write(w.astype(np.uint32))
            fout.write(arr.ravel()[w])

    fout.close()
    f.close()
