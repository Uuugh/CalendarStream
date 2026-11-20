// Holds: the usage panel (DSH-09.c, DSH-09.d): a bar of usage against estimate for each story, and the sprint total.
// Depends on: Sprint, UsageSummary, UsageColors, PointsFormat, AppLocalizations. Used by: the dashboard page.
// Reads or writes: nothing.

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import '../domain/points_format.dart';
import '../domain/sprint.dart';
import '../domain/usage_summary.dart';
import 'dashboard_layout.dart';
import 'usage_colors.dart';

/// The panel. A row per story, bar key `usage-bar-<storyId>` (a [LinearProgressIndicator] valued usage/estimate,
/// clamped); the sprint line has key `usage-total`, its bar `usage-bar-total`.
class UsagePanel extends StatelessWidget {
  const UsagePanel({super.key, required this.sprint});

  final Sprint sprint;

  Widget _row(BuildContext context, AppLocalizations t, String label, double usage, double estimate, Key barKey,
      {Key? key, TextStyle? style}) {
    final scheme = Theme.of(context).colorScheme;
    return Padding(
      key: key,
      padding: const EdgeInsets.symmetric(vertical: DashboardLayout.gap / 2),
      child: Row(children: [
        SizedBox(width: DashboardLayout.usageLabelWidth, child: Text(label, style: style)),
        Expanded(
          child: LinearProgressIndicator(
            key: barKey,
            value: UsageSummary.fraction(usage, estimate),
            color: UsageColors.of(Theme.of(context), over: usage > estimate),
            backgroundColor: scheme.surfaceContainerHighest,
          ),
        ),
        const SizedBox(width: DashboardLayout.gap),
        Text('${t.dshUsage}: ${PointsFormat.format(usage)} / ${t.dshEstimate}: ${PointsFormat.format(estimate)}'),
      ]),
    );
  }

  @override
  Widget build(BuildContext context) {
    final t = AppLocalizations.of(context);
    final text = Theme.of(context).textTheme;
    final total = UsageSummary(sprint);
    return Padding(
      padding: const EdgeInsets.all(DashboardLayout.gap),
      child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
        Text(t.dshUsagePanel, style: text.titleMedium),
        for (final s in sprint.stories)
          _row(context, t, s.id, s.usage, s.estimate, Key('usage-bar-${s.id}'), key: Key('usage-row-${s.id}')),
        _row(context, t, t.dshSprintTotal, total.totalUsage, total.totalEstimate, const Key('usage-bar-total'),
            key: const Key('usage-total'), style: text.titleSmall),
      ]),
    );
  }
}
