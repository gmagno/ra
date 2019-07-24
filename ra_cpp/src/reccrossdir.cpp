#include "reccrossdir.h"

Eigen::VectorXf RecCrossDircpp::intensity_dir(
    Eigen::RowVectorXf power_lin,
    int Nr, double c0,
    double rec_radius_init,
    Eigen::RowVectorXf m_s){
    // allocate memory for intensity calculation
    Eigen::VectorXf i_dir(m_s.size());
    // Eigen::VectorXf m_sexp(m_s.size());
    float dist_dir = time_dir * c0;
    m_s = -m_s * time_dir * c0;
    i_dir = (power_lin.array() / float(Nr)) *
        (1/(M_PI * pow(rec_radius_init, 2.0))) *
        m_s.array().exp();
    // std::cout << "i_dir in c++: " << i_dir << std::endl;
    // this->i_dir;
    return i_dir;
}