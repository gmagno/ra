#include "bind_fun_refpoint.h"

void bind_refpoint(py::module &m)
{
    m.def("_refpoint", refpoint,
    "Computes the reflection point for a given plane and point of origin (prior to pt-in-polygon test)",
    py::arg("ray_origin").noconvert(),
    py::arg("v_dir").noconvert(),
    py::arg("normal").noconvert(),
    py::arg("vertcoord").noconvert()
    );
}