#include "raytracer_main.h"

void raytracer_main(
    double ht_length,
    int allow_scattering,
    int transition_order,
    std::vector<Sourcecpp> &sources,
    std::vector<Planecpp> &planes,
    double c0,
    Eigen::MatrixXd &v_init,
    std::vector<Raycpp> &rays){
        for(auto&& s: sources){
            std::cout << "testing source coord:" << s.coord << std::endl;
            for(auto v : v_init.rowwise()){
                std::cout << "testing ray:" << v << std::endl;
            }
        }
        // std::cout << "testing ht_length:" << ht_length << std::endl;
        // std::cout << "testing allow scaterring:" << allow_scattering << std::endl;
        // std::cout << "testing transition order:" << transition_order << std::endl;
        // std::cout << "testing source coord:" << sources[0].coord << std::endl;
        // std::cout << "testing plane normal:" << planes[0].normal << std::endl;
        std::cout << "testing plane seq before:" << rays[0].planes_hist << std::endl;
        rays[0].planes_hist[1] = 15;
        std::cout << "testing plane seq after:" << rays[0].planes_hist << std::endl;
        // std::cout << "c0:" << c0 << std::endl;
        // std::cout << "rays:" << v_init << std::endl;
        // // return 2.3;
}