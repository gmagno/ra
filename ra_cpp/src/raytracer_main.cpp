#include "raytracer_main.h"


std::vector<Sourcecpp> raytracer_main(
    double ht_length,
    int allow_scattering,
    int transition_order,
    double rec_radius_init,
    int alow_growth,
    double rec_radius_final,
    std::vector<Sourcecpp> &sources,
    std::vector<Receivercpp> &receivers,
    std::vector<Planecpp> &planes,
    double c0,
    Eigen::MatrixXf &v_init){
    int N_rays = sources[0].rays.size();
    int N_recs = sources[0].rays[0].recs.size();
    int N_max_ref = sources[0].rays[0].planes_hist.size(); // max ref_order
    int N_max_ro = sources[0].rays[0].refpts_hist.rows(); // max number of ref points saved
    int sc = 0; // source counter
    for(auto&& s: sources){
        // std::cout << "test" << s.rays[0].planes_hist << std::endl;
        std::cout << "Tracing rays for source: " << sc + 1 << " at: (" << s.coord << ") [m]" << std::endl;
        // orient toward source (optional) and fig8 mic
        point_all_receivers(s.coord, receivers);
        // std::cout << "rec 0 fig 8  in main: " << 
        //     receivers[0].orientation_fig8 <<
        //     " for source: " << s.coord << std::endl;
        int rc = 0; // ray counter
        for(auto&& v: s.rays){
            progress_bar(rc, N_rays);
            double rec_radius_current = rec_radius_init;
            std::vector<double> dist_rp_rec(N_recs, 0.0);
            uint16_t plane_detected = 65534; // initialize detected plane
            double dist = 0.0; // initialize distance travelled in ray section
            double cum_dist = 0.0; // initialize cumulative distance
            int ref_order = 0; // initialize reflection order
            Eigen::RowVector3f r_origin;
            r_origin = s.coord; // initialize ray origin
            Eigen::RowVector3f v_dir = v_init.row(rc);
            // while loop
            bool pop_condition = false;
            while(ref_order < N_max_ref){ //  (cum_dist / c0) <= ht_length && 
                // find the intercepted plane
                v.plane_finder(planes, r_origin, v_dir, plane_detected, dist);
                // fill the plane in appropriate place
                v.planes_hist[ref_order] = plane_detected;
                // fill the reflection points up to transition order + 2
                if (ref_order < N_max_ro)
                    v.refpts_hist.row(ref_order) = r_origin;
                // stop loop while if no plane is detected
                if (plane_detected == 65533)
                    break; // and after fill a invalid_ray seq
                // visibility test
                visibility_test(sc, rc, pop_condition, sources,
                    receivers, dist_rp_rec, dist);
                // reflect the ray
                // int n_spec_ref = 0;
                v_dir = rayreflection(v_dir,
                planes[plane_detected].normal,
                planes[plane_detected].s,
                ref_order, allow_scattering, transition_order);
                // increase reflection order
                ref_order++;
                cum_dist += dist;
                pop_condition = true;
                // increase the receiver size (if allowed by conditions)
                recgrow(alow_growth, transition_order, ref_order,
                    rec_radius_init, rec_radius_final, rec_radius_current,
                    cum_dist, N_rays);
                // std::cout << "for " << ref_order << "rec radius is: " << rec_radius_current << "[m]" << std::endl;
                // receiver processing
                ray_sphere_all(sc, rc, r_origin, v_dir, sources,
                    receivers, dist_rp_rec, ref_order,
                    rec_radius_current, c0, cum_dist);
            }
            // std::cout << "testing ray: " << rc << " plane seq after:" << rays[rc].planes_hist << std::endl;
            // std::cout << "testing ray: " << rc << " r_p seq after:" << rays[rc].refpts_hist << std::endl;
            rc++; // increase ray counter
        }
        std::cout<< std::endl;
        sc++; // increase source counter
    }
    return sources;
}

/* inline implementation of all receiver test - with rayshere
// rec_c = 0;
// for(auto&& r: receivers){
//     double time_cross = 0.0;
//     // double dist_rp_rec = 0.0;
//     r.raysphere(r_origin, v_dir, rec_radius_current,
//         c0, cum_dist, time_cross, dist_rp_rec[rec_c]);
//     // sources[sc].rays[rc].recs[rec_c].time_cross.push_back(time_cross);
//     if(time_cross != 0.0){
//         sources[sc].rays[rc].recs[rec_c].time_cross.push_back(time_cross);
//         sources[sc].rays[rc].recs[rec_c].rad_cross.push_back(rec_radius_current);
//         sources[sc].rays[rc].recs[rec_c].ref_order.push_back(ref_order);
//     }
//     // std::cout << "receiver: " << rec_c << ", time cross is: " << time_cross << std::endl;
//     rec_c++;
// }

 */

/* cout plots
// std::cout << "testing ht_length:" << ht_length << std::endl;
// std::cout << "testing allow scaterring:" << allow_scattering << std::endl;
// std::cout << "testing transition order:" << transition_order << std::endl;
// std::cout << "testing source coord:" << sources[0].coord << std::endl;
// std::cout << "testing plane normal:" << planes[0].normal << std::endl;
// std::cout << "testing plane seq before:" << rays[0].planes_hist << std::endl;
// rays[0].planes_hist[1] = 15;
// std::cout << "testing plane seq after:" << sources[0].rays[0].planes_hist << std::endl;
// std::cout << "testing plane seq after:" << rays[1].planes_hist << std::endl;

// std::cout << "testing ref_pts seq after:" << rays[3].refpts_hist << std::endl;
// std::cout << "c0:" << c0 << std::endl;
// std::cout << "rays:" << v_init << std::endl;
// std::vector<double> rays_cpp;
// rays_cpp.push_back(2.2);
// rays_cpp.push_back(4.2);
// rays_cpp.push_back(5.3);
// sources[1].rays[0].recs[0].time_cross.push_back(0.2f);
// sources[1].rays[0].recs[0].time_cross.push_back(0.35f);

 */