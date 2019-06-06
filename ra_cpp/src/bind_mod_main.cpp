
#include "bind_mod_main.h"

PYBIND11_MODULE(ra_cpp, m)
{
    //bind_compute(m);
    bind_doc(m);
    bind_raysphere(m);
    bind_rayreflection(m);
    bind_refpoint(m);
    bind_lambdadist(m);
    bind_ptinpol(m);
    bind_isleft(m);
    bind_recgrow(m);
    

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
