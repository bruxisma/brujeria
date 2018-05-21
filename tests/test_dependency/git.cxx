#include <Python.h>
#include <git2.h>


namespace git {

void init () { git_libgit2_init(); }

} /* namespace git */

static auto test_git_init (PyObject*, PyObject* args) {
  git::init();
  Py_RETURN_NONE;
}

static PyMethodDef test_git_methods[] = {
  { "test_git_init", test_git_init, METH_VARARGS, nullptr, },
  { }
};

static PyModuleDef test_dependency {
  PyModuleDef_HEAD_INIT,
  "git",
  nullptr,
  -1,
  test_git_methods
};

PyMODINIT_FUNC PyInit_test_dependency () {
  return PyModule_Create(&test_dependency);
}