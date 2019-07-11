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
        Eigen::RowVector3f coord,
        Eigen::RowVector3f orientation,
        Eigen::RowVectorXf power_dB,
        Eigen::RowVectorXf eq_dB,
        Eigen::RowVectorXf power_lin,
        double delay
        ):
    coord(coord), orientation(orientation),
    power_dB(power_dB), eq_dB(eq_dB),
    power_lin(power_lin), delay(delay)
    {}
    ~Sourcecpp()  {} // class destructor - can be automatic later
// Parameters of the Sourcescpp class
Eigen::RowVector3f coord;
Eigen::RowVector3f orientation;
Eigen::RowVectorXf power_dB;
Eigen::RowVectorXf eq_dB;
Eigen::RowVectorXf power_lin;
double delay;
};
#endif /* SOURCE_H */