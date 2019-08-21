#ifndef WHICHSIDE_H
#define WHICHSIDE_H

#include <iostream>

#include "pybind11/complex.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "unsupported/Eigen/Polynomials"


namespace py = pybind11;

double whichside(Eigen::Ref<Eigen::RowVector3f> ray_origin,
        Eigen::Ref<Eigen::RowVector3f> v_in,
        Eigen::Ref<Eigen::RowVector3f> ref_point);

#endif /* WHICHSIDE_H */