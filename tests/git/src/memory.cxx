#include <git/memory.hpp>

namespace git {

void deleter::operator() (git_repository* ptr) const noexcept {
  git_repository_free(ptr);
}

void deleter::operator () (git_object* ptr) const noexcept {
  git_object_free(ptr);
}

void deleter::operator () (git_commit* ptr) const noexcept {
  git_commit_free(ptr);
}

void deleter::operator () (git_refdb* ptr) const noexcept {
  git_refdb_free(ptr);
}

void deleter::operator() (git_buf* ptr) const noexcept {
  git_buf_free(ptr);
}

} /* namespace git */