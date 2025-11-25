# setup.py

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize
import numpy as np
import pathlib
import subprocess


ROOT = pathlib.Path(__file__).parent.resolve()
SS_ROOT = ROOT / "extern" / "SuiteSparse"
LIB_DIR = SS_ROOT / "lib"
INC_DIR = SS_ROOT / "include" / "suitesparse"


class BuildExtWithSuiteSparse(build_ext):
    """
    build_ext that first builds SuiteSparse (static libs) so we can
    statically link them into PyKLU._klu.
    """

    def run(self):
        # Build SuiteSparse components; adjust to use your actual build method.
        # If you already have CMake configured per component, you can skip this
        # and just rely on extern/SuiteSparse/lib/*.a existing.
        suitesparse_components = [
            "SuiteSparse_config",
            "COLAMD",
            "AMD",
            "BTF",
            "CHOLMOD",
            "KLU",
        ]

        for comp in suitesparse_components:
            comp_src = SS_ROOT / comp
            build_dir = comp_src / "build"
            build_dir.mkdir(exist_ok=True)

            print(f"Configuring SuiteSparse component: {comp}")
            subprocess.check_call(
                [
                    "cmake",
                    "-S", str(comp_src),
                    "-B", str(build_dir),
                    "-DSUITESPARSE_LOCAL_INSTALL=1",
                    "-DBUILD_SHARED_LIBS=ON",
                    "-DBUILD_STATIC_LIBS=ON",
                    "-DSUITESPARSE_USE_OPENMP=OFF",   # <- key line
                    # optionally:
                    # "-DSUITESPARSE_USE_FORTRAN=OFF",
                ]
            )


            print(f"Building SuiteSparse component: {comp}")
            subprocess.check_call(
                ["cmake", "--build", str(build_dir), "--config", "Release", "-j8"]
            )

            print(f"Installing SuiteSparse component: {comp}")
            subprocess.check_call(
                ["cmake", "--install", str(build_dir)]
            )

        # At this point, we expect static libs here:
        #   LIB_DIR / "libklu.a"
        #   LIB_DIR / "libbtf.a"
        #   LIB_DIR / "libamd.a"
        #   LIB_DIR / "libcolamd.a"
        #   LIB_DIR / "libsuitesparseconfig.a"
        #   LIB_DIR / "libcholmod.a"

        super().run()


def make_extensions():
    # List the static libs to link in
    static_libs = [
        "libklu.a",
        "libbtf.a",
        "libamd.a",
        "libcolamd.a",
        "libsuitesparseconfig.a",
        "libcholmod.a",
    ]

    extra_objects = [str(LIB_DIR / libname) for libname in static_libs]

    ext = Extension(
        "PyKLU._klu",
        sources=[
            "PyKLU/_klu.pyx",
            "PyKLU/klu_interf.c",
        ],
        include_dirs=[
            "PyKLU",                 # for klu_interf.h
            np.get_include(),
            str(INC_DIR),            # SuiteSparse headers (klu.h, amd.h, ...)
        ],
        extra_objects=extra_objects,  # static link SuiteSparse
        # DO NOT set "libraries" / "library_dirs" here when statically linking
    )

    return cythonize([ext])


setup(
    name="PyKLU",
    version="0.1.0",
    packages=["PyKLU"],
    ext_modules=make_extensions(),
    cmdclass={"build_ext": BuildExtWithSuiteSparse},
    include_package_data=True,
)