#include "bind_cls_ray.h"

void bind_cls_raycpp(py::module &m){
    py::class_<Raycpp>(m, "Raycpp")
        .def(py::init<
        // Eigen::RowVectorXi,
        RowVectorXui,
        Eigen::MatrixXf
        >())
        //.def("point_to_source", &Raycpp::point_to_source)
        .def_readwrite("planes_hist", &Raycpp::planes_hist)
        .def_readwrite("refpts_hist", &Raycpp::refpts_hist);
}