#include "bind_fun_raytracer_main.h"

void bind_fun_raytracer_main(py::module &m)
{
    m.def(
        "_raytracer_main",
        raytracer_main,
    "The main function to compute the ray tracing.",
    py::arg("ht_length"),
    py::arg("allow_scattering"),
    py::arg("transition_order"),
    py::arg("sources"),
    py::arg("geometry"),
    py::arg("c0"),
    py::arg("v_init"),
    py::arg("rays")
    );
}