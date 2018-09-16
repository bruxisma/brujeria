#include <git/error.hpp>

namespace git {

struct git_category final : std::error_category {
  virtual char const* name () const noexcept override final;
  virtual std::string message (int) const override final;
};

std::error_category const& error_category() noexcept {
  static git_category category;
  return category;
}

std::error_code make_error_code (error e) noexcept {
  return std::error_code(int(e), error_category());
}

std::error_code to_code (int ec) noexcept {
  return std::error_code(ec, error_category());
}

char const* git_category::name () const noexcept { return "git"; }
std::string git_category::message (int condition) const {
  switch (error(condition)) {
    case error::ok: return "no error";
    case error::generic: return "generic error";
    case error::not_found: return "requested object could not be found";
    case error::object_exists: return "object exists preventing operation";
    case error::ambiguous: return "more than one object matches";
    case error::buffer_too_small: return "output buffer too short to hold data";
    case error::bare_repo: return "operation not allowed on bare repository";
    case error::unborn_branch: return "HEAD refers to branch with no commits";
    case error::unmerged: return "merge in progress prevented operation";
    case error::not_fast_forwardable: return "reference was not fast forwardable";
    case error::invalid_spec: return "name/ref spec was not in a valid format";
    case error::checkout_conflict: return "checkout conflicts prevented operation";
    case error::locked_file: return "lock file prevented operation";
    case error::modified: return "reference value does not match expected";
    case error::authentication: return "authentication error";
    case error::invalid_certificate: return "server certificate invalid";
    case error::already_applied: return "patch/merge has already been applied";
    case error::peel_not_possible: return "the requested peel operation is not possible";
    case error::eof: return "unexpected eof";
    case error::invalid_operation: return "invalid operation or input";
    case error::uncommitted_changes: return "uncommitted changes in index prevented operation";
    case error::invalid_directory: return "the operation is not valid for a directory";
    case error::merge_conflict: return "a merge conflict exists and cannot continue";
    case error::hash_mismatch: return "hashsum mismatch in object";
  }
}

} /* namespace git */
