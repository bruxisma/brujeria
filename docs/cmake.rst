CMake API
=========

This section discusses the CMake API provided by Brujería for user's
:file:`init.cmake` files. These APIs are *very* simplistic, but are simple
enough.

Initialization File
-------------------

Brujería looks for files named :file:`init.cmake` and uses these as so called
*entrypoints* to get information on how to build a native extension. The name
was chosen to coincide with python's naming conventions, however having many
underscores seems weird when its not Python.

Regardless, the initialization file is silo'd from other initialization files.
Brujería *will not* support projects that include other init.cmake files from
the default. While it might be tempting (especially to *import* other modules),
to do so, it is not recommended. Instead, if multiple modules are desired,
initialize them all from one init.cmake, but use the Python C API to manually
add them.

Build Functions
---------------
 
All of these functions are wrappers and automatically add flags to a given
native extension. They are available from within the extension's
:file:`init.cmake`

.. option:: sources(...)

   Takes a list of file sources. Wrapper around ``target_sources``

.. option:: defines(...)

   Takes a list of compiler defines. Wrapper around
   ``target_compile_definitions``

.. option:: options(...)

   Takes a list of compiler options. Wrapper around ``target_compile_options``

.. option:: link(...)

   Takes a list of libraries to link against. Wrapper around
   ``target_link_libraries``

.. option:: includes(...)

   Takes a list of directories. Wrapper around ``target_include_directories``

.. option:: features(...)

   Takes a list of CMake compiler features. Wrapper around
   ``target_compile_features``

Dependency Functions
--------------------

.. option:: git (name, repository, tag)

   Wraps :option:`fetch`, downloads the given ``repository`` at commit ``tag``,
   and then creates an interface target called ``module::${name}``.

.. option:: fetch (name, ...)

   Wrapper around FetchContent, this fetches, includes, and then generates an
   interface target with the name ``module::${name}``. This allows transitive
   properties of dependencies. This requires some form of arguments to fetch
   said content. It does not download, git clone, or subversion checkout
   anything by default.

Utility Functions
-----------------

.. option:: cache(var value type)

   Sets a variable in the CMake cache. Useful for overriding subproject options.

.. option:: info(...)

   Wrapper around ``message``, prints text to stdout

.. option:: warn(...)

   Wrapper around ``message``, prints a warning to stderr

.. option:: error(...)

   Wrapper around ``message``, prints an error to stderr and then halts
   execution.

Example File
------------

The following is an example on how to use these APIs to download and configure
libgit2 and libssh2 as dependencies for a native extension.

.. code-block:: cmake

   git(SSH https://github.com/libssh2/libssh2.git libssh2-1.8.0)
   git(Git https://github.com/libgit2/libgit2.git v0.27.0)

   cache(ENABLE_ZLIB_COMPRESSION ON BOOL)
   if (WIN32)
     cache(CRYPTO_BACKEND WinCNG STRING)
   endif()

   # These values disable unnecessary build targets in Git
   cache(BUILD_EXAMPLES OFF BOOL)
   cache(BUILD_CLAR OFF BOOL)

   # This might seem counter-intuitive, but is needed because of how libgit2
   # searches for libssh2
   cache(USE_SSH OFF BOOL)
   cache(LIBSSH2_FOUND TRUE BOOL)
   cache(LIBSSH2_LIBRARIES module::SSH STRING)
   cache(LIBSSH2_LIBRARY_DIRS $<TARGET_FILE_DIR:module::SSH> STRING)

   includes(${Git_SOURCE_DIR}/include)

   sources(spam.cxx)
   features(cxx_std_17)
   link(module::Git)