#ifndef RAYTRACER_MAIN_H
#define RAYTRACER_MAIN_H

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

std::vector<Raycpp> raytracer_main(
    double ht_length,
    int allow_scattering,
    int transition_order,
    std::vector<Sourcecpp> &sources,
    std::vector<Planecpp> &planes,
    double c0, Eigen::MatrixXf &v_init,
    std::vector<Raycpp> &rays);

#endif /* RAYTRACER_MAIN */