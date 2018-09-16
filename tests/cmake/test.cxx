#include <sstream>
#include <memory>
#include <ciso646>

//#include "error.hpp"
#include <git/repository.hpp>

#include <Python.h>
#include "structmember.h"

namespace git {

void init () { git_libgit2_init(); }

} /* namespace git */

struct retain_ptr {
  auto get () const noexcept { return this->ptr; }
private:
  T* ptr;
};

template <> std::string to (cobra::unicode const& str) {
  cobra::ssize_t size { };
  auto ptr = PyUnicode_AsUTF8AndSize(str.get(), &size);
  return { ptr, size };
}

template <> std::string_view to (cobra::unicode const& str) {
  cobra::size_t size { };
  auto ptr = PyUnicode_AsUTF8AndSize(str.get(), &size);
  return { ptr, size };
}

struct Custom : PyObject {
  // Default initializers WOO!
  // What we really want is a throwing default constructor, however.
  retain_ptr<PyObject> first = PyUnicode_FromString("");
  retain_ptr<PyObject> last = PyUnicode_FromString("");
  int number { };

  static int init (Custom* self, PyObject* args, PyObject* kwargs) {
    auto params = parameters { self->first, self->last, self->number };
    auto keys = keywords { "first", "last", "number" };
    auto converter = [] (PyObject* obj, void* handle) {
      auto&& handle = *static_cast<handle_type*>(handle);
      handle.reset(obj);
    };
    auto parser = ArgumentParser(args, kwargs, "|O&O&i");
    auto result = parser(params, keys)
    return 0;
  }
  // alternatively make this a special methods<T, N> type that wraps std::array
  // and has a deduction guide to N + 1 the array so we don't have to manually
  // declare the sentinel.
  // This also gives us the opportunity to have an automatic decay to T* for
  // PyMethodDef, so it can *just* be passed to `tp_methods` directly.
  // The actual names need to be figured out.
  static inline auto methods = methods {
    method("name", "Return full name") = [] (handle self) {
      if (not self->first) { return error(PyExc_AttributeError, "first"); }
      if (not self->last) { return error(PyExc_AttributeError, "last"); }
      return format("{} {}", self->first, self->last); // cobra::format -> cobra::unicode
    }
  };

  static inline auto members = members {
    readonly(&Custom::first, "first name"),
    readonly(&Custom::last, "last name"),
    member(&Custom::number, "custom number")
  };

  static inline auto properties = properties {
    property { "number", &Custom::get_number, &Custom::set_number },
    get { "last" } = [] (PyObject* obj, void*) {
      auto self = static_cast<Custom*>(obj);
      return retain_ptr(self->last).release();
    }
  };

};

template <class T>
auto decrement (T* ptr) { Py_DECREF(ptr); return nullptr; }

template <class T>
auto initialize (PyObject* self, PyObject* args, PyObject* kwargs) {
  return T::init(static_cast<T*>(self), args, kwargs);
}

template <class T, enable_if_t<DerivedFrom<T, PyObject>>
auto as (PyObject* self) noexcept { return static_cast<T*>(self); }

namespace user {

// TODO: This is an 'int' on MSVC/Windows
template <class T>
std::ptrdiff_t offset (T) noexcept {
  static_assert(sizeof(member) == sizeof(ptrdiff_t));
  static_assert(std::is_member_object_pointer_v<T>);
  std::ptrdiff_t a { };
  std::memcpy(&a, &member, sizeof(member));
  return a;
}

template <class T, bool read=false>
auto member_impl (T member, char const* doc) noexcept {
  return PyMemberDef {
    ctti::nameof_v<T>,
    type_tag<class_of_t<T>>,
    offset(member),
    int(read), 
    doc
  };
}

template <class T>
auto readonly (T member, char const* doc = "") noexcept {
  return member_impl<T, true>();
}

template <class T>
auto member (T member, char const* doc = "") noexcept {
  return member_impl<T>();
}

// XXX For the time being, we won't accept arguments to our __new__. No
// metaclasses for our C++ classes. Although that sounds fascinating...
template <class T>
PyObject* cxx_generic_new (PyTypeObject* type, PyObject*, PyObject*) try {
  return new (type) T { };
} catch (...) { return nullptr; }

template <class T>
void cxx_generic_finalize (PyObject* obj) {
  error::protector scope { };
  std::destroy_at(as<T>(obj));
}

inline void cxx_generic_free (PyObject* obj) {
  PyObject_Free(self);
}

namespace error {

inline auto raise (PyObject* err, char const* msg) {
  PyErr_SetString(err, msg);
  return nullptr;
}

} /* namespace error */

// Current list of protocols:
// collectable -- gc
// iterable -- iterator
// sequence -- list-like
// mapping -- dict-like
// buffer -- data-like
// awaitable -- async, and iterable
// descriptor -- get, set, del
// dynamic -- has a __dict__ object that can be used
// Comparable -- StrictTotallyOrdered, EqualityComparable
// EqualityComparable -- ==, !=
// StrictTotallyOrdered -- >=, <=, >, <
// builtin
// final (sets Py_TPFLAGS_BASETYPE)
//
// callable -- operator ()
// stringify -- str()
// representation -- repr()
// hashable -- hash()
// Attributable -- getattr, setattr

// Standard Layout means we can inherit directly from PyTypeObject and still
// do our thing.
// XXX: Consider using a 'policy' approach. This would help with reducing
//      the chance of breaking std layout. This 'policy', can simply be a
//      tuple of types that are used to initialize the type's various member
//      functions and values.
//      This would actually be doable... keep types like `collectable` clear of
//      inheritance, then have a default function available if necessary.
//      Add this new 'type' to the policy and simply have it as a type alias
//      in class T. (This is extremely doable, and possible!)
//      Call the wrapper<Ts...> class *protocol*
//      Used like struct { protocol<iterable, collectable, sequence> }; etc.
// TODO: rename 'type' to define<T> OR definition<T>
// NOTE: We cannot use virtual functions, but what we *can* do is have a
// retain_ptr or unique_ptr in our CustomObject classes that can point to a
// type we're wrapping. Then, we simply have the static functions, cast and call
// various functions directly through ~~inheritance~~.
// I like this idea.
// NOTE: We need to have the is_detected trait + enough traits to detect all
//       necessary interfaces. Targeting C++20 means we could easily use
//       Concepts for checking.
template <class T>
struct type : PyTypeObject {
  type () :
    PyTypeObject { PyVarObject_HEAD_INIT(nullptr, 0) }, // this seems dangerous...
    tp_name { T::name },
    tp_doc { T::doc },
    tp_basicsize { sizeof(T) },
    tp_itemsize { },
    tp_flags { Py_TPFLAGS_DEFAULT },
    tp_new { cxx_generic_new<T> }, // we don't have a tp_alloc because we can call new
    tp_init { initialize<T> },
    tp_finalize { cxx_generic_finalize<T> }, // this is new in 3.4 and maps to __del__
    tp_dealloc { }, // This needs to be an empty function, I reckon
    tp_free { cxx_generic_free },
    //PyType_GenericAlloc unfortunately uses memset, and that's not safe
    // for our types, as they are standard layout, not trivially copyable.
    // this has to be overriden for all C++ types... which is easy thanks to
    // mixins. On the bright side, tp_alloc is only ever called by us directly
    // So... we can have it be a function that just returns a nullptr, and use
    // operator new instead. That said, I need to figure out the actual
    // allocation needed for such an operation... we might need to do a
    // placement new that takes a type<T>...
    tp_alloc { nullptr }, 
    tp_members { T::members },
    tp_methods { T::methods },
    tp_getset { T::properties },
  // using <concepts>
  { static_assert(std::DerivedFrom<T, type>); }

  static auto get () noexcept {
    static type instance;
    return std::addressof(instance);
  }
};

static PyTypeObject Type = {
  PyVarObject_HEAD_INIT(NULL, 0)
};

} /* namespace user */

/*
PyObject* test_file (PyObject*, PyObject* args) {
  PyObject* obj;
  auto result = PyArg_ParseTuple(args, "O&", PyUnicode_FSDecoder, &obj);
  if (not result) { return nullptr; }
  auto path = PyUnicode_AsUTF8(obj);
  if (not path) { return nullptr; }

  try {
    git::repository repo(path);
  } catch (std::system_error const& e) {
    PyErr_SetString(PyExc_ValueError, e.what());
    return nullptr;
  }
  Py_RETURN_NONE;
}

static PyMethodDef test_methods[] = {
  { "file", test_file, METH_VARARGS, nullptr },
  { }
};

static PyModuleDef test {
  PyModuleDef_HEAD_INIT,
  "test",
  nullptr,
  -1,
  test_methods
};

PyMODINIT_FUNC PyInit_test () {
  git::init();
  auto module = PyModule_Create(&test);
  if (module) {
    auto error = python::exception();
    Py_INCREF(error);
    PyModule_AddObject(module, "BrujeriaError", error);
  }
  return module;
}*/
