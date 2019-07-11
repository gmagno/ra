#include "geometry.h"

// Method to calculate reflection point
Eigen::RowVector3f Planecpp::refpoint3d(
    Eigen::Ref<Eigen::RowVector3f> ray_origin,
    Eigen::Ref<Eigen::RowVector3f> v_in){
    Eigen::RowVector3f ref_point;
    Eigen::RowVector3f vertex = vertices.row(2);
    // Calculate reflection point
    ref_point = refpoint(ray_origin, v_in, normal, vertex);
    return ref_point;
}

// For point in polygon test
int Planecpp::test_single_plane(Eigen::Ref<Eigen::RowVector3f> ray_origin,
    Eigen::Ref<Eigen::RowVector3f> v_in,
    Eigen::Ref<Eigen::RowVector3f> ref_point){
    // Calculate if the ray goes towards the plane
    // (whichside>0) or not
    double whichside = v_in.dot(ref_point) - v_in.dot(ray_origin);
    // Calculate the distance from ray_origin to ref_point
    double distance = (ref_point - ray_origin).norm();
    // Initialize winding number (wn) por pt in pol test
    int wn = 0; // wn = 0 means rp is outside of the plane
    // Things will be calculated only if the ray goes towards the plane
    if (whichside > 0.0){
        // Get the reflection point in 2D for pt in polygon test
        Eigen::RowVector2f ref_point2d;
        ref_point2d(0) = ref_point(nig(0));
        ref_point2d(1) = ref_point(nig(1));
        // Point in polygon test
        wn = ptinpol(vert_x, vert_y, ref_point2d);
    }
    return wn;
}


