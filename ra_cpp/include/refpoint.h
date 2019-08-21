#ifndef REFPOINT_H
#define REFPOINT_H

#include <iostream>

#include "pybind11/complex.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "unsupported/Eigen/Polynomials"

namespace py = pybind11;

Eigen::RowVector3f refpoint(Eigen::Ref<Eigen::RowVector3f> ray_origin,
        Eigen::Ref<Eigen::RowVector3f> v_in,
        Eigen::Ref<Eigen::RowVector3f> normal,
        Eigen::Ref<Eigen::RowVector3f> vertcoord);

#endif /* REFPOINT_H */