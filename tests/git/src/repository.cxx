#include <git/repository.hpp>
#include <git/error.hpp>

namespace git {

repository::repository (std::string path) {
  pointer ptr;
  auto result = to_code(git_repository_open(&ptr, path.data()));
  if (result) { throw std::system_error(result); }
  this->handle.reset(ptr);
}

repository::repository (pointer ptr) noexcept :
  handle { ptr }
{ }

repository repository::init (std::string path, bare is_bare) {
  pointer ptr = nullptr;
  auto result = to_code(git_repository_init(&ptr, path.data(), bool(is_bare)));
  if (result) { throw std::system_error(result); }
  return repository(ptr);
}

repository repository::init (std::string path) {
  return init(std::move(path), bare::no);
}

void repository::swap (repository& that) noexcept {
  using std::swap;
  swap(this->handle, that.handle);
}

repository::operator bool () const noexcept { return bool(this->handle); }

repository::pointer repository::get () const noexcept {
  return this->handle.get();
}

std::error_code repository::add_ignore_rule(char const* rules) noexcept {
  return to_code(git_ignore_add_rule(this->get(), rules));
}

std::error_code repository::clear_rules () noexcept {
  return to_code(git_ignore_clear_internal_rules(this->get()));
}

bool repository::is_ignored (char const* path) const noexcept {
  int ignored { };
  git_ignore_path_is_ignored(&ignored, this->get(), path);
  return ignored;
}

std::string_view repository::current_namespace () const noexcept {
  return git_repository_get_namespace(this->get());
}

std::string_view repository::username () const noexcept {
  char const* name = nullptr;
  git_repository_ident(&name, nullptr, this->get());
  return name;
}

std::string_view repository::email () const noexcept {
  char const* email = nullptr;
  git_repository_ident(nullptr, &email, this->get());
  return email;
}

std::string_view repository::working_directory () const noexcept {
  return git_repository_workdir(this->get());
}

std::string_view repository::path () const noexcept {
  return git_repository_path(this->get());
}

repository::state repository::current_state () const noexcept {
  return state(git_repository_state(this->get()));
}

bool repository::head_detached () const noexcept {
  // TODO: Handle error codes.
  auto result = git_repository_head_detached(this->get());
  return result == 1;
}

bool repository::head_unborn () const noexcept {
  auto result = git_repository_head_unborn(this->get());
  return result == 1;
}

bool repository::is_worktree () const noexcept {
  return git_repository_is_worktree(this->get());
}

bool repository::is_shallow () const noexcept {
  return git_repository_is_shallow(this->get());
}

bool repository::is_empty () const noexcept {
  return git_repository_is_empty(this->get());
}

bool repository::is_bare () const noexcept {
  return git_repository_is_bare(this->get());
}

void swap (repository& lhs, repository& rhs) noexcept { lhs.swap(rhs); }

} /* namespace git */