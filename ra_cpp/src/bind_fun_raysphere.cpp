#include "bind_fun_raysphere.h"

void bind_raysphere(py::module &m)
{
    m.def("_raysphere", raysphere,
    "Test if the ray intersect a receiver sphere and, if TRUE, compute the time instant of this intersection",
    py::arg("ray_origin").noconvert(),
    py::arg("v_dir").noconvert(),
    py::arg("rec_coord").noconvert(),
    py::arg("rec_radius"), py::arg("c0"), py::arg("dist_travel")
    );
}