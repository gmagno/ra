#ifndef BIND_FUN_RECGROW_H
#define BIND_FUN_RECGROW_H

#include <iostream>

#include "pybind11/complex.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "unsupported/Eigen/Polynomials"
#include "recgrow.h"

namespace py = pybind11;

void bind_recgrow(py::module &m);

#endif /* BIND_FUN_RECGROW_H */