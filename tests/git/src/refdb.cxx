#include <git/refdb.hpp>

namespace {

auto create (git::repository const& repo) {
  git_refdb* ptr;
  auto result = git::to_code(git_refdb_new(&ptr, repo.get()));
  if (result) { throw std::system_error(result); }
  return ptr;
}

} /* nameless namespace */

namespace git {

refdb::refdb (repository const& repo) : self(::create(repo)) { }

void refdb::compress () { git_refdb_compress(this->get()); }

} /* namespace git */