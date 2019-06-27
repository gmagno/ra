#include "bind_fun_whichside.h"

void bind_whichside(py::module &m)
{
    m.def(
        "_whichside",
        whichside,
    "Computes the lambda of ray-plane intersection and a boolean for distance travell",
    py::arg("ray_origin").noconvert(),
    py::arg("v_in").noconvert(),
    py::arg("ref_point").noconvert()
    );
}