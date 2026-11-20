// Holds: one row of the Usage table of `SCRUM.d/usage.md` (DSH-14.a). Depends on: UsageMeter.
// Used by: UsageTable, UsageChart. Reads or writes: nothing.

import 'usage_meter.dart';

/// A block's estimate and its readings before and after, as percent of each meter. A null is a dash (not known).
class UsageRow {
  const UsageRow({
    required this.block,
    this.estimateSession,
    this.estimateWeek,
    this.beforeSession,
    this.beforeWeek,
    this.afterSession,
    this.afterWeek,
  });

  final String block;
  final double? estimateSession;
  final double? estimateWeek;
  final double? beforeSession;
  final double? beforeWeek;
  final double? afterSession;
  final double? afterWeek;

  double? estimate(UsageMeter m) => m == UsageMeter.session ? estimateSession : estimateWeek;
  double? before(UsageMeter m) => m == UsageMeter.session ? beforeSession : beforeWeek;
  double? after(UsageMeter m) => m == UsageMeter.session ? afterSession : afterWeek;
}
