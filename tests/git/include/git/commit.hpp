#ifndef GIT_COMMIT_HPP
#define GIT_COMMIT_HPP

#include <git/memory.hpp>
#include <string_view>

namespace git {

struct commit final {
  using handle_type = unique_ptr<git_commit>;
  using pointer = handle_type::pointer;

  void swap (commit&) noexcept;

  explicit operator bool () const noexcept;
  pointer get () const noexcept;

  std::string_view message () const noexcept;
  std::string_view body () const noexcept;

private:
  handle_type handle;
};

void swap (commit&, commit&) noexcept;

} /* namespace git */

#endif /* GIT_COMMIT_HPP */