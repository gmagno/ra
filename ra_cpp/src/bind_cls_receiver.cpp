#include "bind_cls_receiver.h"

void bind_cls_receivercpp(py::module &m){
    py::class_<Receivercpp>(m, "Receivercpp")
        .def(py::init<
        Eigen::RowVector3f,
        Eigen::RowVector3f
        >())
        .def("point_to_source", &Receivercpp::point_to_source)
        .def("point_fig8", &Receivercpp::point_fig8)
        .def_readwrite("coord", &Receivercpp::coord)
        .def_readwrite("orientation", &Receivercpp::orientation)
        .def_readwrite("orientation", &Receivercpp::orientation_fig8)
        // Now, let us try to picke the geometry
        .def("__getstate__", [](const Receivercpp &p) {
        /* Return a tuple that fully encodes the state of the object */
        return py::make_tuple(p.coord, p.orientation, p.orientation_fig8);
        })
        .def("__setstate__", [](Receivercpp &p, py::tuple t) {
        if (t.size() != 3)
            throw std::runtime_error("Invalid state!");

        /* Invoke the in-place constructor. Note that this is needed even
           when the object just has a trivial default constructor */
        new (&p) Receivercpp(
            t[0].cast<Eigen::RowVector3f>(),
            t[1].cast<Eigen::RowVector3f>());

        /* Assign any additional state */
        // p.point_to_source(t[1].cast<Eigen::RowVector3f>());
        // p.point_fig8(t[2].cast<Eigen::RowVector3f>());
        // p.get_name();
    });
}