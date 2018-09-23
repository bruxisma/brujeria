# This file contains all functions related to fetching dependencies.
# Currently, only git is supported via a wrapper. Additional work is required
# when using fetch
include_guard(GLOBAL)

function (target_directories name)
  cmake_parse_arguments("" "" "" "RELATIVE_PATH" "INTERFACE;PUBLIC;PRIVATE" ${ARGN})
  list(APPEND extensions
    ${CMAKE_CXX_SOURCE_FILE_EXTENSIONS}
    ${CMAKE_C_SOURCE_FILE_EXTENSIONS})
  foreach(directory IN LISTS _INTERFACE)
    foreach(extension IN LISTS extensions)
      list(APPEND globs "${directory}/*${extension}")
    endforeach()
    file(GLOB_RECURSE interface
      RELATIVE_PATH ${_RELATIVE_PATH}
      CONFIGURE_DEPENDS
      ${globs})
    target_sources(${name} INTERFACE ${interface})
  endforeach()
  
endfunction()

function (glob_sources directory)
  foreach(var IN LISTS
    CMAKE_CXX_SOURCE_FILE_EXTENSIONS
    CMAKE_C_SOURCE_FILE_EXTENSIONS)
    list(APPEND globs "${directory}/*${var}")
  endforeach()
  file(GLOB_RECURSE sources
    RELATIVE ${BRUJERIA_MODULE_PATH}
    CONFIGURE_DEPENDS
    ${globs})
  target_sources(${PROJECT_NAME} PRIVATE ${sources})
endfunction()

# TODO: Replace logic elsewhere with this...
function (FetchContent name)
  FetchContent_Declare(${name} ${ARGN})
  FetchContent_GetProperties(${name})
  if (${name}_POPULATED)
    return()
  endif()
  FetchContent_Populate(${name})
  string(TOLOWER ${name} lcname)
  set(source ${lcname}_SOURCE_DIR)
  set(binary ${lcname}_BINARY_DIR)
  add_subdirectory(${source} ${binary} EXCLUDE_FROM_ALL)
endfunction()

function (_get_targets _var _path)
  get_property(_subdirs DIRECTORY ${_path} PROPERTY SUBDIRECTORIES)
  foreach (_subdir IN LISTS _subdirs)
    _get_targets(${_var} ${_subdir})
  endforeach()
  get_property(_targets DIRECTORY ${_path} PROPERTY BUILDSYSTEM_TARGETS)
  foreach (_target IN LISTS _targets)
    get_target_property(_type ${_target} TYPE)
    if(_type STREQUAL STATIC_LIBRARY OR _type STREQUAL INTERFACE_LIBRARY)
      list(APPEND ${_var} ${_target})
    endif()
  endforeach()
  set(${_var} ${${_var}} PARENT_SCOPE)
endfunction()

function (git _name _repository _tag)
  fetch(${_name}
    GIT_REPOSITORY ${_repository}
    GIT_TAG ${_tag}
    GIT_SHALLOW ON
    ${ARGN})
  set(${_name}_SOURCE_DIR ${${_name}_SOURCE_DIR} PARENT_SCOPE)
endfunction ()

function (github _repository _tag)
  get_filename_component(name ${_repository} NAME)
  git(${name} "https://github.com/${_repository}.git" ${_tag})
  set(${name}_SOURCE_DIR ${${name}_SOURCE_DIR} PARENT_SCOPE)
endfunction ()

function (fetch _name)
  FetchContent_Declare(${_name} ${ARGN})
  FetchContent_GetProperties(${_name})
  string(TOLOWER ${_name} _lcname)
  if (NOT ${_lcname}_POPULATED)
    FetchContent_Populate(${_name})
    set(_srcdir ${${_lcname}_SOURCE_DIR})
    set(_bindir ${${_lcname}_BINARY_DIR})
    add_subdirectory(${_srcdir} ${_bindir} EXCLUDE_FROM_ALL)
  endif ()
  add_library(module::${_name} INTERFACE IMPORTED GLOBAL)
  _get_targets(_deps ${_srcdir})
  target_link_libraries(module::${_name} INTERFACE ${_deps})
  target_include_directories(module::${_name}
    INTERFACE ${_srcdir}/include)
  foreach(_dep IN LISTS _deps)
    target_include_directories(module::${_name} INTERFACE
      $<TARGET_PROPERTY:${_dep},INTERFACE_INCLUDE_DIRECTORIES>)
  endforeach()
  # TODO: Make sure Upper/Lower works correctly...
  # to have the same case because FetchContent turns everything into a lcName
  set(${_name}_SOURCE_DIR ${_srcdir} PARENT_SCOPE)
endfunction ()

