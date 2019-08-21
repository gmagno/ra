#include "bind_fun_isleft.h"

void bind_isleft(py::module &m)
{
    m.def("_isleft", isleft,
    "Computes the inline isleft function. Used for point in polygon test",
    py::arg("Vx").noconvert(),
    py::arg("Vy").noconvert(),
    py::arg("ref_point2d").noconvert()
    );  
}