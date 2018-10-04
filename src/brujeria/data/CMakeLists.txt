# TODO: Add support for cython modules.
# TODO: Add support for SWIG modules.
cmake_minimum_required(VERSION 3.12)
project(${BRUJERIA_PROJECT_NAME})

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

set(EITHER_CLANG $<OR:$<CXX_COMPILER_ID:AppleClang>,$<CXX_COMPILER_ID:Clang>>)

add_library(${PROJECT_NAME} MODULE)
target_compile_definitions(${PROJECT_NAME} PRIVATE
  $<$<AND:$<COMPILE_LANGUAGE:CXX>,$<PLATFORM_ID:Windows>,$<CXX_COMPILER_ID:GNU>>:_hypot=hypot>)
target_compile_options(${PROJECT_NAME} PRIVATE
  $<$<AND:$<COMPILE_LANGUAGE:CXX>,$<PLATFORM_ID:Windows>,$<CXX_COMPILER_ID:MSVC>>:/permissive->
  $<$<AND:$<COMPILE_LANGUAGE:CXX>,$<PLATFORM_ID:Windows>,$<CXX_COMPILER_ID:GNU>>:-include cmath>
  $<$<AND:$<COMPILE_LANGUAGE:CXX>,$<CXX_COMPILER_ID:GNU>>:-fdiagnostics-color=always>
  $<$<AND:$<COMPILE_LANGUAGE:CXX>,${EITHER_CLANG}>:-fcolor-diagnostics>)
target_include_directories(${PROJECT_NAME} PRIVATE ${BRUJERIA_MODULE_PATH}/include)
target_link_libraries(${PROJECT_NAME} PRIVATE Python::Python)
target_sources(${PROJECT_NAME} PRIVATE ${sources})

set_target_properties(${PROJECT_NAME} PROPERTIES
  INTERPROCEDURAL_OPTIMIZATION ${BRUJERIA_IPO_SUPPORTED}
  SUFFIX ${BRUJERIA_MODULE_EXTENSION}
  PREFIX "")

# Look into copying/symlinking init.cmake to a CMakeLists.txt file so we can add_subdirectory it?
include(${BRUJERIA_MODULE_PATH}/init.cmake)
