#include <algorithm>
#include "ray.h"

void Raycpp::plane_finder(std::vector<Planecpp> &planes,
    Eigen::RowVector3f &ray_origin,
    Eigen::Ref<Eigen::RowVector3f> v_in,
    uint16_t &plane_detected,
    double &dist){
        int pc = 0; // plane counter
        // initialize vector containers for reflection point, plane_detected, etc
        std::vector<Eigen::RowVector3f> ref_pt_vec;
        std::vector<int> plane_detected_vec;
        std::vector<double> dist_vec;
        for(auto&& pl: planes){
                // 1 - It is forbiden to detect the previously detected plane
                if(pc == plane_detected){
                        pc++;
                        continue;
                }
                // 2 - Calculate the reflection point for this plane
                Eigen::RowVector3f ref_pt;
                ref_pt = pl.refpoint3d(ray_origin, v_in);
                // 3 - Protect against difficult geometry
                dist = (ref_pt - ray_origin).norm();
                if(dist < 0.000001 || ref_pt == ray_origin){
                        pc++;
                        continue;
                }
                // 4 - Test this plane (wn = 0 - plane is not a hit)
                int wn = 0;
                wn = pl.test_single_plane(ray_origin, v_in, ref_pt);
                // 5 - if detection is +, append plane to a list of possible planes
                if (wn != 0){
                        ref_pt_vec.push_back(ref_pt);
                        plane_detected_vec.push_back(pc);
                        dist_vec.push_back(dist);
                }
                pc++;
        }
        /* Now that we scanned all the planes, we can determine which is
        the correct intercepted plane. This is the plane for which the
        travel distance from origin to ref_pt is the smallest */
        // 1 - if the vectors have size 1 - single plane detection
        if (plane_detected_vec.size() == 1){
                ray_origin = ref_pt_vec[0];
                plane_detected = plane_detected_vec[0];
                dist = dist_vec[0];
                // std::cout << "single plane detection" << std::endl;
        }
        // 2 - if the vectors have size 0 - no plane detection
        else if (plane_detected_vec.size() == 0){
                ray_origin << 2.3, 2.3,2.3; //ray_origin + 50 * v_in;
                plane_detected = -1;
                dist = 10000000.0;
                // std::cout << "no plane detection" << std::endl;
        }
        // 3 - multiple planes detection (find the closest one)
        else {
                int min_id = std::min_element(dist_vec.begin(), dist_vec.end())
                        - dist_vec.begin(); // index of the minimum distance
                ray_origin = ref_pt_vec[min_id];
                plane_detected = plane_detected_vec[min_id];
                dist = dist_vec[min_id];
                // std::cout << "multiple plane detection" << std::endl;
        }
        // int plane_id = -1;
        //ray_origin << 0.3, 0.3, 0.3;
        // return plane_id;

}