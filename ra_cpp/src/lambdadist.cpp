#include "lambdadist.h" 

py::array_t<double> lambdadist(Eigen::Ref<Eigen::RowVector3d> ray_origin, 
        Eigen::Ref<Eigen::RowVector3d> v_in,
        Eigen::Ref<Eigen::RowVector3d> ref_point)

    
{
        
    // Calculate lambda - it tell us if the ray goes towards the plane (>0) or not
    double lambda = v_in.dot(ref_point) - v_in.dot(ray_origin);
    // Calculate the distance from ray_origin to ref_point
    double distance = (ref_point - ray_origin).norm();

    // double * result = new double[2];

    size_t size = 2;
    double *data = new double[size]{}; // <-- initialize with zeros
    py::capsule free_when_done(data, [](void *f) {
        double *data = reinterpret_cast<double *>(f);
        delete[] data;
    });

    auto result = py::array_t<
        double,
        py::array::c_style | py::array::forcecast>(
        {1, 2}, // shape
        {
            2 * sizeof(double),
            sizeof(double)}, // C-style contiguous strides for double
        data,                // the data pointer
        free_when_done       // numpy array references this parent
    );
    auto res = result.mutable_unchecked<2>();

    res(0,0) = lambda;
    res(0,1) = distance;
    //std::cout << "lambda is: " << lambda << ", distance is: " << distance << " [m]" << std::endl;

    return result;

  
}