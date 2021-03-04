#include "visibilitytest.h"
/* Visibility test of the ray. Compares the distance of the next reflection point
    with the distance to receiver. If the later is larger or equal than the former,
    there is an obstacle between the ray and the receiver. */
void visibility_test(int sc, int rc,
    bool pop_condition,
    std::vector<Sourcecpp> &sources,
    std::vector<Receivercpp> &receivers,
    std::vector<double> &dist_rp_rec,
    double dist){
    int rec_c = 0;
    if (pop_condition){
        for(auto&& r: receivers){
            if (dist_rp_rec[rec_c] >= dist){
                sources[sc].reccrossdir[rec_c].size_of_time--;
                sources[sc].rays[rc].recs[rec_c].time_cross.pop_back();
                sources[sc].rays[rc].recs[rec_c].rad_cross.pop_back();
                sources[sc].rays[rc].recs[rec_c].ref_order.pop_back();
            }
        rec_c++;
        }
    }
}