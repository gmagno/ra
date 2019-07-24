#ifndef RECCROSS_H
#define RECCROSS_H

#include <iostream>
#include <vector>
#include "pybind11/pybind11.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/stl.h"

/* The class RecCrosscpp is used to construct a list of
receiver objects, which will receive source-ray-receiver
dependent data such as: time of ray cross, current receiver
radius at crossing and current reflection order at crossing */

class RecCrosscpp
{
public:
    RecCrosscpp(
        std::vector<float> time_cross,
        std::vector<float> rad_cross,
        std::vector<uint16_t> ref_order
        // float t_dir,
        // uint16_t n_dir_hits
        ):
    time_cross(time_cross), rad_cross(rad_cross),
    ref_order(ref_order)
    // t_dir(t_dir), n_dir_hits(n_dir_hits)
    {}
    ~RecCrosscpp()  {} // class destructor - can be automatic later
    // Methods
    // Eigen::RowVector3f point_to_source(Eigen::RowVector3f &source_coord);
// Parameters of the Receivercpp class
std::vector<float> time_cross;
std::vector<float> rad_cross;
std::vector<uint16_t> ref_order;
// float t_dir;
// uint16_t n_dir_hits;
};
#endif /* RECCROSS_H */