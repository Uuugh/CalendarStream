// Holds: the error raised when the web app cannot reach the server (DSH-10.e). Depends on: IssueTrackerException.
// Used by: HttpFileAccess, HttpIssueTracker, the dashboard page. Reads or writes: nothing.

import 'issue_tracker_exception.dart';

/// The server did not answer; [reason] is shown as {reason} of msg:dshServerUnreachable. It is an
/// [IssueTrackerException] so every place that already handles tracker failures handles it too.
class ServerUnreachableException extends IssueTrackerException {
  const ServerUnreachableException(super.reason);
}
