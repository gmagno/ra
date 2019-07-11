#include "recgrow.h"

double recgrow(int growth_allowed, int trans_order, int ref_order,
    double rec_init, double rec_max, double rec_current,
    double dist_cum, int Nrays)
{
double rec_radii = rec_init;
if (growth_allowed == 1 && ref_order > trans_order) // conditions to allow growth
    rec_radii = 2.0 * dist_cum / sqrt(double(Nrays)); // new radii
    if (rec_radii < rec_init) // if new smaller than initial correct
        rec_radii = rec_init;
    else if (rec_radii > rec_max) // if new bigger than final correct
        rec_radii = rec_max;
return rec_radii;
}