#include "bind_fun_rayreflection.h"

void bind_rayreflection(py::module &m)
{
    m.def("_rayreflection", rayreflection,
    "Computes the outward direction of ray reflection ",
    py::arg("v_in").noconvert(),
    py::arg("normal").noconvert(),
    py::arg("s_s"), py::arg("ref_order"), 
    py::arg("s_on_off"), py::arg("trans_order")  
    );  
}