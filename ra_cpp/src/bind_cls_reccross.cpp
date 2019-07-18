#include "bind_cls_reccross.h"
// #include "ray.h"
// #include "bind_cls_ray.h"

void bind_cls_reccrosscpp(py::module &m){
    py::class_<RecCrosscpp>(m, "RecCrosscpp")
        .def(py::init<
        std::vector<float>,
        std::vector<float>,
        std::vector<uint16_t>
        >())
        .def_readwrite("time_cross", &RecCrosscpp::time_cross)
        .def_readwrite("rad_cross", &RecCrosscpp::rad_cross)
        .def_readwrite("ref_order", &RecCrosscpp::ref_order);
}