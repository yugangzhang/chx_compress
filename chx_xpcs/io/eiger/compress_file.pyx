import numpy as np
cimport numpy as np

cdef extern from "../../../src/_compress_file.h":
    int raw_compress_file(char * filename, char *dataset_root,
                          char * dataset_prefix, char * out_filename);

def compress_file(char * filename, char * dataset_root, char * dataset_prefix,
                  char * out_filename):
    raw_compress_file(bytes(filename), bytes(dataset_root), bytes(dataset_prefix),
                      bytes(out_filename));
