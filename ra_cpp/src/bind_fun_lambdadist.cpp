#include "bind_fun_lambdadist.h"

void bind_lambdadist(py::module &m)
{
    m.def(
        "_lambdadist",
        lambdadist,
    
    "Computes the lambda of ray-plane intersection and a boolean for distance travell",
    py::arg("ray_origin").noconvert(),
    py::arg("v_in").noconvert(),
    py::arg("ref_point").noconvert()
    );  
}