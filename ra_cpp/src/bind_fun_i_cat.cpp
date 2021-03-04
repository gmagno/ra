#include "bind_fun_i_cat.h"

void bind_i_cat(py::module &m)
{
    m.def("_intensity_cat", intensity_cat,
    "Get the intensity matrix for each encounter w/ receiver and concatenate all to an intensity matrix",
    py::arg("rays").noconvert(),
    py::arg("time_dir").noconvert(),
    py::arg("jrec").noconvert(),
    py::arg("time_size").noconvert()
    );
}