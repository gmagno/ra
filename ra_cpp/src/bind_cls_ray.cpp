#include "bind_cls_ray.h"

void bind_cls_raycpp(py::module &m){
    py::class_<Raycpp>(m, "Raycpp")
        .def(py::init<
        // Eigen::RowVectorXi,
        RowVectorXui,
        Eigen::MatrixXf,
        std::vector<RecCrosscpp>
        >())
        //.def("point_to_source", &Raycpp::point_to_source)
        .def_readwrite("planes_hist", &Raycpp::planes_hist)
        .def_readwrite("refpts_hist", &Raycpp::refpts_hist)
        .def_readwrite("recs", &Raycpp::recs)
        // Now, let us try to picke the geometry
        .def("__getstate__", [](const Raycpp &p) {
        /* Return a tuple that fully encodes the state of the object */
        return py::make_tuple(p.planes_hist, p.refpts_hist, p.recs);
        })
        .def("__setstate__", [](Raycpp &p, py::tuple t) {
        if (t.size() != 3)
            throw std::runtime_error("Invalid state!");

        /* Invoke the in-place constructor. Note that this is needed even
           when the object just has a trivial default constructor */
        new (&p) Raycpp(
            t[0].cast<RowVectorXui>(),
            t[1].cast<Eigen::MatrixXf>(),
            t[2].cast<std::vector<RecCrosscpp>>());

        /* Assign any additional state */
        // pet.go_for_a_walk(t[1].cast<int>());
        // p.get_name();
    });
}