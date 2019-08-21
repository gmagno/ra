#ifndef BIND_FUN_REFPOINT_H
#define BIND_FUN_REFPOINT_H

#include <iostream>

#include "pybind11/complex.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "unsupported/Eigen/Polynomials"
#include "refpoint.h"

namespace py = pybind11;

void bind_refpoint(py::module &m);

#endif /* BIND_FUN_REFPOINT_H */