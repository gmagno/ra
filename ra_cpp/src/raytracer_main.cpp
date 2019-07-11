#include "raytracer_main.h"
#include "rayreflection.h"
#include "do_progress.h"

std::vector<Raycpp> raytracer_main(
    double ht_length,
    int allow_scattering,
    int transition_order,
    std::vector<Sourcecpp> &sources,
    std::vector<Planecpp> &planes,
    double c0,
    Eigen::MatrixXf &v_init,
    std::vector<Raycpp> &rays){
        int N_rays = rays.size();
        int N_max_ref = rays[0].planes_hist.size();
        // std::cout << "Max ref order: " << N_max_ref << std::endl;
        for(auto&& s: sources){
            // std::cout << "testing source coord:" << s.coord << std::endl;
            int rc = 0; // ray counter
            for(auto&& v: rays){
                progress_bar(rc, N_rays);
                uint16_t plane_detected = 65534; // initialize detected plane
                double dist = 0.0; // initialize distance travelled in ray section
                double cum_dist = 0.0; // initialize cumulative distance
                int ref_order = 0; // initialize reflection order
                Eigen::RowVector3f r_origin;
                r_origin = s.coord; // initialize ray origin
                Eigen::RowVector3f v_dir = v_init.row(rc);
                //std::cout << "ray initial direction: " << v_dir << std::endl;
                // std::cout << "test ray origin: " << r_origin << std::endl;
                // while loop
                while(ref_order < N_max_ref){ //  (cum_dist / c0) <= ht_length && 
                    // std::cout << "r_o before: " << r_origin << std::endl;
                    // find the intercepted plane
                    v.plane_finder(planes, r_origin, v_dir, plane_detected, dist);
                    // fill the plane and ref_pts history in appropriate place
                    v.planes_hist[ref_order] = plane_detected;
                    v.refpts_hist.row(ref_order) = r_origin;
                    // stop loop while if no plane is detected
                    if (plane_detected == -1)
                        break; // and after fill a invalid_ray seq
                    //std::cout << "rp from v.refpts_hist: " << v.refpts_hist.row(ref_order) << std::endl;
                    //v.refpts_hist[ref_order](r_origin);
                    // std::cout << "r_o after: " << r_origin << std::endl;
                    // std::cout << "plane detected: " << plane_detected << std::endl;
                    // reflect the ray
                    v_dir = rayreflection(v_dir,
                    planes[plane_detected].normal,
                    planes[plane_detected].s,
                    ref_order, allow_scattering, transition_order);
                    // std::cout << "ray ref direction: " << v_dir << std::endl;

                    // increase reflection order
                    ref_order++;
                    cum_dist += dist;
                }
                // std::cout << "testing ray: " << rc << " plane seq after:" << rays[rc].planes_hist << std::endl;
                // std::cout << "testing ray: " << rc << " r_p seq after:" << rays[rc].refpts_hist << std::endl;
                rc++;
            }
        }
        // std::cout << "testing ht_length:" << ht_length << std::endl;
        // std::cout << "testing allow scaterring:" << allow_scattering << std::endl;
        // std::cout << "testing transition order:" << transition_order << std::endl;
        // std::cout << "testing source coord:" << sources[0].coord << std::endl;
        // std::cout << "testing plane normal:" << planes[0].normal << std::endl;
        // std::cout << "testing plane seq before:" << rays[0].planes_hist << std::endl;
        // rays[0].planes_hist[1] = 15;
        // std::cout << "testing plane seq after:" << rays[0].planes_hist << std::endl;
        // std::cout << "testing plane seq after:" << rays[1].planes_hist << std::endl;

        // std::cout << "testing ref_pts seq after:" << rays[3].refpts_hist << std::endl;
        // std::cout << "c0:" << c0 << std::endl;
        // std::cout << "rays:" << v_init << std::endl;
        // std::vector<double> rays_cpp;
        // rays_cpp.push_back(2.2);
        // rays_cpp.push_back(4.2);
        // rays_cpp.push_back(5.3);
        return rays;
}