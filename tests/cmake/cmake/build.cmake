include_guard(GLOBAL)

function (sources)
  target_sources(${PROJECT_NAME} PRIVATE ${ARGN})
endfunction()

function (defines)
  target_compile_definitions(${PROJECT_NAME} PRIVATE ${ARGN})
endfunction()

function (options)
  target_compile_options(${PROJECT_NAME} PRIVATE ${ARGN})
endfunction()

function (link)
  target_link_libraries(${PROJECT_NAME} PRIVATE ${ARGN})
endfunction()

function (includes)
  target_include_directories(${PROJECT_NAME} PRIVATE ${ARGN})
endfunction()

function (features)
  target_compile_features(${PROJECT_NAME} PRIVATE ${ARGN})
endfunction()

# TODO: Does this actually work? Should we be a bit more secretive and
# automatically handle cython files added via sources()? That might be the way
# to go, but we do want to support multiple calls to sources. Otherwise, what's
# the point in wrapping the damn function?
# TODO: We need to also do a search for relevant dependencies. Other tools do
# weird things where they regex files and like hell we're going to do that.
# *no thank you*.
function (cython)
  set(_output ${PROJECT_BINARY_DIR}/cython/${basename}.cxx)
  add_custom_command(
    OUTPUT ${_output}
    MAIN_DEPENDENCY ${basename}.pyx
    DEPENDS ${basename}.pxi ${basename}.pxd
    COMMAND cython --cplus -3
      -I$<JOIN:$<TARGET_PROPERTY:${PROJECT_NAME},INCLUDE_DIRECTORIES>,;-I>
      -w "${CMAKE_CURRENT_LIST_DIR}"
      -o ${_output}
      ${basename}.pyx
    COMMAND_EXPAND_LISTS
    VERBATIM
  )
  target_sources(cython-files PUBLIC ${_output})
endfunction()