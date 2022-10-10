import os

from conan import ConanFile
from conan.tools.apple import fix_apple_shared_install_name
from conan.tools.cmake import CMake
from conan.tools.files import copy, rmdir, load

required_conan_version = ">=1.50.0"

class Recipe(ConanFile):
    name = "serd"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://drobilla.net/software/serd.html"
    description = "A lightweight C library for RDF syntax"
    topics = "linked-data", "semantic-web", "rdf", "turtle", "trig", "ntriples", "nquads"
    license = "ISC"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    _cmake = None

    exports_sources = "include/*", "src/*", "CMakeLists.txt", "cmake/*"
    generators = ("CMakeDeps", "CMakeToolchain")

    def set_version(self):
        if not hasattr(self, 'version') or self.version is None:
            cmake_file = load(self, os.path.join(self.recipe_folder, "CMakeLists.txt"))
            import re
            self.version = re.search(r"project\([^)]*VERSION\s+(\d+\.\d+.\d+)[^)]*\)", cmake_file).group(1)

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC
        try:
            del self.settings.compiler.libcxx
        except Exception:
            pass
        try:
            del self.settings.compiler.cppstd
        except Exception:
            pass

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.configure()

        return self._cmake

    def build(self):
        self._configure_cmake().build()

    def package(self):
        copy(self, "COPYING", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        self._configure_cmake().install()
        rmdir(self, os.path.join(self.package_folder, "cmake"))
        rmdir(self, os.path.join(self.package_folder, "share"))
        copy(self, "LICENSE", src=self.folders.base_source, dst="licenses")
        fix_apple_shared_install_name(self)

    def package_info(self):
        self.cpp_info.libs = ["serd"]
