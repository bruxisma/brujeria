# List of required variables that brujeria must either pass in, or use as a
# template.
# BRUJERIA_PROJECT_NAME -- This is the name of the module
# BRUJERIA_PYTHON_VERSION -- {sys.version_info.major}{..minor}{..micro}
# BRUJERIA_MODULE_EXTENSION -- An extension, as if built via distutils
# BRUJERIA_MODULE_PATH -- Path to init.cmake file
# BRUJERIA_MACRO_PREFIX -- Prefix to all macro values set in a config header
#
# BRUJERIA_PYTHON_VERSION = '.'.join([str(v) for v in islice(sys.version_info, 0, 3))
# BRUERJIA_PYTHON_PREFIX = sys.prefix
# BRUJERIA_SITE_PACKAGES = distutils.sysconfig.get_python_lib(plat_specific=True)

cmake_minimum_required(VERSION 3.11)
project(${BRUJERIA_PROJECT_NAME})

# TODO: change the value that gets set from the config. This should be something
# that is gotten from pkg_resources by default.
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR}/cmake)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

include(CheckCXXSourceCompiles)
include(CheckCXXSymbolExists)
include(CheckCXXSourceRuns)

include(CheckCSourceCompiles)
include(CheckCCompilerFlag)
include(CheckSymbolExists)

include(CheckIncludeFileCXX)
include(CheckIncludeFile)

include(CheckPrototypeDefinition)

include(CMakePackageConfigHelpers)
include(FetchContent)

# TODO: These should be optional includes, in the event a user overrides default
# module path. It is also why we don't use any of the functions in these files
# for the entire CMakeLists.txt
include(dependency)
include(utility)
include(build)

find_package(PythonInterp REQUIRED ${BRUJERIA_PYTHON_VERSION})
find_package(PythonLibs REQUIRED ${BRUJERIA_PYTHON_VERSION})

# TODO: Place all functions into separate cmake files, then add directories to
# CMAKE_MODULE_PATH at configure time, make part of Config object so users can
# override it.

# We don't want to test or build shared libs unless it's explicitly done.
# This is provided for us by adding 'test' modules and run through a manually
# added catch2 dependency that allows us to "link" pytest and catch2, while
# letting python to act as the test runner
set(BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
set(BUILD_TESTING OFF CACHE BOOL "" FORCE)

add_library(python INTERFACE)
target_link_libraries(python INTERFACE ${PYTHON_LIBRARY})
target_include_directories(python INTERFACE ${PYTHON_INCLUDE_DIRS})
target_compile_definitions(python INTERFACE
  $<$<AND:$<COMPILE_LANGUAGE:CXX>,$<PLATFORM_ID:Windows>,$<CXX_COMPILER_ID:GNU>>:_hypot=hypot>)
target_compile_options(python INTERFACE
  $<$<AND:$<COMPILE_LANGUAGE:CXX>,$<PLATFORM_ID:Windows>,$<CXX_COMPILER_ID:GNU>>:-include cmath>
  $<$<AND:$<CONFIG:Release>,$<CXX_COMPILER_ID:MSVC>>:/GL>)

add_library(${PROJECT_NAME} MODULE)
target_link_libraries(${PROJECT_NAME} PRIVATE python)
set_target_properties(${PROJECT_NAME} PROPERTIES
  PREFIX ""
  SUFFIX ${BRUJERIA_MODULE_EXTENSION})

# Look into generating an additional CMakeLists.txt file so we can add_subdirectory it.
include(${BRUJERIA_MODULE_PATH})