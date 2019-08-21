#ifndef BIND_FUN_WHICHSIDE_H
#define BIND_FUN_WHICHSIDE_H

#include <iostream>

#include "pybind11/complex.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "unsupported/Eigen/Polynomials"
#include "whichside.h"

namespace py = pybind11;

void bind_whichside(py::module &m);

#endif /* BIND_FUN_WHICHSIDE_H */