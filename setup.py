from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy as np
import os

HERE = os.path.dirname(__file__)
LIB_DIR = os.path.join(HERE, "lib")
INC_DIR = os.path.join(HERE, "include")

extensions = [
    Extension(
        "klu",
        ["klu.pyx", "klu_interf.c"],
        include_dirs=[np.get_include(), INC_DIR],
        libraries=[
            "klu",
            "btf",
            "amd",
            "colamd",
            "suitesparseconfig",
        ],
        library_dirs=[LIB_DIR],
        extra_link_args=[
            # Make dyld search ./lib relative to the .so at import time
            "-Wl,-rpath,@loader_path/lib",
        ],
    )
]

setup(
    ext_modules=cythonize(extensions),
)
