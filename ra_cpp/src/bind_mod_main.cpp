#include "bind_mod_main.h"
PYBIND11_MODULE(ra_cpp, m)
{
    //bind_compute(m);
    bind_doc(m);
    bind_raysphere(m);
    bind_rayreflection(m);
    bind_refpoint(m);
    bind_whichside(m);
    bind_ptinpol(m);
    bind_isleft(m);
    bind_recgrow(m);
    bind_cls_pet(m);
    bind_cls_picleable(m);
    bind_cls_planecpp(m);
    bind_cls_sourcecpp(m);
    bind_cls_receivercpp(m);
    bind_cls_reccrosscpp(m);
    bind_cls_reccrossdircpp(m);
    bind_cls_raycpp(m);
    bind_fun_direct_sound(m);
    bind_fun_raytracer_main(m);
    bind_fun_intensity_main(m);
    bind_t_cat(m);
    bind_i_cat(m);
    bind_cos_cat(m);

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
