#include "bind_cls_source.h"
// #include "ray.h"
// #include "bind_cls_ray.h"

void bind_cls_sourcecpp(py::module &m){
    py::class_<Sourcecpp>(m, "Sourcecpp")
        .def(py::init<
        Eigen::RowVector3f,
        Eigen::RowVector3f,
        Eigen::RowVectorXf,
        Eigen::RowVectorXf,
        Eigen::RowVectorXf,
        double,
        std::vector<Raycpp>,
        std::vector<RecCrossDircpp>
        >())
        .def_readwrite("coord", &Sourcecpp::coord)
        .def_readwrite("orientation", &Sourcecpp::orientation)
        .def_readwrite("power_dB", &Sourcecpp::power_dB)
        .def_readwrite("eq_dB", &Sourcecpp::eq_dB)
        .def_readwrite("power_lin", &Sourcecpp::power_lin)
        .def_readwrite("delay", &Sourcecpp::delay)
        .def_readwrite("rays", &Sourcecpp::rays)
        .def_readwrite("reccrossdir", &Sourcecpp::reccrossdir)
        // Now, let us try to picke the geometry
        .def("__getstate__", [](const Sourcecpp &p) {
        /* Return a tuple that fully encodes the state of the object */
        return py::make_tuple(p.coord, p.orientation, p.power_dB,
            p.eq_dB, p.power_lin, p.delay,
            p.rays, p.reccrossdir);
        })
        .def("__setstate__", [](Sourcecpp &p, py::tuple t) {
        if (t.size() != 8)
            throw std::runtime_error("Invalid state!");

        /* Invoke the in-place constructor. Note that this is needed even
           when the object just has a trivial default constructor */
        new (&p) Sourcecpp(
            t[0].cast<Eigen::RowVector3f>(),
            t[1].cast<Eigen::RowVector3f>(),
            t[2].cast<Eigen::RowVectorXf>(),
            t[3].cast<Eigen::RowVectorXf>(),
            t[4].cast<Eigen::RowVectorXf>(),
            t[5].cast<double>(),
            t[6].cast<std::vector<Raycpp>>(),
            t[7].cast<std::vector<RecCrossDircpp>>());

        /* Assign any additional state */
        // pet.go_for_a_walk(t[1].cast<int>());
        // p.get_name();
    });
}