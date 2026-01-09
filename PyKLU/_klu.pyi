# PyKLU/_klu.pyi
# PyKLU – Python bindings for SuiteSparse KLU
# Copyright (C) 2015-2025 CERN
# Licensed under the LGPL-2.1-or-later. See LICENSE for details.

from __future__ import annotations

from typing import Any
import numpy as np
import numpy.typing as npt
from scipy.sparse import csc_matrix

ArrayLike = npt.ArrayLike

class Klu:
    """
    Sparse LU factorization using the KLU library.

    This class wraps a factorization of a sparse matrix ``A`` stored in
    CSC (Compressed Sparse Column) format, and provides methods to solve
    linear systems of the form ::

        A x = b
        A X = B

    for one or multiple right-hand sides.

    The underlying factorization is created once at construction time and
    reused for subsequent solves.
    """
    def __init__(self, Acsc: csc_matrix) -> None: 
        """
        Factorize a sparse matrix in CSC format using KLU.

        Parameters
        ----------
        Acsc :
            Sparse matrix in SciPy ``csc_matrix`` format representing the
            coefficient matrix ``A``.

            The matrix is internally converted to use

            * ``float64`` for the data array, and
            * ``int32`` for the index arrays

            if it does not already have those dtypes.

        Raises
        ------
        TypeError
            If ``Acsc`` is not an instance of :class:`scipy.sparse.csc_matrix`.
        """
        ...

    def solve(self, B: ArrayLike, copy: bool = ...) -> np.ndarray: 
        """
        Solve the linear system ``A X = B`` using the stored LU factorization.

        The shape and layout of ``B`` determine how the system is interpreted:

        * If ``B`` is 1D with shape ``(m,)``, the method solves
            ``A x = b`` and returns a 1D array of shape ``(m,)``.
        * If ``B`` is 2D with shape ``(m, k)``, the method solves
            ``A X = B`` for ``k`` right-hand sides and returns a 2D array
            of shape ``(m, k)``.

        Parameters
        ----------
        B :
            Right-hand side vector or matrix. Any array-like object that can
            be converted to a NumPy array is accepted. The leading dimension
            must match the number of rows ``m`` of ``A``.

            * For a single RHS, ``B.shape == (m,)``.
            * For multiple RHS, ``B.shape == (m, k)``.

        copy :
            Controls whether the solve is performed in-place when possible.

            * If ``True`` (default), a new ``float64`` array is always
                allocated internally. The original ``B`` is never modified.
            * If ``False``, the solve is performed in-place on ``B`` **if**
                it is a ``float64`` NumPy array with appropriate memory layout:
                - 1D: contiguous (C or Fortran) ``float64`` array
                - 2D: Fortran-contiguous (column-major) ``float64`` array
                The modified array is then returned.

        Returns
        -------
        numpy.ndarray
            The solution array. When ``copy=True`` this is always a newly
            allocated array. When ``copy=False`` and the input meets the
            required conditions, this will be the same array object as the
            input ``B`` (mutated in place).

        Raises
        ------
        TypeError
            If ``copy=False`` and ``B`` does not have dtype ``float64``.
        ValueError
            If the shape of ``B`` does not match the problem size, or if
            ``copy=False`` is requested but the array is not contiguous in a
            required layout (e.g. non-contiguous 1D array, or non-Fortran
            2D array).
        """
        ...

    def __dealloc__(self) -> None: 
        """
        Release native resources associated with the factorization.

        This is called automatically when the :class:`Klu` instance is
        garbage-collected and should not normally be invoked directly.
        """
        ...