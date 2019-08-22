#include "bind_fun_cos_cat.h"

void bind_cos_cat(py::module &m)
{
    m.def("_cos_cat", cos_cat,
    "Concatenate cossine (fig8) vector",
    py::arg("rays").noconvert(),
    py::arg("cos_dir").noconvert(),
    py::arg("jrec").noconvert(),
    py::arg("time_size").noconvert()
    );
}