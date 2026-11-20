// Holds: the four statuses of a requirement or an issue, in order (DSH-03.b, DSH-05.a). Depends on: nothing.
// Used by: Requirement, Issue, NewIssue, StatusRule, the backends. Reads or writes: nothing.

/// Where a requirement or an issue is: not agreed, waiting for a story, in a story, accepted. The order is the
/// order of the enum.
enum Status {
  proposed,
  backlog,
  planned,
  done;

  /// The status written in [text]: its first word, ignoring case (`proposed (?)` is `proposed`). A blank or unknown
  /// word is `backlog` (DSH-03.b, DSH-05.a).
  static Status parse(String? text) {
    final word = (text ?? '').trim().split(RegExp(r'\s+')).first.toLowerCase();
    for (final s in Status.values) {
      if (s.name == word) return s;
    }
    return Status.backlog;
  }

  /// The status named exactly [name], or null.
  static Status? tryName(String? name) {
    for (final s in Status.values) {
      if (s.name == name) return s;
    }
    return null;
  }
}
