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
from functools import partial

def argument (opts, var, value):
    if var is None: return
    opts.append(f'-D{var}={value}')

class Extension:
    def __init__ (self, name):
        self.name = name
        self.path = os.path.join(name.split('.'))
        self.languages = ['CXX']
        self.prelude = None
        self.version = None
        self.description = None
        self.args = []

    def cmake_args (self):
        options = []
        arg = partial(argument, options)

        languages = ';'.join(self.languages)
        arg(f'BRUJERIA_PROJECT_NAME', self.name)
        arg(f'BRUJERIA_MODULE_PATH', self.path)
        arg(f'BRUJERIA_PROJECT_LANGUAGES', languages)

        arg(f'CMAKE_PROJECT_{self.name}_INCLUDE', self.prelude)
        arg(f'BRUJERIA_PROJECT_VERSION', self.version)
        arg(f'BRUJERIA_PROJECT_DESCRIPTION', self.description)
        arg(f'CMAKE_CXX_COMPILER', config.compiler.cxx)
        arg(f'CMAKE_C_COMPILER', config.compiler.cc)
        options.extend(self.args)
        return options
