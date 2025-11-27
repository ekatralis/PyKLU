# PyKLU/_klu.pyi
from __future__ import annotations

from typing import Any
import numpy as np
import numpy.typing as npt
from scipy.sparse import csc_matrix

ArrayLike = npt.ArrayLike
Float64Array1D = npt.NDArray[np.float64]
Float64Array2D = npt.NDArray[np.float64]

class Klu:
    def __init__(self, Acsc: csc_matrix) -> None: ...
    # or more specific:
    # def __init__(self, Acsc: "scipy.sparse.csc_matrix[Any]") -> None: ...

    def solve(self, B: ArrayLike, copy: bool = ...) -> np.ndarray: ...
    def inplace_solve_batched(self, B: Float64Array2D) -> None: ...
    def inplace_solve_vector(self, B: Float64Array1D) -> None: ...
    def __dealloc__(self) -> None: ...