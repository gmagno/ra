#ifndef RAYSPHERE_H
#define RAYSPHERE_H

#include <iostream>

#include "pybind11/complex.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "unsupported/Eigen/Polynomials"
#include "raysphere.h"

namespace py = pybind11;

double raysphere(Eigen::Ref<Eigen::RowVector3f> ray_origin,
    Eigen::Ref<Eigen::RowVector3f> v_dir,
    Eigen::Ref<Eigen::RowVector3f> rec_coord,
    double rec_radius,
    double c0,
    double dist_travel);

#endif /* RAYSPHERE */