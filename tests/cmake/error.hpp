#ifndef TEST_ERROR_HPP
#define TEST_ERROR_HPP

#include <Python.h>
#include <stdexcept>

namespace python {

inline PyObject* exception () noexcept {
  static PyObject* exc = PyErr_NewException("test.BrujeriaError", nullptr, nullptr);
  return exc;
}

inline void* raise (std::exception const& e) {
  PyErr_SetString(exception(), e.what());
  return nullptr;
}

} /* namespace python */

#endif /* TEST_ERROR_HPP */