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