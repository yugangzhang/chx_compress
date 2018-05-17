from chx_xpcs.io.eiger.compress_file import compress_file
import time
from chx_xpcs.io.eiger.compress_file2 import compress_file as compress_file2

filename = "/home/lhermitte/research/projects/xpcs-aps-chx-project/sample_data/bnl_data_yugang/647a2a04-bc5c-4dc9-8550_2511_master.h5".encode("utf-8")
dataset_prefix = "/entry/data/data_".encode("utf-8")
dataset_root = "/entry/data".encode("utf-8")
out_filename = "out_version1_large.bin".encode("utf-8")

print("begin compression")
t1 = time.time()
compress_file(filename, dataset_root, dataset_prefix, out_filename)
t2 = time.time()
print("end. took {} seconds".format(t2-t1))

print("begin compression version 2 (python API)")
t1 = time.time()
compress_file2(filename, dset_min=1, dset_max=50, dset_pref="data_",
               outfile="out_version2_large.bin")
t2 = time.time()
print("end. took {} seconds".format(t2-t1))

#filename = "../../sample_data/flow10crlT0_EGhtd_011_66/flow10crlT0_EGhtd_011_66_master.h5".encode("utf-8")
#dataset_prefix = "entry/data_".encode("utf-8")
#dataset_root = "/entry".encode("utf-8")
#out_filename = "out2.bin".encode("utf-8")
