#include "bind_fun_whichside.h"

void bind_whichside(py::module &m)
{
    m.def(
        "_whichside",
        whichside,
    "Calculate if the ray goes towards the plane (whichside>0) or not",
    py::arg("ray_origin").noconvert(),
    py::arg("v_in").noconvert(),
    py::arg("ref_point").noconvert()
    );
}