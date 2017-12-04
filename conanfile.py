from conans import ConanFile, CMake, tools
import os
import git


class h5cppConan(ConanFile):
    name = "h5cpp"
    version = "master"
    auto_update = True
    h5cpp_git_url = "https://github.com/ess-dmsc/h5cpp.git"
    
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "Conan package for the HDF5 C++ wrapper"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],"commit":"ANY"}
    requires = ("Boost/1.62.0@lasote/stable",
                "hdf5/1.10.1@eugenwintersberger/testing",
                "gtest/1.8.0@conan/stable",
                "zlib/1.2.8@conan/stable")
    default_options = "shared=True"
    generators = "cmake"
    
    def _get_local_current_commit(self,repository_path):
        self.output.info("Trying to access repository in: "+repository_path)
        commit = None
        try:
            self.run("cd %s && git pull" %repository_path) 
            repo = git.Repo(repository_path)
            commit = repo.commit().hexsha
            self.output.info("Current commit is: "+commit)
            
        except:
            self.output.info("Could not retrieve current commit of sources")
            
        return commit
    
    def _get_remote_current_commit(self):
        self.output.info("Trying to get latest commit from remote repository")
        gcmd = git.cmd.Git()
        commit = None
        
        try:
            commit = gcmd.ls_remote(self.h5cpp_git_url,"refs/heads/master").split("\t")[0]
            self.output.info("The current remote master is on: %s" %commit)
        except:
            self.output.info("Failure to determine the current commit from remote")
            
        return commit
    
    def _get_current_commit(self):
        #we pull here the repository and add the commit to the build options. 
        #if the commit has changed the hash of the build configuration will change
        #and thus force a rebuild of the package
        
        
        current_commit = None
        self.output.info("Checking the GIT commit")       
        source_path =  os.path.join(self.conanfile_directory,"..","source","h5cpp")
        
        if os.path.exists(source_path):
            current_commit = self._get_local_current_commit(source_path)
        else:
            current_commit = self._get_remote_current_commit()
            
        return current_commit
    
    def _set_commit_option(self):
        current_commit = self._get_current_commit()
        if current_commit != None:
            #if we can obtain the actual commit of the repository we can do something with it
            self.options.commit = current_commit
    
    

    def configure(self):

        self.options["Boost"].shared=True
        self.options["hdf5"].shared=True
        self.options["gtest"].shared=True
        
        if self.auto_update: self._set_commit_option()
        
    

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
