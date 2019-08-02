#include "t_cat.h"

std::vector<float> time_cat(std::vector<Raycpp> &rays,
    float time_dir, int jrec){
    // create the result std::vector - initialize time_dir
    std::vector<float> t_cat;//(time_dir);
    t_cat.push_back(time_dir);
    // loop through rays
    for(auto&& r: rays){
        std::move(r.recs[jrec].time_cross.begin(),
            r.recs[jrec].time_cross.end(),
            std::back_inserter(t_cat));
    }
    return t_cat;
}