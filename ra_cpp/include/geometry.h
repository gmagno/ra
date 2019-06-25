#ifndef GEOMETRY_H
#define GEOMETRY_H

#include <iostream>
#include "pybind11/pybind11.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"

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


class PlaneMat
{
public:
    // PlaneMat();
    PlaneMat(
        const std::string &name,
        bool bbox,
        Eigen::MatrixXd vertices,
        Eigen::RowVector3d normal,
        Eigen::RowVectorXd vert_x,
        Eigen::RowVectorXd vert_y,
        double area,
        Eigen::RowVector3d centroid,
        Eigen::RowVectorXd alpha,
        double s
    ) {}
    ~PlaneMat() {}


private:
    std::string name;
    bool bbox;
    Eigen::MatrixXd vertices;
    Eigen::RowVector3d normal;
    Eigen::RowVectorXd vert_x;
    Eigen::RowVectorXd vert_y;
    double area;
    Eigen::RowVector3d centroid;
    Eigen::RowVectorXd alpha;
    double s;
};


#endif /* GEOMETRY_H */