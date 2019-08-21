#ifndef RECGROW_H
#define RECGROW_H

#include <iostream>

#include "pybind11/complex.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "unsupported/Eigen/Polynomials"

namespace py = pybind11;

void recgrow(int alow_growth, int transition_order, int ref_order,
    double rec_radius_init, double rec_radius_final, double &rec_radius_current,
    double cum_dist, int N_rays);

#endif /* RECGROW_H */