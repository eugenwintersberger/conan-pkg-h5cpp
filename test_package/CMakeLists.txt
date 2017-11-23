project(PackageTest CXX)
cmake_minimum_required(VERSION 3.0.0)
set(CMAKE_CXX_STANDARD 11)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(h5cpp REQUIRED)

add_executable(example example.cpp)
target_link_libraries(example h5cpp_shared)

# CTest is a testing tool that can be used to test your project.
enable_testing()
add_test(NAME example
	  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
	  COMMAND example)
