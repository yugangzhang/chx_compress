make compress:
	cythonize compress_file.pyx
	# PATH TO PYTHON LIBRARY
	h5cc -shared -o compress_file.so -I/home/lhermitte/miniconda3/envs/py3/include/python3.6m compress_file.c
