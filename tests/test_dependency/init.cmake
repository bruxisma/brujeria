git(libssh2 https://github.com/libssh2/libssh2.git libssh2-1.8.0)
git(libgit2 https://github.com/libgit2/libgit2.git v0.27.0)

cache(ENABLE_ZLIB_COMPRESSION ON BOOL)
if (WIN32)
  cache(CRYPTO_BACKEND WinCNG STRING)
endif()

cache(BUILD_EXAMPLES OFF BOOL)
cache(BUILD_CLAR OFF BOOL)

# This is currently required to get libgit2 to use our fetched libssh2
cache(USE_SSH OFF BOOL)
cache(LIBSSH2_FOUND TRUE BOOL)
cache(LIBSSH2_INCLUDE_DIRS ${libssh2_SOURCE_DIR}/include PATH)
cache(LIBSSH2_LIBRARIES deps::libssh2 STRING)
cache(LIBSSH2_LIBRARY_DIRS $<TARGET_FILE_DIR:deps::libssh2> STRING)

includes(${libgit2_SOURCE_DIR}/include)
sources(git.cxx)
features(cxx_std_17)
link(deps::libgit2)