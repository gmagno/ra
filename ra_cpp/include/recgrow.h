#ifndef RECGROW_H
#define RECGROW_H

#include <iostream>

#include "pybind11/complex.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "unsupported/Eigen/Polynomials"

namespace py = pybind11;

double recgrow(int growth_allowed, int trans_order, int ref_order,
    double rec_init, double rec_max, double rec_current,
    double dist_cum, int Nrays);

#endif /* RECGROW_H */