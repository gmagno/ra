#ifndef POINT_ALL_RECS_H
#define POINT_ALL_RECS_H

#include <iostream>
#include <vector>
#include "pybind11/complex.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "unsupported/Eigen/Polynomials"
#include "source.h"
#include "receiver.h"

namespace py = pybind11;

void point_all_receivers(
    Eigen::RowVector3f source_coord,
    std::vector<Receivercpp> &receivers);

#endif /* POINT_ALL_RECS */