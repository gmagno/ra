#include "cos_cat.h"
// Eigen
Eigen::RowVectorXf cos_cat(std::vector<Raycpp> &rays,
    float cos_dir, int jrec, int time_size){
    // create the result std::vector - initialize time_dir
    Eigen::RowVectorXf cos_cat(time_size);//(time_dir);
    cos_cat[0] = cos_dir;
    // loop through rays
    int colc_i = 1;
    for(auto&& r: rays){
        int n_cols = r.recs[jrec].time_cross.size();
        cos_cat.middleCols(colc_i, n_cols) =
            Eigen::RowVectorXf::Map(r.recs[jrec].cos_cross.data(),
            r.recs[jrec].cos_cross.size());
        colc_i += n_cols;
    }
    // std::cout<<"cos test in cos_cat: " << cos_cat << std::endl;
    return cos_cat;
}