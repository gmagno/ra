#include "bind_fun_ptinpol.h"

void bind_ptinpol(py::module &m)
{
    m.def("_ptinpol", ptinpol,
    "Computes the winding number to test if the reflection pt is in or out of the polygon",
    py::arg("vert_x").noconvert(),
    py::arg("vert_y").noconvert(),
    py::arg("ref_point2d").noconvert()
    );
}