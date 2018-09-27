# TODO: Move these notes to documentation where they belong.
# TODO: Add support for cython modules.
# Configuration values can be set on a per project (the whole setup.py location)
# *or* on a per extension basis. Currently, brujeria does not support settings
# via setup.cfg, otherwise we would be recommending their definition there.
# *however* we should be able to add it into our setuptools monkeypatching.
# Whether it will be *useful* or not is still up in the air.
#
# List of required variables that brujeria must either pass in, or use as a
# template.
# BRUJERIA_PYTHON_VERSION -- {sys.version_info.major}{..minor}{..micro}
# BRUJERIA_MODULE_EXTENSION -- An extension, as if built via distutils
# BRUJERIA_MODULE_PATH -- Path to init.cmake file
#
# BRUERJIA_PYTHON_PREFIX = sys.prefix
#
# Additional variables that we will provide in the brujeria config, that will be
# turned into CMAKE_DEFINED_VARIABLES in the generated file.
# config.compiler.cxx -> gets defined as CMAKE_CXX_COMPILER before running cmake
# config.compiler.cc -> gets defined as CMAKE_C_COMPILER before running cmake
# config.tools.tidy -> Path to clang-tidy
# config.tools.launcher -> Path to compiler launcher (such as ccache or distcc)
# config.tools.cppcheck -> Path to cppcheck executable + args
# config.tools.iwyu -> Path to include-what-you-use tool
# extension.name -> Gets defined as BRUJERIA_PROJECT_NAME (just the basename)
# extension.path -> Directory containing init.cmake, defined as BRUJERIA_MODULE_PATH
#   by default, this is inferred from the extension.name
#   (e.g., given `my.base`, it is defined as ${package_dir}/my/base)
# extension.languages -> List passed to project(), defaults to *just* ['CXX']
# extension.prelude -> File path that gets defined as 
#   `CMAKE_PROJECT_${BRUJERIA_PROJECT_NAME}_INCLUDE`. None by default, and not
#   defined if it is None.
# extension.version -> taken from Distribution.version if not provided
#   passed to VERSION arg in project()
# extension.description -> taken from Distribution.description if not provided 
#   passed to DESCRIPTION arg in project()

# TODO: Starting with CMake 3.12 we don't need some of our stuff here to define
#       We still need to pass in the python version, *and* we need to pass in
#       the module suffix. Unfortunately the Python_add_library command doesn't
#       actually set the correct suffix.

cmake_minimum_required(VERSION 3.12)
project(${BRUJERIA_PROJECT_NAME})

# TODO: We need to just inline these later...
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR}/cmake)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

include(CheckCXXSourceCompiles)
include(CheckCXXSymbolExists)
include(CheckIncludeFileCXX)
include(CheckCXXSourceRuns)
include(CheckIPOSupported)

include(CheckPrototypeDefinition)
include(CheckCSourceCompiles)
include(CheckCCompilerFlag)
include(CheckSymbolExists)
include(CheckIncludeFile)

include(FetchContent)

# TODO: Provide a way to get Catch2, while also providing a small C++ API so
# that a user can automatically add their unit tests to their modules, *or*,
# if they're so inclined, can have their test_modules separate from their
# source modules, much like the current python style way of doing things.

include(dependency)
include(utility)
include(build)

find_package(Python COMPONENTS Development REQUIRED ${BRUJERIA_PYTHON_VERSION})
find_package(Git REQUIRED)

check_ipo_supported(RESULT BRUJERIA_IPO_SUPPORTED)

# We don't want to test or build shared libs unless it's explicitly done.
# This is provided for us by adding 'test' modules and run through a manually
# added catch2 dependency that allows us to "link" pytest and catch2, while
# letting python to act as the test runner
set(BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
set(BUILD_TESTING OFF CACHE BOOL "" FORCE)

# Need to download this, then run a SHA hash against it.
# https://github.com/catchorg/Catch2/releases/download/v2.2.3/catch.hpp

foreach(var IN LISTS
  CMAKE_CXX_SOURCE_FILE_EXTENSIONS
  CMAKE_C_SOURCE_FILE_EXTENSIONS)
  list(APPEND globs "${BRUJERIA_MODULE_PATH}/src/*.${var}")
endforeach()

file(GLOB_RECURSE sources
  CONFIGURE_DEPENDS
  ${globs})

add_library(${PROJECT_NAME} MODULE)
target_compile_definitions(${PROJECT_NAME} PRIVATE
  $<$<AND:$<COMPILE_LANGUAGE:CXX>,$<PLATFORM_ID:Windows>,$<CXX_COMPILER_ID:GNU>>:_hypot=hypot>)
target_compile_options(${PROJECT_NAME} PRIVATE
  $<$<AND:$<COMPILE_LANGUAGE:CXX>,$<PLATFORM_ID:Windows>,$<CXX_COMPILER_ID:MSVC>>:/permissive->
  $<$<AND:$<COMPILE_LANGUAGE:CXX>,$<PLATFORM_ID:Windows>,$<CXX_COMPILER_ID:GNU>>:-include cmath>)
target_include_directories(${PROJECT_NAME} PRIVATE ${BRUJERIA_MODULE_PATH}/include)
target_link_libraries(${PROJECT_NAME} PRIVATE Python::Python)
target_sources(${PROJECT_NAME} PRIVATE ${sources})

set_target_properties(${PROJECT_NAME} PROPERTIES
  INTERPROCEDURAL_OPTIMIZATION ${BRUJERIA_IPO_SUPPORTED}
  SUFFIX ${BRUJERIA_MODULE_EXTENSION}
  PREFIX ""
)

# Look into copying/symlinking init.cmake to a CMakeLists.txt file so we can add_subdirectory it?
include(${BRUJERIA_MODULE_PATH}/init.cmake)
