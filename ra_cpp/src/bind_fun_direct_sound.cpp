#include "bind_fun_direct_sound.h"

void bind_fun_direct_sound(py::module &m)
{
    m.def(
        "_direct_sound",
        direct_sound,
    "The main function to compute the direct sound.",
    py::arg("sources"),
    py::arg("receivers"),
    py::arg("rec_radius"),
    py::arg("geometry"),
    py::arg("c0"),
    py::arg("v_init")
    );
}