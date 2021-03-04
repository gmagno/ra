#include "recgrow.h"
//Computes the new receiver sphere radius based on the distance travelled by the ray.
void recgrow(int alow_growth, int transition_order, int ref_order,
    double rec_radius_init, double rec_radius_final, double &rec_radius_current,
    double cum_dist, int N_rays)
{
if (alow_growth == 1 && ref_order > transition_order) // conditions to allow growth
    rec_radius_current = 2.0 * cum_dist / sqrt(double(N_rays)); // new radii
    if (rec_radius_current < rec_radius_init) // if new smaller than initial correct
        rec_radius_current = rec_radius_init;
    else if (rec_radius_current > rec_radius_final) // if new bigger than final correct
        rec_radius_current = rec_radius_final;
}

// double recgrow(int growth_allowed, int trans_order, int ref_order,
//     double rec_init, double rec_max, double rec_current,
//     double dist_cum, int Nrays)
// {
// double rec_radii = rec_init;
// if (growth_allowed == 1 && ref_order > trans_order) // conditions to allow growth
//     rec_radii = 2.0 * dist_cum / sqrt(double(Nrays)); // new radii
//     if (rec_radii < rec_init) // if new smaller than initial correct
//         rec_radii = rec_init;
//     else if (rec_radii > rec_max) // if new bigger than final correct
//         rec_radii = rec_max;
// return rec_radii;
// }