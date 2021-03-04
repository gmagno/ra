#include "refpoint.h"
//Computes the reflection point for a given plane and point of origin (prior to pt-in-polygon test)
Eigen::RowVector3f refpoint(Eigen::Ref<Eigen::RowVector3f> ray_origin,
        Eigen::Ref<Eigen::RowVector3f> v_in,
        Eigen::Ref<Eigen::RowVector3f> normal,
        Eigen::Ref<Eigen::RowVector3f> vertcoord)
{
    // Chech which normal of the plane to use
    double is_plane_detectable = v_in.dot(normal);
    if (is_plane_detectable > 0.0){ // in this case invert normal
        normal = -normal;
        is_plane_detectable = -is_plane_detectable;
    }

    // dot product of plane normal and ray origin
    double n_ro_dot = normal.dot(ray_origin);
    // dot product of plane normal and one of plane vertexes
    double n_vert_dot = normal.dot(vertcoord);
    // calculate the reflection point
    Eigen::RowVector3f ref_point = ray_origin +
        ((n_vert_dot - n_ro_dot) / is_plane_detectable) * v_in;
    return ref_point;
}