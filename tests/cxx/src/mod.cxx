#include <Python.h>
#include <cstdio>

PyObject* hello (PyObject*, PyObject*) {
  return PyUnicode_FromString("Hello, CppCon 2017!");
}

static PyMethodDef methods[] = {
  { "hello", hello, METH_NOARGS, nullptr },
  { }
};

static PyModuleDef cxx {
  PyModuleDef_HEAD_INIT,
  "cxx",
  nullptr,
  -1,
  methods
};

PyMODINIT_FUNC PyInit_cxx () { return PyModule_Create(&cxx); }
