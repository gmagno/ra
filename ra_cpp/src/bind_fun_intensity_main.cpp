#include "bind_fun_intensity_main.h"

void bind_fun_intensity_main(py::module &m)
{
    m.def(
        "_intensity_main",
        intensity_main,
    "The main function to compute the sound intensities of ray tracing.",
    py::arg("rec_radius_init"),
    py::arg("sources"),
    py::arg("c0"),
    py::arg("m_s"),
    py::arg("alpha_s")
    );
}