cmake_minimum_required(VERSION 2.8.12)
project(yender)

add_subdirectory(pybind11)
pybind11_add_module(renderer_impl src/renderer_impl.cpp)
