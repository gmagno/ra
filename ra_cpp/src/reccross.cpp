#include "reccross.h"
// Method to retrieve a sequence of Reflection coefficients
Eigen::MatrixXf RecCrosscpp::reflection_coeff_hist(
    RowVectorXui &planes_hist,
    Eigen::MatrixXf &refcoeff, int freq_size){
    Eigen::MatrixXf refcoeff_hist(freq_size, planes_hist.size());
    refcoeff_hist = refcoeff(Eigen::all, planes_hist);
    return refcoeff_hist;
}

// Method to calculate the cumulative product of reflection coefficients
Eigen::MatrixXf RecCrosscpp::cum_prod(Eigen::MatrixXf &refcoeff_hist){
    // allocate memory to calculate the cumulative product
    Eigen::MatrixXf refcoeff_cumprod(refcoeff_hist.rows(), ref_order.size());
    // scan through reflection orders to perform prods
    int roc = 0;
    for(auto&& ro: ref_order){
        refcoeff_cumprod.col(roc) =
        refcoeff_hist(Eigen::all,
        Eigen::seq(0,ref_order[roc]-1)).rowwise().prod();
        roc++;
    }
    return refcoeff_cumprod;
}

// Method to calculate sound intensity at direct sound
Eigen::MatrixXf RecCrosscpp::intensity_ref(
    Eigen::RowVectorXf power_lin,
    int Nr, double c0,
    Eigen::RowVectorXf m_s,
    Eigen::MatrixXf &refcoeff_cumprod){
    // sound power / Nrays
    power_lin = power_lin.array() / float(Nr);

    // allocate memory to calculate intensity
    Eigen::MatrixXf i_cross(refcoeff_cumprod.rows(), refcoeff_cumprod.cols());

    // get rad_cross in an eigen array
    Eigen::RowVectorXf radius_cross =
        Eigen::RowVectorXf::Map(rad_cross.data(), rad_cross.size());

    // get time_cross in an eigen array
    Eigen::RowVectorXf t_cross =
        Eigen::RowVectorXf::Map(time_cross.data(), time_cross.size());
    t_cross = t_cross * c0; // cumulative distance

    // 1 / (pi*rec radius^2)
    radius_cross = M_PI * radius_cross.array().pow(2.0);
    radius_cross = radius_cross.array().inverse();

    // // power - radius matrix
    // Eigen::MatrixXf pr_mtx(refcoeff_cumprod.rows(), refcoeff_cumprod.cols());
    // pr_mtx = power_lin.transpose() * radius_cross;

    // air absorption term: exp(-m_s * c0 * time_cross)
    Eigen::MatrixXf ms_mtx(refcoeff_cumprod.rows(), refcoeff_cumprod.cols());
    ms_mtx = -m_s.transpose() * t_cross;
    ms_mtx = ms_mtx.array().exp();

    // calculate intensity
    i_cross = (refcoeff_cumprod.array() * ms_mtx.array() *
    (power_lin.transpose() * radius_cross).array());

    // std::cout << "first i results: " << std::endl <<
    // i_cross(Eigen::all, Eigen::seq(0,3)) << std::endl;
    return i_cross;
}
/* cumprod_mine
//fake stuff to test
    // std::vector<int> rord_fake;
    // rord_fake.push_back(1);
    // rord_fake.push_back(2);
    // rord_fake.push_back(3);
// refcoeff_hist(Eigen::all, Eigen::seq(0,2)).rowwise().prod();
    // std::cout << refcoeff_hist(Eigen::all, Eigen::seq(0,2)).rowwise().prod() << std::endl;
*/
/*
//fake stuff to test
    // std::vector<int> rord_fake;
    // rord_fake.push_back(1);
    // rord_fake.push_back(2);
    // rord_fake.push_back(3);

    // // Create a tensor of 2 dimensions
    // Eigen::Tensor<int, 2> a(2, 3);
    // a.setValues({{1, 2, 3}, {4, 5, 6}});
    // // Scan it along the second dimension (1) using summation
    // Eigen::Tensor<int, 2> b = a.cumsum(1);
    // // The result is a tensor with the same size as the input
    // std::cout << "a" << a << std::endl;
    // std::cout << "b" << b << std::endl;
*/