from conans import ConanFile, CMake, tools
import os
import git


class h5cppConan(ConanFile):
    name = "h5cpp"
    version = "master"
    auto_update = True
    h5cpp_git_url = "https://github.com/ess-dmsc/h5cpp.git"
    
    license = "GPL V2"
    url = "https://github.com/eugenwintersberger/conan-pkg-h5cpp"
    description = "Conan package for the HDF5 C++ wrapper"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],"commit":"ANY"}
    requires = ("Boost/1.62.0@lasote/stable",
                "hdf5/1.10.1@eugenwintersberger/testing",
                "gtest/1.8.0@conan/stable",
                "zlib/1.2.8@conan/stable",
                "bzip2/1.0.6@conan/stable")
    default_options = "shared=True","commit=None"
    generators = "cmake"
    
    def _current_remote_commit(self):
        self.output.info("Trying to get latest commit from remote repository")
        gcmd = git.cmd.Git()
        commit = None
        
        try:
            commit = gcmd.ls_remote(self.h5cpp_git_url,"refs/heads/master").split("\t")[0]
            self.output.info("The current remote master is on: %s" %commit)
        except:
            self.output.info("Failure to determine the current commit from remote")
            
        return commit
    

    def configure(self):

        self.options["Boost"].shared=True
        self.options["hdf5"].shared=True
        self.options["gtest"].shared=True
        self.options["zlib"].shared=True
        self.options["bzip2"].shared=True
        self.options["Boost"].python=False
        
        #if auto_update is active we add the current remote commit to the build options
        if self.auto_update: 
            self.options.commit = self._current_remote_commit()
    

    def source(self):
        #initial clone of the repository
        self.run("git clone https://github.com/ess-dmsc/h5cpp.git")

    def build(self):
        #
        # pull changes from the master branch if necessary
        #
        self.output.info("Pulling changes if required ..")
        self.run("cd h5cpp && git pull")
        
        
        #clone the repository - we need something more elaborate here
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
