#include "bind_cls_reccrossdir.h"
// #include "ray.h"
// #include "bind_cls_ray.h"

void bind_cls_reccrossdircpp(py::module &m){
    py::class_<RecCrossDircpp>(m, "RecCrossDircpp")
        .def(py::init<
        float,
        uint16_t
        >())
        .def("intensity_dir", &RecCrossDircpp::intensity_dir)
        .def_readwrite("time_dir", &RecCrossDircpp::time_dir)
        .def_readwrite("hits_dir", &RecCrossDircpp::hits_dir)
        .def_readwrite("i_dir", &RecCrossDircpp::i_dir);
}