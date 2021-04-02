cmake_minimum_required(VERSION 3.18)
cmake_policy(VERSION 3.18)
project(${BRUJERIA_PROJECT_NAME}
  DESCRIPTION "${BRUJERIA_PROJECT_DESCRIPTION}"
  VERSION "${BRUJERIA_PROJECT_VERSION}")

include(CMakePrintHelpers)

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

file(GLOB_RECURSE sources CONFIGURE_DEPENDS ${BRUJERIA_MODULE_PATH}/src/*)

string(CONCAT is-mingw $<AND:
  $<COMPILE_LANG_AND_ID:CXX,GNU>,
  $<PLATFORM_ID:Windows>
>)

Python_add_library(${PROJECT_NAME} MODULE WITH_SOABI)
target_sources(${PROJECT_NAME} PRIVATE ${sources})

target_include_directories(${PROJECT_NAME}
  PRIVATE
    $<BUILD_INTERFACE:${BRUJERIA_MODULE_PATH}/include>)
target_compile_definitions(${PROJECT_NAME} PRIVATE  $<${is-mingw}:_hypot=hypot>)
target_compile_options(${PROJECT_NAME}
  PRIVATE
    $<$<COMPILE_LANG_AND_ID:CXX,MSVC>:/permissive->
    "$<${is-mingw}:-include cmath>"
    $<$<COMPILE_LANG_AND_ID:CXX,GNU>:-fdiagnostic-color=always>
    $<$<COMPILE_LANG_AND_ID:CXX,AppleClang,Clang>:-fcolor-diagnostics>)
target_link_libraries(${PROJECT_NAME} PRIVATE Python::Module)

# TODO: This *could* be turned into a call to
# cmake_language(DEFER DIRECTORY CALL include ${BRUJERIA_MODULE_PATH}/init.cmake)
# but further up and within the template file that is copied over
include(${BRUJERIA_MODULE_PATH}/init.cmake)

# TODO: Add support for cython modules.
# TODO: Add support for SWIG modules.
