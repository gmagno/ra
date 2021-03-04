#include "t_cat.h"
// Get the time vector for each encounter w/ receiver and concatenate all to a time vector
Eigen::RowVectorXf time_cat(std::vector<Raycpp> &rays,
    float time_dir, int jrec, int time_size){
    // create the result std::vector - initialize time_dir
    Eigen::RowVectorXf t_cat(time_size);//(time_dir);
    t_cat[0] = time_dir;
    // loop through rays
    int colc_i = 1;
    for(auto&& r: rays){
        int n_cols = r.recs[jrec].time_cross.size();
        t_cat.middleCols(colc_i, n_cols) =
            Eigen::RowVectorXf::Map(r.recs[jrec].time_cross.data(),
            r.recs[jrec].time_cross.size());
        colc_i += n_cols;
    }
    return t_cat;
}

// Original - Dynamic alloc
// std::vector<float> time_cat(std::vector<Raycpp> &rays,
//     float time_dir, int jrec){
//     // create the result std::vector - initialize time_dir
//     std::vector<float> t_cat;//(time_dir);
//     t_cat.push_back(time_dir);
//     // loop through rays
//     for(auto&& r: rays){
//         std::move(r.recs[jrec].time_cross.begin(),
//             r.recs[jrec].time_cross.end(),
//             std::back_inserter(t_cat));
//     }
//     return t_cat;
// }

// std vector - known size
// std::vector<float> time_cat(std::vector<Raycpp> &rays,
//     float time_dir, int jrec, int time_size){
//     // create the result std::vector - initialize time_dir
//     std::vector<float> t_cat(time_size);
//     t_cat[0] = time_dir;
//     // loop through rays
//     int colc_i = 1;
//     for(auto&& r: rays){
//         auto first = t_cat.begin() + colc_i;
//         std::copy(r.recs[jrec].time_cross.begin(),
//             r.recs[jrec].time_cross.end(),
//             first);
//         colc_i += r.recs[jrec].time_cross.size();
//     }
//     return t_cat;
// }