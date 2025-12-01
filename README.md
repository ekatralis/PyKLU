# PyKLU
> Version 0.1.0

## About
PyKLU provides python bindings for the KLU algorithm to solve sparse linear systems on CPU

## Installation
PyKLU requires the following packages to install and function:
```
numpy
Cython
scipy
```
### Recommended installation procedure
Set up a conda environment:
```bash
conda create -n pyklu_test python=3.1x # Replace with desired python version
```
Then activate the environment and install the dependencies. Installing PyKLU in this way requires `cmake` and `blas` to be installed on the system. If no system-wide installation is present, they must be installed within the environment:
```bash
conda activate pyklu_test
# Python dependencies
pip install numpy
pip install Cython
pip install scipy
# Install dependencies
conda install cmake
conda install -c conda-forge libblas
```
Installing requires cloning the repository with `--recursive` enabled, to also clone the SuiteSparse repo.
```bash
git clone --recursive https://github.com/ekatralis/PyKLU.git
```
Then from within the repository folder (`cd PyKLU`), the package can be installed via `pip` in editable mode:
```bash
pip install -e .
```

## Licensing

PyKLU is licensed under the GNU Lesser General Public License v2.1 (LGPL-2.1) (see `LICENSE`).  
This project includes the KLU sparse solver from SuiteSparse, distributed under the GNU LGPL v2.1 (or later) with a static-linking exception.  
See `LICENSE.suitesparse` for the full SuiteSparse license text.

## TODO
- Package is still under development. This README serves as preliminary documentation
- As the intended goal is to publish this package on `PyPI`, we bundle the SuiteSparse libs together with `PyKLU`, which means that `OpenMP` had to be disabled. This shouldn't have any noticeable impact on performance, but the goal is to update setup.py, so PyKLU can be linked against any desired SuiteSparse library.
- Publish to PyPI
