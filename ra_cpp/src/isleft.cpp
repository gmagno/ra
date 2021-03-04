#include "isleft.h"
// Computes the inline isleft function. Used for point in polygon test
double isleft(Eigen::Ref<Eigen::RowVector2f> Vx,
    Eigen::Ref<Eigen::RowVector2f> Vy,
    Eigen::Ref<Eigen::RowVector2f> ref_point2d)
{
    double isl = (Vx(1) - Vx(0)) * (ref_point2d(1) - Vy(0)) -
        (ref_point2d(0) - Vx(0)) * (Vy(1) - Vy(0));
    return isl;
}