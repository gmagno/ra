#ifndef BIND_FUN_ISLEFT_H
#define BIND_FUN_ISLEFT_H

#include <iostream>

#include "pybind11/complex.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "unsupported/Eigen/Polynomials"
#include "isleft.h"

namespace py = pybind11;

void bind_isleft(py::module &m);

#endif /* BIND_FUN_ISLEFT_H */