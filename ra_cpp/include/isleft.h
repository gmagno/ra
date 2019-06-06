#ifndef ISLEFT_H
#define ISLEFT_H

#include <iostream>

#include "pybind11/complex.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "unsupported/Eigen/Polynomials"

namespace py = pybind11;

double isleft(Eigen::Ref<Eigen::RowVector2d> Vx, 
    Eigen::Ref<Eigen::RowVector2d> Vy, 
    Eigen::Ref<Eigen::RowVector2d> ref_point2d);

#endif /* ISLEFT_H */