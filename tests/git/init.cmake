github(libssh2/libssh2 libssh2-1.8.0)
github(libssh2/libssh2 v0.27.0)
#gitlab(owner/project HEAD)
#git(SSH https://github.com/libssh2/libssh2.git libssh2-1.8.0)
#git(Git https://github.com/libgit2/libgit2.git v0.27.0)

cache(ENABLE_ZLIB_COMPRESSION ON BOOL)
cache(CRYPTO_BACKEND WinCNG STRING)

cache(BUILD_EXAMPLES OFF BOOL)
cache(BUILD_CLAR OFF BOOL)

# Well, this is a PITA :/
cache(USE_SSH OFF BOOL)
cache(LIBSSH2_FOUND TRUE BOOL)
cache(LIBSSH2_LIBRARIES module::SSH STRING)
cache(LIBSSH2_LIBRARY_DIRS $<TARGET_FILE_DIR:module::SSH> STRING)

sources(
  git/repository.cxx
  git/object.cxx
  git/memory.cxx
  git/error.cxx
  git/refdb.cxx
  test.cxx)

features(cxx_std_17)
link(module::Git)
