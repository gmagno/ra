#include "receiver.h"

// Method to point receiver to a given sound source
Eigen::RowVector3d Receivercpp::point_to_source(
    Eigen::Ref<Eigen::RowVector3d> source_coord){    orientation = coord - source_coord;
    orientation = orientation / orientation.norm();
    return orientation;
}