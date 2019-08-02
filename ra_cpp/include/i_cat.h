#ifndef I_CAT_H
#define I_CAT_H

#include <iostream>

#include "pybind11/complex.h"
#include "pybind11/eigen.h"
#include <vector>
#include "pybind11/numpy.h"
#include "pybind11/stl.h"
#include "pybind11/pybind11.h"
#include "unsupported/Eigen/Polynomials"
#include "ray.h"

namespace py = pybind11;

Eigen::MatrixXf intensity_cat(std::vector<Raycpp> &rays,
    Eigen::VectorXf &i_dir, int jrec, int time_size);

#endif /* I_CAT_H */