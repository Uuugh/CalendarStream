// Holds: the error raised when an issue was created but a later step failed (DSH-08.g). Depends on: nothing.
// Used by: IssueService, the New issue dialog. Reads or writes: nothing.

/// The issue [number] exists; the step after its creation failed for [reason]. Not an [IssueTrackerException]:
/// the issue must not be created again.
class IssuePartialFailure implements Exception {
  const IssuePartialFailure(this.number, this.reason);

  final int number;
  final String reason;

  @override
  String toString() => 'issue #$number: $reason';
}
