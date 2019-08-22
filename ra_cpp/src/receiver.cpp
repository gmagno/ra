#include "receiver.h"

// Method to point receiver to a given sound source
Eigen::RowVector3f Receivercpp::point_to_source(
    Eigen::RowVector3f &source_coord){
    orientation = source_coord - coord;
    orientation = orientation / orientation.norm();
    return orientation;
}

// Method to point the receiver 90 deg from orientation y -axis
Eigen::RowVector3f Receivercpp::point_fig8(){
    Eigen::RowVector3f orientation_z = orientation;
    orientation_z(2) += 0.2;
    orientation_z = orientation_z / orientation_z.norm();
    Eigen::RowVector3f orientation_fig8 =
        orientation.cross(orientation_z);
    orientation_fig8 = orientation_fig8 / orientation_fig8.norm();
    return orientation_fig8;
}

// Method to calculate if a receiver is intercepted by a ray
void Receivercpp::raysphere(
    Eigen::Ref<Eigen::RowVector3f> ray_origin,
    Eigen::Ref<Eigen::RowVector3f> v_dir,
    double rec_radius,
    double c0,
    double cum_dist,
    double &time_cross,
    double &dist_rp_rec){
    dist_rp_rec = 0.0; 
    // Initialize timecross
    // double time_cross = 0.0;
    // Calculate the roots for ray-sphere intersection
    Eigen::RowVector3f ray_rec_vec = ray_origin - coord;
    double b = ray_rec_vec.dot(v_dir);
    double dist_origin2rec = ray_rec_vec.norm();
    double c = pow(dist_origin2rec, 2.0) - pow(rec_radius, 2.0);
    double delta = pow(b, 2.0) - c;
    // test of ray intersection
    if (delta >= 0.0 && b <= 0.0){
        // distance from center of receiver to mid crossing point inside rec
        double d = (ray_rec_vec - b * v_dir).norm();
        // real distance from wall to receiver
        dist_rp_rec = sqrt(pow(dist_origin2rec, 2.0) + pow(d, 2.0));
        time_cross = (cum_dist + dist_rp_rec) / c0;
    }
    // return time_cross;
}