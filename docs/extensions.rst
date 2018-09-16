Native Extensions
=================

Building native extensions in python is typically considered to be a huge pain.
So much so, that a massive amount of effort has been invested in *not using*
distutils or setuptools to build the extensions. Some of the biggest issues
are the lack of incremental recompilation. In a small one or two file extension
this isn't typically a large issue. However, when projects become many files,
waiting for the entire extension to rebuild isn't much of an option. This also
gets trickier if you are trying to compile dependencies for the native
extension. Additionally, setting compiler flags on a per compiler basis becomes
tricky and before you realize it, your setup.py script has ballooned just to
compile some code.

Brujería attempts to solve this by utilizing CMake under the hood. While CMake
has typically been obtuse, difficult to understand, and wildly unpredictable,
Brujería provides a more minimal interaction, providing several wrappers, and
abstracting away most CMake details so that a developer can focus on writing
code, instead of writing CMake.

By using CMake, Brujería is able to provide an incremental recompilation
development workflow while still acting as though it were distutils or
setuptools running the build. Additionally, a prototyping development workflow
is supported, allowing one to *import* their native extension directly from the
Python REPL. This can be useful for manual testing before unit tests are
written.

In addition to the above, Brujería also automatically provides a way to generate
unit tests for your code via the Catch2 C++ library. Simply writing your unit
tests in your C++ code will be enough for py.test to run them directly, without
having to write test harnesses or run executables via CMake's CTest.

Brujería also provides several utilities for making the python development
workflow a bit better. These are discussed in depth in :doc:`utility`, and it
is recommended that developers at the very least take a quick look to understand
what else Brujería can do.

Incremental Recompilation
-------------------------

The incremental recompilation development workflow is quite simple. When a file
or any of the other files it depends on (such as headers) change, the minimal
set of files are recompiled and then relinked into the extension module. This
saves quite a bit of time when developing, and currently distutils and
setuptools do not support this approach.

Prototyping Imports
-------------------

Integrating changes for a native extension into a python codebase can be long,
arduous, and an overall terrible experience. One must first compile the
extension, and then run tests, or an additional script. Brujería provides an
``importlib`` mechanism to permit importing a native extension directly into a
REPL. This gives one the ability to write small test functions, or to play
around with a native extensions API, without having to touch the rest of a
project.