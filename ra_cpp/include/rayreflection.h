#ifndef RAYREFLECTION_H
#define RAYREFLECTION_H

#include <iostream>

#include "pybind11/complex.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "unsupported/Eigen/Polynomials"
#include <algorithm>
#include <random>
#include <math.h>


namespace py = pybind11;

Eigen::RowVector3d rayreflection(Eigen::Ref<Eigen::RowVector3d> v_in,
    Eigen::Ref<Eigen::RowVector3d> normal,
    double s_s,
    int ref_order,
    int s_on_off,
    int trans_order);

#endif /* REFLECTION_H */