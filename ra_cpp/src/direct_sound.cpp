#include "direct_sound.h"
/* This function calculates the direct sound at each receiver */

std::vector<Sourcecpp> direct_sound(
    std::vector<Sourcecpp> &sources,
    std::vector<Receivercpp> &receivers,
    double rec_radius,
    std::vector<Planecpp> &planes,
    double c0, Eigen::MatrixXf &v_init){
    // loop through sources
    for(auto&& s: sources){
        // calculate the direct sound time of arrival for each receiver
        int rec_c = 0;
        for(auto&& r: receivers){
            // The distance between source and receiver
            Eigen::RowVector3f sr_vec = r.coord - s.coord;
            float dist_dir = sr_vec.norm();
            // std::cout << "distance " << dist_dir << std::endl;
            // visibility test (find plane, distance and check)
            Eigen::RowVector3f v_dir = sr_vec / dist_dir;
            Eigen::RowVector3f ray_origin = s.coord;
            uint16_t plane_detected = 65534;
            double dist_plane = 0.0;
            s.rays[0].plane_finder(planes, ray_origin, v_dir,
                plane_detected, dist_plane);
            // affect time_dir only if distance to plane is bigger
            if (dist_dir < dist_plane){
                s.reccrossdir[rec_c].time_dir = dist_dir / c0;
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
            // s.rays[0].recs[rec_c].time_cross.push_back(dist_dir / c0);
            // perform a visibility test for each receiver
            // plane_finder(planes, s.coord, v_dir, plane_detected, dist);
            // std::cout << "source coord" << s.coord << std::endl;
            // std::cout << "rec coord" << r.coord << std::endl;
            // std::cout << "s-r" << sr_vec << std::endl;
        }
    }
    Eigen::RowVectorXf m_s;
    // m_s << 0.00002, 0.00002, 0.00003, 0.00003, 0.0008, 0.001, 0.004,
    //     0.008;
    // m_s = sources[0].power_lin;
    // // Eigen::VectorXf i_dir(m_s.size());
    // sources[0].reccrossdir[0].i_dir =
    //     sources[0].reccrossdir[0].intensity_dir(
    //     sources[0].power_lin, 1, c0, rec_radius, m_s
    // );
    // sources[0].reccrossdir[0].i_dir = i_dir;
    // std::cout << "i_dir in direct sound: " << sources[0].reccrossdir[0].i_dir << std::endl;
    return sources;

}