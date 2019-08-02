#include "i_cat.h"

Eigen::MatrixXf intensity_cat(std::vector<Raycpp> &rays,
    Eigen::VectorXf &i_dir, int jrec, int time_size){
    // create the resulting matrix
    Eigen::MatrixXf i_cat(rays[0].recs[0].i_cross.rows(), time_size);
    // direct intensity
    i_cat.col(0) = i_dir;
    // loop through rays
    int colc_i = 1;
    for(auto&& r: rays){
        int n_cols = r.recs[jrec].time_cross.size();
        i_cat.middleCols(colc_i, n_cols) =
            r.recs[jrec].i_cross;
        colc_i += n_cols;
    }
    return i_cat;
}