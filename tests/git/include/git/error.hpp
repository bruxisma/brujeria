#ifndef GIT_ERROR_HPP
#define GIT_ERROR_HPP

#include <system_error>
#include <git2.h>

namespace git {

std::error_category const& error_category() noexcept;

enum class error {
  ok = GIT_OK,
  generic = GIT_ERROR,
  not_found = GIT_ENOTFOUND,
  object_exists = GIT_EEXISTS,
  ambiguous = GIT_EAMBIGUOUS,
  buffer_too_small = GIT_EBUFS,
  bare_repo = GIT_EBAREREPO,
  unborn_branch = GIT_EUNBORNBRANCH,
  unmerged = GIT_EUNMERGED,
  not_fast_forwardable = GIT_ENONFASTFORWARD,
  invalid_spec = GIT_EINVALIDSPEC,
  checkout_conflict = GIT_ECONFLICT,
  locked_file = GIT_ELOCKED,
  modified = GIT_EMODIFIED,
  authentication = GIT_EAUTH,
  invalid_certificate = GIT_ECERTIFICATE,
  already_applied = GIT_EAPPLIED,
  peel_not_possible = GIT_EPEEL,
  eof = GIT_EEOF,
  invalid_operation = GIT_EINVALID,
  uncommitted_changes = GIT_EUNCOMMITTED,
  invalid_directory = GIT_EDIRECTORY,
  merge_conflict = GIT_EMERGECONFLICT,
  hash_mismatch = GIT_EMISMATCH,
};

std::error_code make_error_code (error) noexcept;
std::error_code to_code (int) noexcept;

} /* namespace git */

namespace std {

template <> struct is_error_condition_enum<git::error> : true_type { };
template <> struct is_error_code_enum<git::error> : true_type { };

} /* namespace std */

#endif /* GIT_ERROR_HPP */