#ifndef GIT_OBJECT_HPP
#define GIT_OBJECT_HPP

#include <git/memory.hpp>
#include <string_view>

namespace git {

enum class object_type {
  any = GIT_OBJ_ANY,
  bad = GIT_OBJ_BAD,
  commit = GIT_OBJ_COMMIT,
  tree = GIT_OBJ_TREE,
  blob = GIT_OBJ_BLOB,
  tag = GIT_OBJ_TAG,
  offset_delta = GIT_OBJ_OFS_DELTA,
  id_delta = GIT_OBJ_REF_DELTA
};

std::string_view to_string (object_type) noexcept;
object_type to_type (std::string) noexcept;
bool is_loose (object_type) noexcept;

struct object {
  using handle_type = unique_ptr<git_object>;
  using pointer = handle_type::pointer;

  void swap (object&) noexcept;

  explicit operator bool () const noexcept;
  pointer get () const noexcept;

  object_type type () const noexcept;

private:
  handle_type handle;
};

void swap (object&, object&) noexcept;

} /* namespace git */


#endif /* GIT_OBJECT_HPP */