Overview
========

Brujería is a python library that augments `setuptools`_ `build_ext`_ and
`build_clib`_ by providing abstract interfaces for user defined extension
workflows. In laymen's terms: It makes it easier to hook in a different build
system like `meson`_ or `CMake`_ for your native extensions. Additionally, it
provides a minimal `ninja`_ based build generator, and also provides an import
hook for lazy building and importing of native extensions a-la `cppimport`_,
while still permitting user-defined build systems.

Features
--------

Currently, Brujería provides the following:

 * build_ninja_clib and build_ninja_ext command classes for setuptools' setup
 * LibraryCommand and ExtensionCommand base classes for implementing custom
   command classes
 * import hooks to permit automatic importing and building of C++ extensions
 * Optional monkey patching to use logbook over the builtin distutils.log
   interfaces, while retaining API compatibility.
 * A basic ninja file generator, separate from ``ninja_syntax.py``

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
.. _build_clib: https://git.io/vAz66
.. _meson: https://mesonbuild.com
.. _CMake: https://cmake.org
.. _ninja: https://ninja-build.org
.. _cppimport: https://github.com/tbenthompson/cppimport