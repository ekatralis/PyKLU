from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy as np
import os

HERE = os.path.dirname(__file__)
SS_ROOT = os.path.join(HERE, "extern", "SuiteSparse")
LIB_DIR = os.path.join(SS_ROOT, "lib")
INC_DIR = os.path.join(SS_ROOT, "include", "suitesparse")

extensions = [
    Extension(
        "klu",
        ["klu.pyx", "klu_interf.c"],
        include_dirs=[
            np.get_include(),
            INC_DIR,
        ],
        libraries=[
            "klu",
            "btf",
            "amd",
            "colamd",
            "suitesparseconfig",
        ],
        library_dirs=[LIB_DIR],
        extra_link_args=[f"-Wl,-rpath,{LIB_DIR}"],  # <-- add this line
    )
]

setup(
    ext_modules=cythonize(extensions),
)
