#ifndef GIT_REPOSITORY_HPP
#define GIT_REPOSITORY_HPP

#include <git/memory.hpp>
#include <git/error.hpp>
#include <ciso646>

#include <string_view>
#include <string>


namespace git {

enum class bare : bool { no, yes };

struct repository final {
  using handle_type = unique_ptr<git_repository>;
  using pointer = handle_type::pointer;

  enum class state {
    none = GIT_REPOSITORY_STATE_NONE,
    merge = GIT_REPOSITORY_STATE_MERGE,
    revert = GIT_REPOSITORY_STATE_REVERT,
    revert_sequence = GIT_REPOSITORY_STATE_REVERT_SEQUENCE,
    cherrypick = GIT_REPOSITORY_STATE_CHERRYPICK,
    cherrypick_sequence = GIT_REPOSITORY_STATE_CHERRYPICK_SEQUENCE,
    bisect = GIT_REPOSITORY_STATE_BISECT,
    rebase = GIT_REPOSITORY_STATE_REBASE,
    rebase_interactive = GIT_REPOSITORY_STATE_REBASE_INTERACTIVE,
    rebase_merge = GIT_REPOSITORY_STATE_REBASE_MERGE,
    apply_mailbox = GIT_REPOSITORY_STATE_APPLY_MAILBOX,
    apply_malbox_or_rebase = GIT_REPOSITORY_STATE_APPLY_MAILBOX_OR_REBASE,
  };

  repository (std::string path);

  static repository init (std::string, bare);
  static repository init (std::string);

  void swap (repository& that) noexcept;

  explicit operator bool () const noexcept;
  pointer get () const noexcept;

  std::error_code add_ignore_rule (char const* rules) noexcept;
  std::error_code clear_rules () noexcept;
  bool is_ignored (char const* path) const noexcept;

  std::string_view current_namespace () const noexcept;
  std::string_view username () const noexcept;
  std::string_view email () const noexcept;

  // TODO: Change to std::fs::path once gcc 8 is available.
  std::string_view working_directory () const noexcept;
  std::string_view path () const noexcept;

  state current_state () const noexcept;

  bool head_detached () const noexcept;
  bool head_unborn () const noexcept;

  bool is_worktree () const noexcept;
  bool is_shallow () const noexcept;
  bool is_empty () const noexcept;
  bool is_bare () const noexcept;

private:
  repository (pointer) noexcept;
  handle_type handle;
};

void swap (repository&, repository&) noexcept;

} /* namespace git */

#endif /* GIT_REPOSITORY_HPP */