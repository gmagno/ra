#ifndef RECEIVER_H
#define RECEIVER_H

#include <iostream>
#include "pybind11/pybind11.h"
#include "pybind11/eigen.h"
#include <Eigen/Dense>
#include "pybind11/numpy.h"

/* The class Raycpp is used to construct a list of
receiver objects with several properties. This will be used
during the ray tracing in several sub-functions*/

class Receivercpp
{
public:
    Receivercpp(
        Eigen::RowVector3f coord,
        Eigen::RowVector3f orientation
        ):
    coord(coord), orientation(orientation)
    {}
    ~Receivercpp()  {} // class destructor - can be automatic later
    // Method to point receiver to a given sound source
    Eigen::RowVector3f point_to_source(Eigen::RowVector3f &source_coord);
    // Method to point the receiver 90 deg from orientation y -axis
    Eigen::RowVector3f point_fig8();
    // Method to calculate if a receiver is intercepted by a ray
    void raysphere(
        Eigen::Ref<Eigen::RowVector3f> ray_origin,
        Eigen::Ref<Eigen::RowVector3f> v_dir,
        double rec_radius,
        double c0,
        double cum_dist,
        double &time_cross,
        double &dist_rp_rec);
// Parameters of the Receivercpp class
Eigen::RowVector3f coord;
Eigen::RowVector3f orientation;
Eigen::RowVector3f orientation_fig8;
};
#endif /* RECEIVER_H */