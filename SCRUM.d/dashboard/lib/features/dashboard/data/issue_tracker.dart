// Holds: the interface to the issue tracker (DSH-01.e) and the one create-then-close rule (DSH-08.g).
// Depends on: Issue, NewIssue, IssuePartialFailure, IssueTrackerException. Used by: the dashboard page, the New issue dialog.
// Reads or writes: nothing itself; implementations read and write the issue tracker.

import '../domain/issue.dart';
import '../domain/new_issue.dart';
import 'issue_partial_failure.dart';
import 'issue_tracker_exception.dart';

/// The issue tracker as the dashboard sees it. Every method throws [IssueTrackerException] with the reason on failure.
abstract class IssueTracker {
  const IssueTracker();

  /// All issues, open and closed.
  Future<List<Issue>> load();

  /// Creates [issue] without closing it; returns its number.
  Future<int> createOpen(NewIssue issue);

  /// Closes issue [number].
  Future<void> close(int number);

  /// Creates [issue] once, then closes it when [NewIssue.closed]. Throws [IssuePartialFailure] with the number when
  /// the issue exists but the close failed (DSH-08.g); the caller then calls [close], not [create].
  Future<int> create(NewIssue issue) async {
    final number = await createOpen(issue);
    if (issue.closed) {
      try {
        await close(number);
      } on IssueTrackerException catch (e) {
        throw IssuePartialFailure(number, e.reason);
      }
    }
    return number;
  }
}
