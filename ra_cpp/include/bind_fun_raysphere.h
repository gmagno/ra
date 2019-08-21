#ifndef BIND_FUN_RAYSPHERE_H
#define BIND_FUN_RAYSPHERE_H

#include <iostream>

#include "pybind11/complex.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "unsupported/Eigen/Polynomials"
#include "raysphere.h"

namespace py = pybind11;

void bind_raysphere(py::module &m);

#endif /* BIND_FUN_RAYSPHERE_H */