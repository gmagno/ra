#ifndef RAY_H
#define RAY_H

#include <iostream>
#include "pybind11/pybind11.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"

/* The class raycpp is used to construct a list of
ray objects which will contain the ray history in the room.
This will be filled during the ray tracing main function*/

class Raycpp
{
public:
    Raycpp(
        Eigen::RowVectorXi planes_hist,
        Eigen::MatrixXd refpts_hist
        ):
    planes_hist(planes_hist), refpts_hist(refpts_hist)
    {}
    ~Raycpp()  {} // class destructor - can be automatic later
    // Method to point receiver to a given sound source
    // Eigen::RowVector3d point_to_source(Eigen::Ref<Eigen::RowVector3d> source_coord);
// Parameters of the Receivercpp class
Eigen::RowVectorXi planes_hist;
Eigen::MatrixXd refpts_hist;
};
#endif /* RAY_H */