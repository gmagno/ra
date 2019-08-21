#include "bind_fun_ptinpol.h"

void bind_ptinpol(py::module &m)
{
    m.def("_ptinpol", ptinpol,
    "Computes the lambda of ray-plane intersection and a boolean for distance travell",
    py::arg("vert_x").noconvert(),
    py::arg("vert_y").noconvert(),
    py::arg("ref_point2d").noconvert()
    );
}