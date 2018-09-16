include_guard(GLOBAL)

function (cache _var _value _type)
  set(${_var} ${_value} CACHE ${_type} "" FORCE)
endfunction()

function (info)
  message(STATUS ${ARGV})
endfunction()

function(warn)
  message(WARNING ${ARGV})
endfunction()

function (error)
  message(FATAL_ERROR ${ARGV})
endfunction()