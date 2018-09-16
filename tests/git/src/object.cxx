#include <git/object.hpp>

namespace git {

std::string_view to_string (object_type otype) noexcept {
  return git_object_type2string(static_cast<git_otype>(otype));
}

void object::swap (object& that) noexcept {
  using std::swap;
  swap(this->handle, that.handle);
}

object::operator bool () const noexcept { return bool(this->handle); }
object::pointer object::get () const noexcept { return this->handle.get(); }

object_type object::type () const noexcept {
  return object_type(git_object_type(this->get()));
}

void swap (object& lhs, object& rhs) noexcept {
  return lhs.swap(rhs);
}

} /* namespace git */