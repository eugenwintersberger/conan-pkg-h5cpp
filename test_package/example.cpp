#include <iostream>
#include <h5cpp/hdf5.hpp>

using namespace hdf5;

int main() {

  file::File f = file::create("example.h5",file::AccessFlags::TRUNCATE);
}
