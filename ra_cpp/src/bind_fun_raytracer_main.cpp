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
    py::arg("rec_radius_init"),
    py::arg("allow_growth"),
    py::arg("rec_radius_final"),
    py::arg("sources"),
    py::arg("receivers"),
    py::arg("geometry"),
    py::arg("c0"),
    py::arg("v_init")
    );
}