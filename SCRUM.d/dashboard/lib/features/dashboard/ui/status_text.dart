// Holds: the message of each status (DSH-03.b). Depends on: Status, AppLocalizations.
// Used by: the rows, the filters, the New issue form. Reads or writes: nothing.

import '../../../l10n/app_localizations.dart';
import '../domain/status.dart';

/// Status as text.
class StatusText {
  const StatusText._();

  static String of(AppLocalizations l, Status status) => switch (status) {
        Status.proposed => l.dshStatusProposed,
        Status.backlog => l.dshStatusBacklog,
        Status.planned => l.dshStatusPlanned,
        Status.done => l.dshStatusDone,
      };
}
