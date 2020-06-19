Using Brujería
==============

Using Brujeria with Poetry
--------------------------

As of poetry 1.0, a build script must be mentioned within the
:file:`pyproject.toml` file. When using brujeria, this script must simply
contain the following line of code:

.. code:: python

   from brujeria.poetry import build

This will take care of everything else in the package and users will not need
to do anything further unless additional changes are desired.

Using Brujeria with the REPL
-----------------------------

Brujeria's strength comes from it's `cppimport`-like capabilities, in that the
user can `import` a directory containing an :file:`init.cmake` file, and
brujeria will then attempt to build it as part of a CMake build.

To use this inside of the Python REPL, simply `import brujeria` before
attempting to `import` any dotted paths to an `init.cmake`. Because of
limitations in both the documentation of `importlib` as well as difficulty in
supporting of it, Brujeria does *not* currently support namespace packages.
This is an area of support that might require some additional work.
Contributions are welcome :)
