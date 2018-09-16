#ifndef GIT_REFDB_HPP
#define GIT_REFDB_HPP

#include <git/repository.hpp>

namespace git {

struct refdb final : unique<git_refdb> {
  refdb (repository const&);

  void compress ();
};

} /* namespace git */

#endif /* GIT_REFDB_HPP */