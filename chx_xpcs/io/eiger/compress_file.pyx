cdef extern from "../../../src/_compress_file.c":
    int raw_compress_file(char * filename, char *dataset_root,
                          char * dataset_prefix, char * out_filename,
                          int threshold);

def compress_file(char * filename, char * dataset_root, char * dataset_prefix,
                  char * out_filename, int threshold=65535):
    raw_compress_file(bytes(filename), bytes(dataset_root), bytes(dataset_prefix),
                      bytes(out_filename), int(threshold));
