#include "isleft.h"

double isleft(Eigen::Ref<Eigen::RowVector2d> Vx,
    Eigen::Ref<Eigen::RowVector2d> Vy,
    Eigen::Ref<Eigen::RowVector2d> ref_point2d)
{
    double isl = (Vx(1) - Vx(0)) * (ref_point2d(1) - Vy(0)) -
        (ref_point2d(0) - Vx(0)) * (Vy(1) - Vy(0));
    return isl;
}