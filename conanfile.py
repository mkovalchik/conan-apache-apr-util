from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os

class ApacheaprutilConan(ConanFile):
    name = "apache-apr-util"
    version = "1.5.4"
    license = "Apache-2.0"
    url = "https://github.com/mkovalchik/conan-apache-apr-util"
    settings = "os", "compiler", "build_type", "arch"
    requires = "apache-apr/1.5.2@mkovalchik/stable"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    lib_name = name + "-" + version

    def source(self):
        file_ext = ".tar.gz" if not self.settings.os == "Windows" else "-win32-src.zip"
        tools.download("https://www.apache.org/dyn/mirrors/mirrors.cgi?action=download&filename=apr/apr-util-" + self.version + file_ext, self.lib_name + file_ext)
        tools.unzip(self.lib_name + file_ext)

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        with tools.environment_append(env_build.vars):
            configure_command = "./configure"
            if self.settings.os == "Windows":
                configure_command += ".bat"

            configure_command += " --prefix=" + os.getcwd()
            configure_command += " --with-apr=" + self.deps_cpp_info["apache-apr"].rootpath

            with tools.chdir("apr-util-" + self.version):
                self.run(configure_command)
                self.run("make -j " + str(max(tools.cpu_count() - 1, 1)))
                self.run("make install")

    def package(self):
        self.copy("*.so*", dst="lib", src="lib", keep_path=False)
        self.copy("*.a", dst="lib", src="lib", keep_path=False)
        self.copy("*.h", dst="include", src="include", keep_path=True)
        self.copy("apr-1-config", dst="bin", src="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = ["include", "include/apr-1"]
        self.cpp_info.bindirs = ["bin"]
        self.cpp_info.libs = ["aprutil-1"]
