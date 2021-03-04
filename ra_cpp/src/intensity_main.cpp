#include "intensity_main.h"
//Use the ray-history to compute the sound intensities at a given receiver encounter
std::vector<Sourcecpp> intensity_main(
    double rec_radius_init,
    std::vector<Sourcecpp> &sources,
    double c0,
    Eigen::RowVectorXf m_s,
    Eigen::MatrixXf &alpha_s){
    Eigen::MatrixXf v_ps = 1 - alpha_s.array(); // reflection coeff
    int Nr = sources[0].rays.size(); // number of rays
    // std::cout << "Nr inside intensity_main: " << Nr << std::endl;
    int sc = 0; // source counter
    for(auto&& s: sources){
        std::cout << "Calculating intensities for source: " <<
            sc + 1 << " at: (" << s.coord << ") [m]" << std::endl;
        // Calculate the direct sound intensities
        // int recc = 0; // receiver counter
        for(auto&& rec:s.reccrossdir){
            rec.i_dir = rec.intensity_dir(s.power_lin, Nr, c0,
                rec_radius_init, m_s);
            // std::cout<< "test point 2" << std::endl;
        } // end of direct sound calculation

        // Calculate the reflected sound intensities
        int rayc = 0;
        for(auto&& ray:s.rays){ // loop over rays
            int recc = 0; //receiver counter
            for(auto&& rec_ref:ray.recs){ // loop over receivers
                // 1 - the vp_history
                Eigen::MatrixXf vp_hist;
                // std::cout<< "test point 1, rec: " << recc << std::endl;
                vp_hist = rec_ref.reflection_coeff_hist(
                    s.rays[rayc].planes_hist, v_ps, m_s.size());
                // 2 - cumulative product on vp_hist
                Eigen::MatrixXf vp_cp;
                vp_cp = rec_ref.cum_prod(vp_hist);
                // 3 - calculate intensities
                // s.rays[rayc].recs[recc].i_cross =
                //     s.rays[rayc].recs[recc].intensity_ref(
                //         s.power_lin, Nr, c0, m_s, vp_cp);
                rec_ref.i_cross = rec_ref.intensity_ref(
                    s.power_lin, Nr, c0, m_s, vp_cp);
                recc++;
            } //end recs
        rayc++;
        } //end rays
    } // end sources
    return sources;
}