from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize
import numpy as np
import pathlib
import subprocess
import sys
import os


ROOT = pathlib.Path(__file__).parent.resolve()
SS_ROOT = ROOT / "extern" / "SuiteSparse"
LIB_DIR = SS_ROOT / "lib"
INC_DIR = SS_ROOT / "include" / "suitesparse"


class BuildExtWithSuiteSparse(build_ext):
    """build_ext that first builds the SuiteSparse libraries via make."""

    def run(self):
        # 1) Build SuiteSparse libs (rough Python equivalent of your compile_klu script)
        suitesparse_components = [
            "KLU",
            "AMD",
            "BTF",
            "CHOLMOD",
            "COLAMD",
            "SuiteSparse_config",
        ]

        for comp in suitesparse_components:
            comp_dir = SS_ROOT / comp
            print(f"building SuiteSparse component: {comp} in {comp_dir}")
            subprocess.check_call(["make", "local"], cwd=str(comp_dir))
            subprocess.check_call(["make", "install"], cwd=str(comp_dir))

        # 2) let setuptools build the Cython extension
        super().run()


def make_extensions():
    ext = Extension(
        "PyKLU._klu",  # full import path of the extension
        sources=[
            "PyKLU/_klu.pyx",
            "PyKLU/klu_interf.c",
        ],
        include_dirs=[
            np.get_include(),
            str(INC_DIR),
        ],
        libraries=[
            "klu",
            "btf",
            "amd",
            "colamd",
            "suitesparseconfig",
        ],
        library_dirs=[str(LIB_DIR)],
        # IMPORTANT: avoid an absolute rpath into your build tree.
        # Put the shared libraries *next to* the extension .so in the wheel
        # and use $ORIGIN so the wheel works after installation.
        #extra_link_args=["-Wl,-rpath,$ORIGIN"],
        extra_link_args=[f"-Wl,-rpath,{LIB_DIR}"],  # <-- add this line
    )
    return cythonize([ext])


setup(
    name="PyKLU",
    version="0.1.0",
    packages=["PyKLU"],
    ext_modules=make_extensions(),
    cmdclass={"build_ext": BuildExtWithSuiteSparse},
    include_package_data=True
)
