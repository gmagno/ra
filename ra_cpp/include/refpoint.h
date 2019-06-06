#ifndef REFPOINT_H
#define REFPOINT_H

#include <iostream>

#include "pybind11/complex.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "unsupported/Eigen/Polynomials"

namespace py = pybind11;

Eigen::RowVector3d refpoint(Eigen::Ref<Eigen::RowVector3d> ray_origin, 
        Eigen::Ref<Eigen::RowVector3d> v_in,
        Eigen::Ref<Eigen::RowVector3d> normal,
        Eigen::Ref<Eigen::RowVector3d> vertcoord);

#endif /* REFPOINT_H */