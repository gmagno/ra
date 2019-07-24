#include "raysphere_all.h"
/* This function is used to test all receivers. It will perform the
raysphere test for each receiver and append the time_cross, rad_cross,
and correct ref_order to each source.ray.receiver object
*/
void ray_sphere_all(int sc, int rc,
    Eigen::RowVector3f r_origin,
    Eigen::RowVector3f v_dir,
    std::vector<Sourcecpp> &sources,
    std::vector<Receivercpp> &receivers,
    std::vector<double> &dist_rp_rec,
    int ref_order,
    double rec_radius_current,
    double c0, double cum_dist){
        // receiver processing
        int rec_c = 0;
        // std::vector<double> dist_rp_rec(N_recs, 0.0);
        // dist_rp_rec = { 0.0 };
        for(auto&& r: receivers){
            double time_cross = 0.0;
            // double dist_rp_rec = 0.0;
            r.raysphere(r_origin, v_dir, rec_radius_current,
                c0, cum_dist, time_cross, dist_rp_rec[rec_c]);
            // sources[sc].rays[rc].recs[rec_c].time_cross.push_back(time_cross);
            if(time_cross != 0.0){
                sources[sc].rays[rc].recs[rec_c].time_cross.push_back(time_cross);
                sources[sc].rays[rc].recs[rec_c].rad_cross.push_back(rec_radius_current);
                sources[sc].rays[rc].recs[rec_c].ref_order.push_back(ref_order);
            }
            // std::cout << "receiver: " << rec_c << ", time cross is: " << time_cross << std::endl;
            rec_c++;
        }
    }