#ifndef RAY_H
#define RAY_H

#include <iostream>
#include <vector>
#include "pybind11/pybind11.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/stl.h"
#include "geometry.h"
#include "reccross.h"
/* The class raycpp is used to construct a list of
ray objects which will contain the ray history in the room.
This will be filled during the ray tracing main function*/

// typedef Eigen::Matrix<uint16_t, 1, Eigen::Dynamic > RowVectorXui;
typedef Eigen::Array<uint16_t, 1, Eigen::Dynamic > RowVectorXui;

class Raycpp
{
public:
    Raycpp(
        // Eigen::RowVectorXi planes_hist,
        RowVectorXui planes_hist,
        Eigen::MatrixXf refpts_hist,
        std::vector<RecCrosscpp> recs
        ):
    planes_hist(planes_hist), refpts_hist(refpts_hist),
    recs(recs)
    {}
    ~Raycpp()  {} // class destructor - can be automatic later
    // Method to find the plane and reflection point
    void plane_finder(
        std::vector<Planecpp> &planes,
        Eigen::RowVector3f &ray_origin,
        Eigen::Ref<Eigen::RowVector3f> v_in,
        uint16_t &plane_detected,
        double &dist);
// Parameters of the Receivercpp class
// Eigen::RowVectorXi planes_hist;
RowVectorXui planes_hist;
Eigen::MatrixXf refpts_hist;
std::vector<RecCrosscpp> recs;
};
#endif /* RAY_H */