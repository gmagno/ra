#include "bind_fun_t_cat.h"

void bind_t_cat(py::module &m)
{
    m.def("_time_cat", time_cat,
    "Concatenate time vector",
    py::arg("rays").noconvert(),
    py::arg("time_dir").noconvert(),
    py::arg("jrec").noconvert()
    );
}