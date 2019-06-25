#include "bind_cls_geometry.h"

void bind_cls_pet(py::module &m){
    py::class_<Pet>(m, "Pet")
        .def(py::init<const std::string &, int>())
        .def("go_for_a_walk", &Pet::go_for_a_walk)
        .def("get_hunger", &Pet::get_hunger)
        .def("get_name", &Pet::get_name);
}

void bind_cls_planemat(py::module &m){
    py::class_<PlaneMat>(m, "PlaneMat")
        .def(py::init<
        const std::string &,
        bool,
        Eigen::MatrixXd,
        Eigen::RowVector3d,
        Eigen::RowVectorXd,
        Eigen::RowVectorXd,
        double,
        Eigen::RowVector3d,
        Eigen::RowVectorXd,
        double
        >());
}
