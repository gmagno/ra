#ifndef RECCROSSDIR_H
#define RECCROSSDIR_H

#include <iostream>
#include <vector>
#include "pybind11/pybind11.h"
#include "pybind11/eigen.h"
// #include <unsupported/Eigen/MatrixFunctions>
#include "pybind11/numpy.h"
#include "pybind11/stl.h"

/* The class RecCrossDircpp is used to construct a list of
receiver objects, which will receive source-receiver
direct sounda data such as: time_dir (time instant of direct sound)
and hits_dir (the number of times a receiver is crossed by ray
in direct incidence - without reflections) */

class RecCrossDircpp
{
public:
    RecCrossDircpp(
        float time_dir,
        uint16_t hits_dir
        ):
    time_dir(time_dir), hits_dir(hits_dir)
    {}
    ~RecCrossDircpp()  {} // class destructor - can be automatic later
    // Method to calculate sound intensity at direct sound
    Eigen::VectorXf intensity_dir(
        Eigen::RowVectorXf power_lin,
        int Nr, double c0,
        double rec_radius_init,
        Eigen::RowVectorXf m_s);
// Parameters of the RecCrossDircpp class
float time_dir;
uint16_t hits_dir;
Eigen::VectorXf i_dir;
};
#endif /* RECCROSSDIR_H */