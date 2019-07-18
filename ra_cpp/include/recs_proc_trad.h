#ifndef RECS_PROC_TRAD_H
#define RECS_PROC_TRAD_H

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

void recs_proc_trad(
    std::vector<Sourcecpp> &sources,
    std::vector<Raycpp> &rays);

#endif /* RECS_PROC_TRAD */