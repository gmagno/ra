#include "bind_cls_reccross.h"
// #include "ray.h"
// #include "bind_cls_ray.h"

void bind_cls_reccrosscpp(py::module &m){
    py::class_<RecCrosscpp>(m, "RecCrosscpp")
        .def(py::init<
        std::vector<float>,
        std::vector<float>,
        std::vector<uint16_t>,
        std::vector<float>
        >())
        .def("reflection_coeff_hist", &RecCrosscpp::reflection_coeff_hist)
        .def("cum_prod", &RecCrosscpp::cum_prod)
        .def("intensity_ref", &RecCrosscpp::intensity_ref)
        .def_readwrite("time_cross", &RecCrosscpp::time_cross)
        .def_readwrite("rad_cross", &RecCrosscpp::rad_cross)
        .def_readwrite("ref_order", &RecCrosscpp::ref_order)
        .def_readwrite("cos_cross", &RecCrosscpp::cos_cross)
        .def_readwrite("i_cross", &RecCrosscpp::i_cross)
        // Now, let us try to picke the geometry
        .def("__getstate__", [](const RecCrosscpp &p) {
        /* Return a tuple that fully encodes the state of the object */
        return py::make_tuple(p.time_cross, p.rad_cross,
            p.ref_order, p.cos_cross);
        })
        .def("__setstate__", [](RecCrosscpp &p, py::tuple t) {
        if (t.size() != 4)
            throw std::runtime_error("Invalid state!");

        /* Invoke the in-place constructor. Note that this is needed even
           when the object just has a trivial default constructor */
        new (&p) RecCrosscpp(
            t[0].cast<std::vector<float>>(),
            t[1].cast<std::vector<float>>(),
            t[2].cast<std::vector<uint16_t>>(),
            t[3].cast<std::vector<float>>());

        /* Assign any additional state */
        // pet.go_for_a_walk(t[1].cast<int>());
        // p.get_name();
    });

}