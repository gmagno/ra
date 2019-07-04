#ifndef BIND_FUN_RAYTRACER_MAIN_H
#define BIND_FUN_RAYTRACER_MAIN_H

#include <iostream>

#include "pybind11/complex.h"
#include "pybind11/eigen.h"
#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"
#include "pybind11/stl.h"
#include "unsupported/Eigen/Polynomials"
#include <vector>
#include "geometry.h"
#include "raytracer_main.h"

namespace py = pybind11;

void bind_fun_raytracer_main(py::module &m);

#endif /* BIND_FUN_RAYTRACER_MAIN_H */