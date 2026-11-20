// Holds: the one rule on how a status may change (DSH-13.c). Depends on: Status.
// Used by: LocalBackend (the only place that checks it). Reads or writes: nothing.

import 'status.dart';

/// A status moves up the order; the only move down is `planned` to `backlog`.
class StatusRule {
  const StatusRule._();

  /// Why [from] cannot become [to], or null when the change is allowed or does nothing.
  static String? refusal(Status from, Status to) {
    if (from == to) return null;
    if (to.index > from.index) return null;
    if (from == Status.planned && to == Status.backlog) return null;
    return 'a status cannot move from ${from.name} to ${to.name}';
  }
}
