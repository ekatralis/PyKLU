# PyKLU/_klu.pyi
# PyKLU – Python bindings for SuiteSparse KLU
# Copyright (C) 2015-2025 CERN
# Licensed under the LGPL-2.1-or-later. See LICENSE for details.

from __future__ import annotations

from typing import Any, Literal, overload
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

    Notes
    -----
    The factorization is real or complex depending on whether ``Acsc`` is a
    complex-valued sparse matrix (as detected by ``np.iscomplexobj(Acsc)``).

    * Real factorization: ``solve`` operates on/returns ``float64`` arrays.
    * Complex factorization: ``solve`` operates on/returns ``complex128`` arrays.
    """

    def __init__(self, Acsc: csc_matrix) -> None:
        """
        Factorize a sparse matrix in CSC format using KLU.

        Parameters
        ----------
        Acsc :
            Sparse matrix in SciPy ``csc_matrix`` format representing the
            coefficient matrix ``A``.

            The matrix is internally converted (if needed) to:

            * ``float64`` / ``complex128`` for the data array, and
            * ``int32`` for the index arrays (``indices`` and ``indptr``).

        Raises
        ------
        TypeError
            If ``Acsc`` is not an instance of :class:`scipy.sparse.csc_matrix`.
        AssertionError
            If ``Acsc`` is not square.
        """
        ...

    # -------- solve overloads (copy=True) --------
    @overload
    def solve(self, B: ArrayLike, copy: Literal[True] = ...) -> np.ndarray: ...
    # (We keep copy=True broad because the implementation will allocate and
    # return either float64 or complex128 depending on the factorization.)

    # -------- solve overloads (copy=False, real/complex in-place expectations) --------
    @overload
    def solve(
        self,
        B: npt.NDArray[np.float64],
        copy: Literal[False],
    ) -> npt.NDArray[np.float64]: ...
    @overload
    def solve(
        self,
        B: npt.NDArray[np.complex128],
        copy: Literal[False],
    ) -> npt.NDArray[np.complex128]: ...

    def solve(self, B: ArrayLike, copy: bool = ...) -> np.ndarray:
        """
        Solve the linear system ``A X = B`` using the stored LU factorization.

        The shape of ``B`` determines how the system is interpreted:

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

            * If ``True`` (default), a new array is always allocated internally.
              The original ``B`` is never modified. The result dtype matches the
              factorization: ``float64`` for real, ``complex128`` for complex.

            * If ``False``, the solve is performed in-place on ``B`` **if**
              it is a NumPy array of the correct dtype and layout:

              - Real factorization requires ``B.dtype == float64``
              - Complex factorization requires ``B.dtype == complex128``

              Layout requirements when ``copy=False``:
              - 1D RHS: contiguous (C- or Fortran-contiguous) array
              - 2D RHS: Fortran-contiguous (column-major) array

              The modified input array is then returned.

        Returns
        -------
        numpy.ndarray
            The solution array.

            * When ``copy=True`` this is always a newly allocated array.
            * When ``copy=False`` and the input meets the required conditions,
              this will be the same array object as the input ``B`` (mutated
              in place).

        Raises
        ------
        TypeError
            If ``copy=False`` and ``B`` does not have the required dtype for
            the factorization (``float64`` for real, ``complex128`` for complex).
        ValueError
            If ``B`` is not 1D or 2D, if its shape does not match the problem
            size, or if ``copy=False`` is requested but the array does not meet
            the contiguity/layout requirements.
        """
        ...

    def __dealloc__(self) -> None:
        """
        Release native resources associated with the factorization.

        This is called automatically when the :class:`Klu` instance is
        garbage-collected and should not normally be invoked directly.
        """
        ...