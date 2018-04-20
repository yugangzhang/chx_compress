#!/usr/bin/env python
import setuptools
from distutils.core import setup, Extension
import versioneer
import os
import sys
from Cython.Build import cythonize

# necessary deps (won't build if this isn't here)
import numpy as np



def cython_ext():
    #from distutils.sysconfig import get_python_inc
    #get_python_inc() #this gives the include dir
    libs = cythonize("**/*.pyx")
    for lib in libs:
        lib.language="h5cc"
    return libs

setuptools.setup(
    name='chx_xpcs',
    author='Yugang Zhang and Julien Lhermitte',
    packages=setuptools.find_packages(exclude=['doc']),
    include_dirs=[np.get_include()],
    # scripts for building external modules
    #ext_modules=cython_ext(),
    )

