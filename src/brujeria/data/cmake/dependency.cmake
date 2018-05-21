# This file contains all functions related to fetching dependencies.
# Currently, only git is supported via a wrapper. Additional work is required
# when using fetch
include_guard(GLOBAL)

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
endfunction ()

function (fetch _name)
  FetchContent_Declare(${_name} ${ARGN})
  FetchContent_GetProperties(${_name})
  if (NOT ${_name}_POPULATED)
    FetchContent_Populate(${_name})
    add_subdirectory(${${_name}_SOURCE_DIR} ${${_name}_BINARY_DIR} EXCLUDE_FROM_ALL)
  endif ()
  add_library(deps::${_name} INTERFACE IMPORTED GLOBAL)
  _get_targets(_deps ${${_name}_SOURCE_DIR})
  target_link_libraries(deps::${_name} INTERFACE ${_deps})
  foreach(_dep IN LISTS _deps)
    target_include_directories(deps::${_name} INTERFACE
      $<TARGET_PROPERTY:${_dep},INTERFACE_INCLUDE_DIRECTORIES>)
  endforeach()
endfunction ()

