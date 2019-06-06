#ifndef LAMBDADIST_H
#define LAMBDADIST_H

#include <iostream>

#include "pybind11/complex.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "unsupported/Eigen/Polynomials"


namespace py = pybind11;

py::array_t<double> lambdadist(Eigen::Ref<Eigen::RowVector3d> ray_origin, 
        Eigen::Ref<Eigen::RowVector3d> v_in,
        Eigen::Ref<Eigen::RowVector3d> ref_point);

#endif /* LAMBDADIST_H */