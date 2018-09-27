# Given a `name`, this class will search for it amongst all packages
# using the same logic used by the BrujeriaExtensionFinder. (i.e., it looks
# for an init.cmake file in a module with the given name)
# This is then run through the same build steps as if a user had imported the
# init.cmake file.
# init.cmake files are pre-configured files that are add_subdirectory'd via
# a generated CMakeLists.txt. These have a simplified syntax, as there is only
# one target available or event expected. These functions provided are:
# includes -- target_include_directories
# sources -- target_sources
# link -- target_link_libraries
# defines -- target_compile_definitions
# features -- target_compile_features
# options -- target_compile_options (added only if compiler supports it)
#
# Additionally, several other functions are provided for working with
# dependencies:
# fetch -- wrapper around FetchContent
# git -- wrapper around fetch to use git specifically
#
# Dependencies found this way *must* be compiled as static libraries, and
# will be placed into an INTERFACE library, such that the name is
# `deps::<dependency>`, even if that is not the name of a library exported
# during the configure step of these dependencies.
#
# Lastly, several additional functions are provided to reduce boilerplate when
# configuring dependencies or even the build itself, as well as for debugging
# output:
#
# cache(<var> <value> <type>) -- set cache variable
# info -- message(STATUS)
# warn -- message(WARNING)
# error -- message(FATAL_ERROR)
#
# Additional functions may be added at a later time.
import os
from ..core.config import config
from ..core.xdg import CACHE_HOME
from functools import partial
from pkg_resources import resource_filename
from distutils import sysconfig
from subprocess import run
from cmake import CMAKE_BIN_DIR

CMAKE_PRG = os.path.join(CMAKE_BIN_DIR, 'cmake')

def argument (opts, var, value):
    if var is None: return
    opts.append(f'-D{var}={value}')

class Extension:
    def __init__ (self, name, init):
        self.name = name
        self.path = init.parent
        self.languages = ['C', 'CXX']
        self.prelude = None
        self.version = None
        self.description = None
        self.dst = CACHE_HOME / 'brujeria' / self.name
        cmake_src = '-H{}'.format(resource_filename('brujeria', 'data'))
        cmake_dst = '-B{}'.format(self.dst)
        self.args = ['-G', 'Ninja', cmake_src, cmake_dst]
        self.suffix = sysconfig.get_config_var('EXT_SUFFIX') 
        self.output = '{}/{}{}'.format(self.dst, self.name, self.suffix)

    def build (self):
        run([CMAKE_PRG, '--build', os.fspath(self.dst)]).check_returncode()

    def configure (self):
        if os.path.exists(self.dst): return
        options = []
        arg = partial(argument, options)

        languages = ';'.join(self.languages)
        arg(f'BRUJERIA_PROJECT_NAME', self.name)
        arg(f'BRUJERIA_MODULE_PATH', self.path.as_posix())
        #arg(f'BRUJERIA_PROJECT_LANGUAGES', languages)
        arg('BRUJERIA_MODULE_EXTENSION', self.suffix)

        #arg(f'CMAKE_PROJECT_{self.name}_INCLUDE', self.prelude)
        #arg(f'BRUJERIA_PROJECT_VERSION', self.version)
        #arg(f'BRUJERIA_PROJECT_DESCRIPTION', self.description)
        #arg(f'CMAKE_CXX_COMPILER', config.compiler.cxx)
        #arg(f'CMAKE_C_COMPILER', config.compiler.cc)
        options.extend(self.args)
        run([CMAKE_PRG, *options]).check_returncode()
        
