#include "raytracer_main.h"
#include "rayreflection.h"
#include "do_progress.h"

std::vector<Sourcecpp> raytracer_main(
    double ht_length,
    int allow_scattering,
    int transition_order,
    std::vector<Sourcecpp> &sources,
    std::vector<Receivercpp> &receivers,
    std::vector<Planecpp> &planes,
    double c0,
    Eigen::MatrixXf &v_init){
        int N_rays = sources[0].rays.size();
        int N_max_ref = sources[0].rays[0].planes_hist.size();
        int sc = 1; // source counter
        for(auto&& s: sources){
            // std::cout << "test" << s.rays[0].planes_hist << std::endl;
            std::cout << "Tracing rays for source: " << sc << " at: (" << s.coord << ") [m]" << std::endl;
            int rc = 0; // ray counter
            for(auto&& v: s.rays){
                progress_bar(rc, N_rays);
                uint16_t plane_detected = 65534; // initialize detected plane
                double dist = 0.0; // initialize distance travelled in ray section
                double cum_dist = 0.0; // initialize cumulative distance
                int ref_order = 0; // initialize reflection order
                Eigen::RowVector3f r_origin;
                r_origin = s.coord; // initialize ray origin
                Eigen::RowVector3f v_dir = v_init.row(rc);
                // while loop
                while(ref_order < N_max_ref){ //  (cum_dist / c0) <= ht_length && 
                    // find the intercepted plane
                    v.plane_finder(planes, r_origin, v_dir, plane_detected, dist);
                    // fill the plane and ref_pts history in appropriate place
                    v.planes_hist[ref_order] = plane_detected;
                    v.refpts_hist.row(ref_order) = r_origin;
                    // stop loop while if no plane is detected
                    if (plane_detected == -1)
                        break; // and after fill a invalid_ray seq
                    // reflect the ray
                    v_dir = rayreflection(v_dir,
                    planes[plane_detected].normal,
                    planes[plane_detected].s,
                    ref_order, allow_scattering, transition_order);
                    // increase reflection order
                    ref_order++;
                    cum_dist += dist;
                    // receiver processing
                    // for(auto&& r: receivers){
                    //     std::cout << r.coord << std::endl;
                    // }
                }
                // std::cout << "testing ray: " << rc << " plane seq after:" << rays[rc].planes_hist << std::endl;
                // std::cout << "testing ray: " << rc << " r_p seq after:" << rays[rc].refpts_hist << std::endl;
                rc++; // increase ray counter
            }
            std::cout<< std::endl;
            sc++; // increase source counter
        }
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
        sources[1].rays[0].recs[0].time_cross.push_back(0.2f);
        sources[1].rays[0].recs[0].time_cross.push_back(0.35f);
        return sources;
}