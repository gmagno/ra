#include "direct_sound.h"
/* Computes the time of arrival, doa, and energy of the direct sound */

std::vector<Sourcecpp> direct_sound(
    std::vector<Sourcecpp> &sources,
    std::vector<Receivercpp> &receivers,
    double rec_radius,
    std::vector<Planecpp> &planes,
    double c0, Eigen::MatrixXf &v_init){
    // loop through sources
    for(auto&& s: sources){
        // calculate the direct sound time of arrival for each receiver
        // orient toward source (optional) and fig8 mic
        point_all_receivers(s.coord, receivers);
        int rec_c = 0;
        for(auto&& r: receivers){
            // std::cout << "rec fig 8  in direct sound: " << r.orientation_fig8 <<
            // " for source: " << s.coord << std::endl;
            // The distance between source and receiver
            Eigen::RowVector3f sr_vec = r.coord - s.coord;
            float dist_dir = sr_vec.norm();
            // std::cout << "distance " << dist_dir << std::endl;
            // visibility test (find plane, distance and check)
            Eigen::RowVector3f v_dir = sr_vec / dist_dir;
            // std::cout << "dir ray direction: " << v_dir << std::endl; 
            Eigen::RowVector3f ray_origin = s.coord;
            uint16_t plane_detected = 65534;
            double dist_plane = 0.0;
            s.rays[0].plane_finder(planes, ray_origin, v_dir,
                plane_detected, dist_plane);
            // affect time_dir only if distance to plane is bigger
            if (dist_dir < dist_plane){
                // increase size_of
                s.reccrossdir[rec_c].size_of_time++;
                // direct time
                s.reccrossdir[rec_c].time_dir = dist_dir / c0;
                // orient toward source (optional) and fig8 mic
                // r.orientation = r.point_to_source(s.coord);
                // r.orientation_fig8 = r.point_fig8();
                // calculate cossine
                s.reccrossdir[rec_c].cos_dir = v_dir.dot(r.orientation_fig8);
                // std::cout << "cossine value: " << s.reccrossdir[rec_c].cos_dir << std::endl;
                /* Count the number of rays hiting a receiver in direct sound.
                This may help keep things simple and honest, since acumulation
                of energy in reflection may lead to bigger reflected energies
                than direct sound */
                int rc = 0; // ray counter
                for(auto&& v: s.rays){
                    Eigen::RowVector3f v_dir = v_init.row(rc);
                    double time_cross_dummy = 0.0;
                    double dist_rp_rec_dummy = 0.0;
                    // test if this direct ray hits the receiver
                    r.raysphere(s.coord, v_dir, rec_radius,
                        c0, 1.0, time_cross_dummy, dist_rp_rec_dummy);
                    // if it does, increase hits_dir by 1
                    if (time_cross_dummy != 0.0)
                        s.reccrossdir[rec_c].hits_dir++;
                    rc++; // next ray
                }
                /* if the direct path is unblocked and there were no
                positive hits (hits_dir == 0) in receiver testing
                (may occur with small number of rays),
                then increase hits_dir by 1 */
                if (s.reccrossdir[rec_c].hits_dir == 0)
                    s.reccrossdir[rec_c].hits_dir++;
            }
            rec_c++;
        }
    }
    return sources;
}