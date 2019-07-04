#ifndef SOURCE_H
#define SOURCE_H

#include <iostream>
#include "pybind11/pybind11.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"

/* The class Soucespp is used to construct a list of
sound souces objects with several properties. This will be used
during the ray tracing in several sub-functions*/

class Sourcecpp
{
public:
    Sourcecpp(
        Eigen::RowVector3d coord,
        Eigen::RowVector3d orientation,
        Eigen::RowVectorXd power_dB,
        Eigen::RowVectorXd eq_dB,
        Eigen::RowVectorXd power_lin,
        double delay
        ):
    coord(coord), orientation(orientation),
    power_dB(power_dB), eq_dB(eq_dB),
    power_lin(power_lin), delay(delay)
    {}
    ~Sourcecpp()  {} // class destructor - can be automatic later
// Parameters of the Sourcescpp class
Eigen::RowVector3d coord;
Eigen::RowVector3d orientation;
Eigen::RowVectorXd power_dB;
Eigen::RowVectorXd eq_dB;
Eigen::RowVectorXd power_lin;
double delay;
};
#endif /* SOURCE_H */