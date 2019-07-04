#include "bind_cls_geometry.h"

void bind_cls_pet(py::module &m){
    py::class_<Pet>(m, "Pet")
        .def(py::init<const std::string &, int>())
        .def("go_for_a_walk", &Pet::go_for_a_walk)
        .def("get_hunger", &Pet::get_hunger)
        .def("get_name", &Pet::get_name);
}

void bind_cls_planecpp(py::module &m){
    py::class_<Planecpp>(m, "Planecpp")
        .def(py::init<
        const std::string &,
        bool,
        Eigen::MatrixXd,
        Eigen::RowVector3d,
        Eigen::RowVectorXd,
        Eigen::RowVectorXd,
        Eigen::RowVector2i,
        double,
        Eigen::RowVector3d,
        Eigen::RowVectorXd,
        double
        >())
        .def("refpoint3d", &Planecpp::refpoint3d)
        .def("test_single_plane", &Planecpp::test_single_plane)
        .def_readwrite("name", &Planecpp::name)
        .def_readwrite("bbox", &Planecpp::bbox)
        .def_readwrite("vertices", &Planecpp::vertices)
        .def_readwrite("normal", &Planecpp::normal)
        .def_readwrite("vert_x", &Planecpp::vert_x)
        .def_readwrite("vert_y", &Planecpp::vert_y)
        .def_readwrite("nig", &Planecpp::nig)
        .def_readwrite("area", &Planecpp::area)
        .def_readwrite("centroid", &Planecpp::centroid)
        .def_readwrite("alpha", &Planecpp::alpha)
        .def_readwrite("s", &Planecpp::s);
}
