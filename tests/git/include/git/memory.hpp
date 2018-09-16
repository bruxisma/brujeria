#ifndef GIT_MEMORY_HPP
#define GIT_MEMORY_HPP

#include <memory>
#include <git2.h>

namespace git {

struct deleter {
  void operator () (git_repository*) const noexcept;
  void operator () (git_object*) const noexcept;
  void operator () (git_commit*) const noexcept;
  void operator () (git_refdb*) const noexcept;
  void operator () (git_buf*) const noexcept;
};

template <class T>
using unique_ptr = std::unique_ptr<T, deleter>;

template <class T>
struct unique {
  using handle_type = unique_ptr<T>;
  using pointer = typename handle_type::pointer;
  using self = unique;

  void swap (unique& that) {
    using std::swap;
    swap(this->handle, that.handle);
  }

  explicit operator bool () const noexcept { return bool(this->handle); }
  pointer get () const noexcept { return this->handle.get(); }

protected:
  unique (pointer ptr) noexcept : handle(ptr) { }
  unique () = default;

  handle_type handle;
};

template <class T>
void swap (unique<T>& lhs, unique<T>& rhs) noexcept { lhs.swap(rhs); }

} /* namespace git */

#endif /* GIT_MEMORY_HPP */