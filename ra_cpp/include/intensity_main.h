#ifndef INTENSITY_MAIN_H
#define INTENSITY_MAIN_H

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
// #include "geometry.h"
// #include "ray.h"
#include "source.h"
// #include "receiver.h"
// #include "rayreflection.h"
// #include "recgrow.h"
// #include "raysphere_all.h"
// #include "visibilitytest.h"
#include "do_progress.h"


// PYBIND11_MAKE_OPAQUE(std::vector<Raycpp>);
namespace py = pybind11;

std::vector<Sourcecpp> intensity_main(
    double rec_radius_init,
    std::vector<Sourcecpp> &sources,
    double c0,
    Eigen::RowVectorXf m_s,
    Eigen::MatrixXf &alpha_s);

#endif /* INTENSITY_MAIN */