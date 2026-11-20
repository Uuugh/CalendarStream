// Holds: the error raised when the issue tracker cannot be reached (DSH-01.b). Depends on: nothing.
// Used by: IssueService, the dashboard page. Reads or writes: nothing.

/// The tracker could not be reached or answered badly; [reason] is shown as {reason} of msg:dshTrackerUnreachable.
class IssueTrackerException implements Exception {
  const IssueTrackerException(this.reason);

  final String reason;

  @override
  String toString() => reason;
}
