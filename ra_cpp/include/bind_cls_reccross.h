#ifndef BIND_CLS_RECCROSS_H
#define BIND_CLS_RECCROSS_H

#include <iostream>

#include "pybind11/complex.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "unsupported/Eigen/Polynomials"
#include "reccross.h"

namespace py = pybind11;

void bind_cls_reccrosscpp(py::module &m);
#endif /* BIND_CLS_RECCROSS_H */