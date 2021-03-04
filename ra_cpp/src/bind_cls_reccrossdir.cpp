#include "bind_cls_reccrossdir.h"
// #include "ray.h"
// #include "bind_cls_ray.h"

void bind_cls_reccrossdircpp(py::module &m){
    py::class_<RecCrossDircpp>(m, "RecCrossDircpp")
        .def(py::init<
        int,
        float,
        uint16_t,
        float
        >())
        .def("intensity_dir", &RecCrossDircpp::intensity_dir)
        .def_readwrite("size_of_time", &RecCrossDircpp::size_of_time)
        .def_readwrite("time_dir", &RecCrossDircpp::time_dir)
        .def_readwrite("hits_dir", &RecCrossDircpp::hits_dir)
        .def_readwrite("cos_dir", &RecCrossDircpp::cos_dir)
        .def_readwrite("i_dir", &RecCrossDircpp::i_dir)
        // Now, let us try to picke the geometry
        .def("__getstate__", [](const RecCrossDircpp &p) {
        /* Return a tuple that fully encodes the state of the object */
        return py::make_tuple(p.size_of_time, p.time_dir, 
            p.hits_dir, p.cos_dir);
        })
        .def("__setstate__", [](RecCrossDircpp &p, py::tuple t) {
        if (t.size() != 4)
            throw std::runtime_error("Invalid state!");

        /* Invoke the in-place constructor. Note that this is needed even
           when the object just has a trivial default constructor */
        new (&p) RecCrossDircpp(
            t[0].cast<int>(),
            t[1].cast<float>(),
            t[2].cast<uint16_t>(),
            t[3].cast<float>());

        /* Assign any additional state */
        // pet.go_for_a_walk(t[1].cast<int>());
        // p.get_name();
    });
}