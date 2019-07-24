#ifndef VISIBILITYTEST_H
#define VISIBILITYTEST_H

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

void visibility_test(int sc, int rc,
    bool pop_condition,
    std::vector<Sourcecpp> &sources,
    std::vector<Receivercpp> &receivers,
    std::vector<double> &dist_rp_rec,
    double dist);

#endif /* VISIBILITYTEST */