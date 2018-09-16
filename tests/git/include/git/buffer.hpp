#ifndef GIT_BUFFER_HPP
#define GIT_BUFFER_HPP

#include <git/memory.hpp>

namespace git {

struct buffer final {
  using handle_type = unique_ptr<git_buf>;
  using pointer = handle_type::pointer;

  // TODO: Handle 'resize' errors, as they invalidate buffer.
  void grow (size_t) noexcept;

  bool is_binary () const noexcept;
  bool has_null () const noexcept;

  void assign (void const*, size_t);

private:
  handle_type handle;
};

} /* namespace git */

#endif /* GIT_BUFFER_HPP */