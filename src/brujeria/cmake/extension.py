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

class Extension:
    def __init__ (self, name):
        self.name = name