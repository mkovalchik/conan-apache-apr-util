from conans import ConanFile, CMake
import os


channel = os.getenv("CONAN_CHANNEL", "stable")
username = os.getenv("CONAN_USERNAME", "mkovalchik")


class ApacheaprutilTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "apache-apr-util/1.5.4@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is in "test_package"
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", "bin", "bin")
        self.copy("*.dylib", "bin", "bin")

    def test(self):
        os.chdir("bin")
        self.run(".%sexample" % os.sep)
