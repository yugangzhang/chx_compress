from chx_xpcs.io.eiger.compress_file import compress_file
import time
from chx_xpcs.io.eiger.compress_file2 import compress_file as compress_file2

filename = "../../sample_data/flow10crlT0_EGhtd_011_66/flow10crlT0_EGhtd_011_66_master.h5".encode("utf-8")
dataset_prefix = "entry/data_".encode("utf-8")
dataset_root = "/entry".encode("utf-8")
out_filename = "out_version1_small.bin".encode("utf-8")

print("begin compression")
t1 = time.time()
compress_file(filename, dataset_root, dataset_prefix, out_filename)
t2 = time.time()
print("end. took {} seconds".format(t2-t1))

print("begin compression version 2 (python API)")
t1 = time.time()
compress_file2(filename, dset_min=0, dset_max=9, dset_pref="data_",
               dset_root="/entry", outfile="out_version2_small.bin")
t2 = time.time()
print("end. took {} seconds".format(t2-t1))

