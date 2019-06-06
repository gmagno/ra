#include "ptinpol.h"
#include "isleft.h"

int ptinpol(Eigen::Ref<Eigen::RowVectorXd> vert_x,
        Eigen::Ref<Eigen::RowVectorXd> vert_y, 
        Eigen::Ref<Eigen::RowVector2d> ref_point2d)
{        
    
    int Nvert = vert_x.cols()-1; // Get the number of rows
    int wn = 0; // start the winding number counter
    
    Eigen::RowVectorXd vy_refpy = vert_y.array() - ref_point2d(1);
    
    double isl = 0.0;

    for (int jv = 0; jv < Nvert; jv++) {
        if (vy_refpy(jv) <= 0.0) {
            if (vy_refpy(jv+1) > 0.0)
                if (isleft(vert_x.segment(jv,2), vert_y.segment(jv,2),
                        ref_point2d) > 0.0)
                                ++wn;       
        }
        else {
            if (vy_refpy(jv+1) <= 0.0)
                if (isleft(vert_x.segment(jv,2), vert_y.segment(jv,2),
                        ref_point2d) < 0.0)
                                --wn;    
        }
    
    }    
    //std::cout << isleft(1.0, 2.0, -0.5, 0.3, ref_point2d) << std::endl;
    //std::cout << "lambda is: " << lambda << ", distance is: " << distance << " [m]" << std::endl;

    return wn;

}