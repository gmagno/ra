#include "raysphere.h"
// Test if the ray intersect a receiver sphere and, if TRUE, compute the time instant of this intersection
double raysphere(Eigen::Ref<Eigen::RowVector3f> ray_origin,
    Eigen::Ref<Eigen::RowVector3f> v_dir,
    Eigen::Ref<Eigen::RowVector3f> rec_coord,
    double rec_radius,
    double c0,
    double dist_travel){
    // Initialize timecross
    double time_cross = 0.0;
    // Calculate the roots for ray-sphere intersection
    Eigen::RowVector3f ray_rec_vec = ray_origin - rec_coord;
    double b = ray_rec_vec.dot(v_dir);
    double dist_origin2rec = ray_rec_vec.norm();
    double c = pow(dist_origin2rec, 2.0) - pow(rec_radius, 2.0);
    double delta = pow(b, 2.0) - c;
    // test of ray intersection
    if (delta >= 0.0 && b <= 0.0){
        // distance from center of receiver to mid crossing point
        double d = (ray_rec_vec - b * v_dir).norm();
        // distance from wall to receiver
        double dL = sqrt(pow(dist_origin2rec, 2.0) + pow(d, 2.0));
        time_cross = (dist_travel + dL) / c0;
    }
    return time_cross;
}