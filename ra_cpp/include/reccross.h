#ifndef RECCROSS_H
#define RECCROSS_H

#include <iostream>
#include <vector>
#include "pybind11/pybind11.h"
#include "pybind11/eigen.h"
// #include <unsupported/Eigen/CXX11/Tensor>
#include "pybind11/numpy.h"
#include "pybind11/stl.h"

/* The class RecCrosscpp is used to construct a list of
receiver objects, which will receive source-ray-receiver
dependent data such as: time of ray cross, current receiver
radius at crossing and current reflection order at crossing */
typedef Eigen::Array<uint16_t, 1, Eigen::Dynamic > RowVectorXui;
class RecCrosscpp
{
public:
    RecCrosscpp(
        std::vector<float> time_cross,
        std::vector<float> rad_cross,
        std::vector<uint16_t> ref_order,
        std::vector<float> cos_cross
        ):
    time_cross(time_cross), rad_cross(rad_cross),
    ref_order(ref_order), cos_cross(cos_cross)
    {}
    ~RecCrosscpp()  {} // class destructor - can be automatic later
    // Method to retrieve a sequence of Reflection coefficients
    Eigen::MatrixXf reflection_coeff_hist(RowVectorXui &planes_hist,
        Eigen::MatrixXf &refcoeff, int freq_size);
    // Method to calculate the cumulative product of reflection coefficients
    Eigen::MatrixXf cum_prod(Eigen::MatrixXf &refcoeff_hist);
    // Method to calculate sound intensity at direct sound
    Eigen::MatrixXf intensity_ref(
        Eigen::RowVectorXf power_lin,
        int Nr, double c0,
        Eigen::RowVectorXf m_s,
        Eigen::MatrixXf &refcoeff_cumprod);
// Parameters of the Receivercpp class
std::vector<float> time_cross;
std::vector<float> rad_cross;
std::vector<uint16_t> ref_order;
std::vector<float> cos_cross;
Eigen::MatrixXf i_cross;
};
#endif /* RECCROSS_H */