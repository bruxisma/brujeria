Overview
========

Brujería is a python library that augments `setuptools`_ by providing a
`build_ext`_ override to use a CMake based approach, modify logging to use
logbook, and allows a quicker development workflow for native extensions by
permitting the importing of C or C++ native extensions without having to run
setup.py first (much like `cppimport`_).

Features
--------

Currently, Brujería provides the following:

 * ``build_cmake_ext`` to be used in place of `build_ext`_
 * ExtensionCommandMixin base class for implementing custom command classes
 * import hooks to permit automatic importing and building of C++ extensions via
   CMake.
 * Special Extension class and setup function that automatically handle
   finding extensions in a given project, much like setuptools'
   ``find_packages`` function.
 * Optional monkey patching to use logbook over the builtin distutils.log
   interfaces, while retaining API compatibility.
 * Additional build commands for setup.py to simplify a Makefile. (See our
   project's Makefile for a better idea)

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

.. _setuptools: https://setuptools.readthedocs.io
.. _build_ext: https://git.io/vAz6X
.. _CMake: https://cmake.org
.. _cppimport: https://github.com/tbenthompson/cppimport