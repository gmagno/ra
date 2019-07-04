#ifndef GEOMETRY_H
#define GEOMETRY_H

#include <iostream>
#include "pybind11/pybind11.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "refpoint.h"
#include "ptinpol.h"
#include "isleft.h"

/* The class Pet is used solely for instructional purposes*/
class Pet
{
public:
    Pet(const std::string &name, int hunger) : name(name), hunger(hunger) {}
    ~Pet() {}

    void go_for_a_walk() { hunger++; }
    const std::string &get_name() const { return name; }
    int get_hunger() const { return hunger; }

private:
    std::string name;
    int hunger;
};

/* The class Planecpp is used to construct a list of
plane objects with several properties. This will be used
during the ray tracing in several sub-functions*/

class Planecpp
{
public:
    // Planecpp();
    Planecpp(
        const std::string &name,
        bool bbox,
        Eigen::MatrixXd vertices,
        Eigen::RowVector3d normal,
        Eigen::RowVectorXd vert_x,
        Eigen::RowVectorXd vert_y,
        Eigen::RowVector2i nig,
        double area,
        Eigen::RowVector3d centroid,
        Eigen::RowVectorXd alpha,
        double s
    ):
    name(name), bbox(bbox), vertices(vertices),
    normal(normal), vert_x(vert_x), vert_y(vert_y),
    nig(nig), area(area), centroid(centroid),
    alpha(alpha), s(s)
    {}
    ~Planecpp()  {} // can be automatic later

    // Method to calculate reflection point
    Eigen::RowVector3d refpoint3d(Eigen::Ref<Eigen::RowVector3d> ray_origin,
        Eigen::Ref<Eigen::RowVector3d> v_in);

    // For point in polygon test
    int test_single_plane(Eigen::Ref<Eigen::RowVector3d> ray_origin,
        Eigen::Ref<Eigen::RowVector3d> v_in,
        Eigen::Ref<Eigen::RowVector3d> ref_point);
// Parameters of the Planecpp class
std::string name;
bool bbox;
Eigen::MatrixXd vertices;
Eigen::RowVector3d normal;
Eigen::RowVectorXd vert_x;
Eigen::RowVectorXd vert_y;
Eigen::RowVector2i nig;
double area;
Eigen::RowVector3d centroid;
Eigen::RowVectorXd alpha;
double s;
};


// class Planecpp
// {
// public:
//     // Planecpp();
//     Planecpp(
//         const std::string &name,
//         bool bbox,
//         Eigen::MatrixXd vertices,
//         Eigen::RowVector3d normal,
//         Eigen::RowVectorXd vert_x,
//         Eigen::RowVectorXd vert_y,
//         Eigen::RowVector2i nig,
//         double area,
//         Eigen::RowVector3d centroid,
//         Eigen::RowVectorXd alpha,
//         double s
//     ):
//     name(name), bbox(bbox), vertices(vertices),
//     normal(normal), vert_x(vert_x), vert_y(vert_y),
//     nig(nig), area(area), centroid(centroid),
//     alpha(alpha), s(s)
//     {}
//     ~Planecpp() {}
//     const std::string &get_pname() const {
//         std::cout << "bbox in c++: " << bbox << std::endl;
//         return name;
//     }

//     double get_area(){
//         std::cout << "area in c++ is: " << area << std::endl;
//         return area;
//     }

//     // Mathod to calculate reflection point
//     Eigen::RowVector3d refpoint3d(Eigen::Ref<Eigen::RowVector3d> ray_origin,
//         Eigen::Ref<Eigen::RowVector3d> v_in){
//         Eigen::RowVector3d ref_point;
//         Eigen::RowVector3d vertex = vertices.row(2);
//         // Calculate reflection point
//         ref_point = refpoint(ray_origin, v_in, normal, vertex);
//         return ref_point;
//     }

//     // For point in polygon test
//     int test_single_plane(Eigen::Ref<Eigen::RowVector3d> ray_origin,
//         Eigen::Ref<Eigen::RowVector3d> v_in,
//         Eigen::Ref<Eigen::RowVector3d> ref_point){
//         // Calculate if the ray goes towards the plane
//         // (whichside>0) or not
//         double whichside = v_in.dot(ref_point) - v_in.dot(ray_origin);
//         // Calculate the distance from ray_origin to ref_point
//         double distance = (ref_point - ray_origin).norm();
//         // Initialize winding number (wn) por pt in pol test
//         int wn = 0; // wn = 0 means rp is outside of the plane
//         // Things will be calculated only if the ray goes towards the plane
//         if (whichside > 0.0){
//             // Get the reflection point in 2D for pt in polygon test
//             Eigen::RowVector2d ref_point2d;
//             ref_point2d(0) = ref_point(nig(0));
//             ref_point2d(1) = ref_point(nig(1));
//             // Point in polygon test
//             wn = ptinpol(vert_x, vert_y, ref_point2d);
//         }
//         return wn;
//     }
// std::string name;
// bool bbox;
// Eigen::MatrixXd vertices;
// Eigen::RowVector3d normal;
// Eigen::RowVectorXd vert_x;
// Eigen::RowVectorXd vert_y;
// Eigen::RowVector2i nig;
// double area;
// Eigen::RowVector3d centroid;
// Eigen::RowVectorXd alpha;
// double s;

// // private:
// //     std::string name;
// //     bool bbox;
// //     Eigen::MatrixXd vertices;
// //     Eigen::RowVector3d normal;
// //     Eigen::RowVectorXd vert_x;
// //     Eigen::RowVectorXd vert_y;
// //     Eigen::RowVector2i nig;
// //     double area;
// //     Eigen::RowVector3d centroid;
// //     Eigen::RowVectorXd alpha;
// //     double s;
// };


#endif /* GEOMETRY_H */