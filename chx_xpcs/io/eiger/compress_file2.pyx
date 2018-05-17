cimport h5py
cimport numpy as np

def compress_file(filename, dset_min=1, dset_max=49, dset_pref="data_"):
    char *dset_root = "/entry/data"

    cdef np.uint_t [10000000] poss;
    cdef np.uint16_t [10000000] vals;
    cdef np.uint_t [2167, 2070] img;


def write_compress(
#    f = h5py.File(filename)
#    fout = open("test.out", "wb")
#
#    nimgs = 100
#    for i in range(dset_min, dset_max+1):
#        print("reading dataset {}".format(i))
#        for j in range(nimgs):
#            key = dset_root + "/" + dset_pref + "{:06d}".format(i)
#            dset = f[key]
#            dset.read_direct(arr, np.s_[0])
#            #test = np.array(f[key][j])
#            w = np.where(arr < 65535)
#            fout.write(w[0]*dims[1]+w[1])
#            fout.write(arr[w])
#
#    fout.close()
#    f.close()



#filename = "/home/lhermitte/research/projects/xpcs-aps-chx-project/sample_data/bnl_data_yugang/647a2a04-bc5c-4dc9-8550_2511_master.h5"

#compress_file(filename, dset_min=1, dset_max=49, dset_pref="data_")
