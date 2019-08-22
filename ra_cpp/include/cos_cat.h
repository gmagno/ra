#ifndef COS_CAT_H
#define COS_CAT_H

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
// Eigen
Eigen::RowVectorXf cos_cat(std::vector<Raycpp> &rays,
    float cos_dir, int jrec, int time_size);

// Original - Dynamic alloc
// std::vector<float> time_cat(std::vector<Raycpp> &rays,
//     float time_dir, int jrec);

// std vector - known size
// std::vector<float> time_cat(std::vector<Raycpp> &rays,
//     float time_dir, int jrec, int time_size);

#endif /* COS_CAT_H */