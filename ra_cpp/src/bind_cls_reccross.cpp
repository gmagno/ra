#include "bind_cls_reccross.h"
// #include "ray.h"
// #include "bind_cls_ray.h"

void bind_cls_reccrosscpp(py::module &m){
    py::class_<RecCrosscpp>(m, "RecCrosscpp")
        .def(py::init<
        std::vector<float>,
        std::vector<float>,
        std::vector<uint16_t>
        // float,
        // uint16_t
        >())
        .def("reflection_coeff_hist", &RecCrosscpp::reflection_coeff_hist)
        .def("cum_prod", &RecCrosscpp::cum_prod)
        .def("intensity_ref", &RecCrosscpp::intensity_ref)
        .def_readwrite("time_cross", &RecCrosscpp::time_cross)
        .def_readwrite("rad_cross", &RecCrosscpp::rad_cross)
        .def_readwrite("ref_order", &RecCrosscpp::ref_order)
        .def_readwrite("i_cross", &RecCrosscpp::i_cross);
        // .def_readwrite("t_dir", &RecCrosscpp::t_dir)
        // .def_readwrite("n_dir_hits", &RecCrosscpp::n_dir_hits);
}