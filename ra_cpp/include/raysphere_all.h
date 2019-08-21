#ifndef RAYSPHERE_ALL_H
#define RAYSPHERE_ALL_H

#include <iostream>
#include <vector>
#include "pybind11/complex.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "unsupported/Eigen/Polynomials"
#include "raysphere.h"
#include "source.h"
#include "receiver.h"

namespace py = pybind11;

void ray_sphere_all(int sc, int rc,
    Eigen::RowVector3f r_origin,
    Eigen::RowVector3f v_dir,
    std::vector<Sourcecpp> &sources,
    std::vector<Receivercpp> &receivers,
    std::vector<double> &dist_rp_rec,
    int ref_order,
    double rec_radius_current,
    double c0, double cum_dist);

#endif /* RAYSPHERE_ALL */