from conans import ConanFile, CMake, tools


class h5cppConan(ConanFile):
    name = "h5cpp"
    version = "0.0.4"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "Conan package for the HDF5 C++ wrapper"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    requires = ("Boost/1.62.0@lasote/stable",
                "hdf5/1.10.1@eugenwintersberger/testing",
                "gtest/1.8.0@conan/stable",
                "zlib/1.2.8@conan/stable")
    default_options = "shared=True"
    generators = "cmake"

    def configure(self):

        self.options["Boost"].shared=True
        self.options["hdf5"].shared=True
        self.options["gtest"].shared=True

    def source(self):
        pass

    def build(self):
        #clone the repository - we need something more elaborate here
        self.run("git clone https://github.com/ess-dmsc/h5cpp.git")
        cmake = CMake(self)
        cmake_defs = {}
        cmake_defs["CMAKE_INSTALL_PREFIX"] = self.package_folder
        cmake_defs["CMAKE_BUILD_TYPE"] = self.settings.build_type
        cmake.configure(source_dir="%s/h5cpp" % self.source_folder, 
                defs=cmake_defs)
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s' % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)
        
        cmake.build(target="install")
        
    def package(self):
        pass
    
    def imports(self):
        if self.settings.os=="Windows":
            self.copy("*.dll","bin","bin")

    def package_info(self):
        self.cpp_info.libs = ["h5cpp"]
