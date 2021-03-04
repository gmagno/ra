#include "bind_fun_recgrow.h"

void bind_recgrow(py::module &m)
{
    m.def("_recgrow", recgrow,
    "Computes the new receiver sphere radius based on the distance travelled by the ray.",
    py::arg("growth_allowed"), py::arg("trans_order"),
    py::arg("ref_order"), py::arg("rec_init"),
    py::arg("rec_max"), py::arg("rec_current"),
    py::arg("dist_cum"), py::arg("Nrays")
    );
}

