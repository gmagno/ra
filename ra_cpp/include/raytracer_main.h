#ifndef RAYTRACER_MAIN_H
#define RAYTRACER_MAIN_H

#include <iostream>

#include "pybind11/complex.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "pybind11/stl.h"
#include "unsupported/Eigen/Polynomials"
#include <vector>
#include "geometry.h"
#include "ray.h"
#include "source.h"

namespace py = pybind11;

void raytracer_main(
    double ht_length,
    int allow_scattering,
    int transition_order,
    std::vector<Sourcecpp> &sources,
    std::vector<Planecpp> &planes,
    double c0, Eigen::MatrixXd &v_init,
    std::vector<Raycpp> &rays);

#endif /* RAYTRACER_MAIN */