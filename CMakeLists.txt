cmake_minimum_required(VERSION 2.8.12)
project(ra_cpp)

file(GLOB_RECURSE RA_CPP_SOURCES "ra_cpp/src/*.cpp")

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/eigen)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/ra_cpp/include)

# set(PYBIND11_CPP_STANDARD -std=c++14)
set(PYBIND11_CPP_STANDARD -std=c++1y)  # to build on a reference platform (CentOS_5)
set (CMAKE_CXX_FLAGS "-fPIC")
add_subdirectory(pybind11)
pybind11_add_module(ra_cpp "${RA_CPP_SOURCES}")
