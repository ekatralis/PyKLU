# PyKLU/_klu.pxd
# PyKLU – Python bindings for SuiteSparse KLU
# Copyright (C) 2015-2025 CERN
# Licensed under the LGPL-2.1-or-later. See LICENSE for details.

from libc.stdint cimport int32_t

cdef extern from "klu_interf.h":
	
	ctypedef struct lu_state:
		pass
	
	cdef void hello()
	cdef lu_state* construct_superlu(int m, int n, int nnz, double* Acsc_data_ptr, 
		int32_t* Acsc_indices_ptr, int32_t* Acsc_indptr_ptr, int is_complex)
	cdef void lusolve(lu_state* lus, double* BX, int nrhs)
	cdef void lu_destroy(lu_state* lus)
