#include "point_all_recs.h"

// point all receivers to a sound source
void point_all_receivers(
    Eigen::RowVector3f source_coord,
    std::vector<Receivercpp> &receivers){
    // loop through receivers
    for(auto&& r: receivers){
        r.orientation = r.point_to_source(source_coord);
        r.orientation_fig8 = r.point_fig8();
        // std::cout << "orientation: " << r.orientation << std::endl;
    }
}