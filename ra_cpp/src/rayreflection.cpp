#include "rayreflection.h"

std::random_device rd{};
std:: mt19937 engine{ rd() };
std::uniform_real_distribution<double> dist{ 0.0,1.0 };
#define M_PI 3.14159265358979323846 //Pi


Eigen::RowVector3f rayreflection(Eigen::Ref<Eigen::RowVector3f> v_in,
    Eigen::Ref<Eigen::RowVector3f> normal,
    double s_s,
    int ref_order,
    int s_on_off,
    int trans_order)
{
    // Chech which normal of the plane to use
    if (v_in.dot(normal) > 0.0) // in this case invert normal
        normal = -normal;
    //std::cout << "normal is (" << normal[0] << "," << normal[1] << ","  << normal[2] << ")" << std::endl;
    // Define a non-scattering condition
    double sort1 = 2.0; // always bigger than scattering coeff
    // Define a scattering condition
    if (s_on_off == 1 && ref_order > trans_order)
        sort1 = dist(engine); // sorted number to compare to s_s
    //std::cout << "sort1 is " << sort1 << std::endl;
    //Define the direction of reflection
    Eigen::RowVector3f v_out;
    //std::cout << "n.v: " << normal.dot(v_in) << std::endl;
    if (sort1 > s_s)
        v_out = v_in - 2.0 * normal.dot(v_in) * normal;
        else {
        // generate 2 random numbers
        double g1 = dist(engine);
        double g2 = dist(engine);
        // get azimuth elevation and norm
        double phi_h = acos(sqrt(g1));
        double phi_v = 2.0 * M_PI * g2;
        //double r = v_in.norm();
        // convert the spherical coord to cartesian
        v_out[0] = cos(phi_v) * cos(phi_h);
        v_out[1] = cos(phi_v) * sin(phi_h);
        v_out[2] = sin(phi_v);
        // ensure the ray goes in the room
        if (normal.dot(v_out) < 0)
            v_out = -v_out;
    }
    // std::cout << "v_out: (" << v_out[0] << "," << v_out[1] << ","  << v_out[2] << ")" << std::endl;
    // std::cout << "v_out norm: " << v_out.norm() << std::endl;
    return v_out;
}