// Holds: the message that says why data could not be loaded (DSH-01.b, DSH-01.f, DSH-13.h). Depends on:
// AppLocalizations, ServerUnreachableException, IssueTrackerException. Used by: the columns and the board.
// Reads or writes: nothing.

import '../../../l10n/app_localizations.dart';
import '../data/issue_tracker_exception.dart';
import '../data/server_unreachable_exception.dart';

/// Error to text.
class LoadErrorText {
  const LoadErrorText._();

  /// The message for [error]: the server unreachable, else (when [tracker]) the issue tracker unreachable, else the
  /// data could not be read.
  static String of(AppLocalizations l, Object error, {bool tracker = false}) {
    final reason = '$error';
    if (error is ServerUnreachableException) return l.dshServerUnreachable(reason);
    if (tracker && error is IssueTrackerException) return l.dshTrackerUnreachable(reason);
    return l.dshLoadFailed(reason);
  }
}
