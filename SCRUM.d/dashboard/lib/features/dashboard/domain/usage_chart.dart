// Holds: the pure model of the usage chart (DSH-14.c to DSH-14.f): bars, estimate bands, the projection and the over-100
// rule. Depends on: UsageRow, UsageSpan, UsageMeter, Sprint, BlockKind, DashboardLimits.
// Used by: the chart. Reads or writes: nothing.

import 'block_kind.dart';
import 'dashboard_limits.dart';
import 'sprint.dart';
import 'usage_meter.dart';
import 'usage_row.dart';
import 'usage_span.dart';

/// Chart figures as pure functions.
class UsageChart {
  const UsageChart._();

  /// The top of a meter's scale (DSH-14.b).
  static const double scaleMax = 100;

  /// For each row with a before and an after reading on [meter], the bar from before to after (DSH-14.c).
  static List<UsageSpan> bars(List<UsageRow> rows, UsageMeter meter) => [
        for (final r in rows)
          if (r.before(meter) != null && r.after(meter) != null) UsageSpan(r.block, r.before(meter)!, r.after(meter)!),
      ];

  /// For each row with an estimate and a before reading on [meter], the band that starts at the before reading and
  /// ends where the estimate plus its share ends; [UsageSpan.low] is where the estimate minus its share ends (DSH-14.d).
  static List<UsageSpan> bands(List<UsageRow> rows, UsageMeter meter) => [
        for (final r in rows)
          if (r.estimate(meter) != null && r.before(meter) != null) _band(r.block, r.before(meter)!, r.estimate(meter)!),
      ];

  static UsageSpan _band(String block, double before, double estimate) => UsageSpan(
        block,
        before,
        before + estimate * (1 + DashboardLimits.estimateRange),
        low: before + estimate * (1 - DashboardLimits.estimateRange),
      );

  /// The projection for the next planned sprint: the first sprint block of [sprint] in file order that has no after
  /// reading on [meter], from its before reading to before plus estimate (DSH-14.e); null when that sprint has no row, no before
  /// reading or no estimate, or there is no such sprint.
  static UsageSpan? projection(List<UsageRow> rows, Sprint sprint, UsageMeter meter) {
    for (final b in sprint.blocks) {
      if (b.kind != BlockKind.sprint) continue;
      final row = rows.where((r) => r.block == b.id).firstOrNull;
      if (row?.after(meter) != null) continue;
      final before = row?.before(meter);
      final estimate = row?.estimate(meter);
      return before == null || estimate == null ? null : UsageSpan(b.id, before, before + estimate);
    }
    return null;
  }

  /// True when [value] is above the 100 line and is drawn as a triangle with the real number in its tooltip (DSH-14.f).
  static bool overHundred(double value) => value > scaleMax;

  /// Where [value] is drawn on the 0 to 100 scale.
  static double position(double value) => value.clamp(0.0, scaleMax);
}
