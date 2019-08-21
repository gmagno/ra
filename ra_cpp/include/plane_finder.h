#ifndef PLANE_FINDER_H
#define PLANE_FINDER_H

#include <iostream>

#include "pybind11/complex.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "pybind11/stl.h"
// #include "pybind11/stl_bind.h"
// #include "pybind11/functional.h"
// #include "pybind11/chrono.h"
#include "unsupported/Eigen/Polynomials"
#include <vector>
#include "geometry.h"
#include "ray.h"
#include "source.h"


// PYBIND11_MAKE_OPAQUE(std::vector<Raycpp>);
namespace py = pybind11;

void plane_finder(
        std::vector<Planecpp> &planes,
        Eigen::RowVector3f &ray_origin,
        Eigen::Ref<Eigen::RowVector3f> v_in,
        uint16_t &plane_detected,
        double &dist);

#endif /* PLANE_FINDER */