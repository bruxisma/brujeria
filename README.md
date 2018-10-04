Overview
========

Brujería is a python library that simplifies development workflow for native
extensions. It does this by providing import hooks that allow you to compile
your extensions on import (much like [cppimport]) so you can play around with
the API in a REPL. Lastly, it provides some hooks so that using these from
tools like [poetry] are just a single line. It does all of this via CMake, but
in a way that you the user will rarely have to write CMake at all.

Features
--------

Currently, Brujería provides the following:

 * `build_cmake_ext` to be used in place of [build_ext]. This does not
   make integration with setuptools easier. It is recommended that users use
   [poetry] for project development.
 * Automatic discovery of C and C++ extensions.
 * The ability to mix C *and* C++ in a single extension (`distutils`/
   `setuptools` do not currently permit this)
 * Optional monkey patching to use logbook over the builtin `distutils.log`
   interfaces, while retaining API compatibility.
 * [PLANNED] SWIG Support
 * [PLANNED] Cython support
 * [PLANNED] Basic [poetry] integration via preprovided `build` function.
 * [PLANNED] `pyproject.toml` integration for configuration settings

Why the name?
-------------

Brujería is a spanish word for "witchcraft". Given the strange, mystic, and
sometimes arcane steps that distutils and setuptools must take when building
native extensions, it only makes sense that a library that takes advantage of
various undocumented hooks might be labelled Black Magic.

Additionally, Brujería has been developed as part of the Occult C++ Initiative,
a set of tools and libraries meant to *demystify* the black magic of C and C++
toolchains, compilers, build systems, and package managers. Brujería is an
important foundation for this initiative.

[build_ext]: https://git.io/vAz6X
[cppimport]: https://github.com/tbenthompson/cppimport
[poetry]: https://poetry.eustace.io
[CMake]: https://cmake.org
