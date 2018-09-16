Overview
========

Brujería is a python library that augments `setuptools`_ and `build_ext`_ by
providing abstract interfaces for user defined extension workflows. In laymen's
terms: It makes it easier to write C and C++ native extensions while improving
the overall workflow by adding incremental recompilation, and better REPL
support (in that one can technically import their extension modules without
having to manually compile anything)

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

.. toctree::
   :maxdepth: 2

   Native Extensions <extensions>
   Using Brujería <usage>
   Build Commands <build>
   Import Hooks <import>
   CMake API <cmake>

.. _setuptools: https://setuptools.readthedocs.io
.. _build_ext: https://git.io/vAz6X
.. _CMake: https://cmake.org
.. _ninja: https://ninja-build.org
