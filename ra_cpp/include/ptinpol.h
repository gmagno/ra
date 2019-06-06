#ifndef PTINPOL_H
#define PTINPOL_H

#include <iostream>

#include "pybind11/complex.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "unsupported/Eigen/Polynomials"

namespace py = pybind11;

int ptinpol(Eigen::Ref<Eigen::RowVectorXd> vert_x,
        Eigen::Ref<Eigen::RowVectorXd> vert_y, 
        Eigen::Ref<Eigen::RowVector2d> ref_point2d);

#endif /* PTINPOL_H */