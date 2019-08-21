#ifndef DIRECT_SOUND_H
#define DIRECT_SOUND_H

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
#include "visibilitytest.h"
#include "point_all_recs.h"
#include "plane_finder.h"
#include "do_progress.h"


// PYBIND11_MAKE_OPAQUE(std::vector<Raycpp>);
namespace py = pybind11;

std::vector<Sourcecpp> direct_sound(
    std::vector<Sourcecpp> &sources,
    std::vector<Receivercpp> &receivers,
    double rec_radius,
    std::vector<Planecpp> &planes,
    double c0, Eigen::MatrixXf &v_init);

#endif /* DIRECT_SOUND */