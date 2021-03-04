#include "bind_cls_geometry.h"

// Do not worry about pet class
void bind_cls_pet(py::module &m){
    py::class_<Pet>(m, "Pet")
        .def(py::init<const std::string &, int>())
        .def("go_for_a_walk", &Pet::go_for_a_walk)
        .def("get_hunger", &Pet::get_hunger)
        .def("get_name", &Pet::get_name)
        .def_readwrite("name", &Pet::name)
        .def_readwrite("hunger", &Pet::hunger)

        .def("__getstate__", [](const Pet &p) {
        /* Return a tuple that fully encodes the state of the object */
        return py::make_tuple(p.name, p.hunger);
        })
        .def("__setstate__", [](Pet &p, py::tuple t) {
        if (t.size() != 2)
            throw std::runtime_error("Invalid state!");

        /* Invoke the in-place constructor. Note that this is needed even
           when the object just has a trivial default constructor */
        new (&p) Pet(t[0].cast<const std::string>(),
            t[1].cast<int>());

        /* Assign any additional state */
        // pet.go_for_a_walk(t[1].cast<int>());
        // p.get_name();
    });
}


// Do not worry about pet picleable
void bind_cls_picleable(py::module &m){
    py::class_<Pickleable>(m, "Pickleable")
        .def(py::init<std::string>())
        .def("value", &Pickleable::value)
        .def("extra", &Pickleable::extra)
        .def("setExtra", &Pickleable::setExtra)
        .def("__getstate__", [](const Pickleable &p) {
            /* Return a tuple that fully encodes the state of the object */
            return py::make_tuple(p.value(), p.extra());
        })
        .def("__setstate__", [](Pickleable &p, py::tuple t) {
            if (t.size() != 2)
                throw std::runtime_error("Invalid state!");

            /* Invoke the in-place constructor. Note that this is needed even
            when the object just has a trivial default constructor */
            new (&p) Pickleable(t[0].cast<std::string>());

            /* Assign any additional state */
            p.setExtra(t[1].cast<int>());
        });
}

// Geometry class
void bind_cls_planecpp(py::module &m){
    py::class_<Planecpp>(m, "Planecpp")
        .def(py::init<
        const std::string &,
        bool,
        Eigen::MatrixXf,
        Eigen::RowVector3f,
        Eigen::RowVectorXf,
        Eigen::RowVectorXf,
        Eigen::RowVector2i,
        double,
        Eigen::RowVector3f,
        Eigen::RowVectorXf,
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
        .def_readwrite("s", &Planecpp::s)
        // Now, let us try to picke the geometry
        .def("__getstate__", [](const Planecpp &p) {
        /* Return a tuple that fully encodes the state of the object */
        return py::make_tuple(p.name, p.bbox, p.vertices, p.normal,
            p.vert_x, p.vert_y, p.nig, p.area, p.centroid,
            p.alpha, p.s);
        })
        .def("__setstate__", [](Planecpp &p, py::tuple t) {
        if (t.size() != 11)
            throw std::runtime_error("Invalid state!");

        /* Invoke the in-place constructor. Note that this is needed even
           when the object just has a trivial default constructor */
        new (&p) Planecpp(t[0].cast<const std::string>(),
            t[1].cast<bool>(),
            t[2].cast<Eigen::MatrixXf>(),
            t[3].cast<Eigen::RowVector3f>(),
            t[4].cast<Eigen::RowVectorXf>(),
            t[5].cast<Eigen::RowVectorXf>(),
            t[6].cast<Eigen::RowVector2i>(),
            t[7].cast<double>(),
            t[8].cast<Eigen::RowVector3f>(),
            t[9].cast<Eigen::RowVectorXf>(),
            t[10].cast<double>());

        /* Assign any additional state */
        // pet.go_for_a_walk(t[1].cast<int>());
        // p.get_name();
    });
}
