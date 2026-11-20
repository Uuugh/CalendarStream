// Holds: the usage chart at the top of the Agent progress column (DSH-14): heading, the session meter and the week meter,
// or the note that there are no readings. Depends on: UsageMeterView, UsageRow, Sprint, LoadErrorText.
// Used by: ProgressColumn. Reads or writes: nothing.

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import '../domain/sprint.dart';
import '../domain/usage_meter.dart';
import '../domain/usage_row.dart';
import 'load_error_text.dart';
import 'usage_meter_view.dart';

/// The chart, `Key('usage-chart')`. [rows] is null when the usage file is missing or has no table (DSH-14.g).
class UsageChartView extends StatelessWidget {
  const UsageChartView({required this.rows, required this.sprint, this.error}) : super(key: const Key('usage-chart'));

  final List<UsageRow>? rows;
  final Sprint? sprint;
  final Object? error;

  @override
  Widget build(BuildContext context) {
    final l = AppLocalizations.of(context);
    final theme = Theme.of(context);
    final data = rows;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Text(l.dshUsageChart, style: theme.textTheme.titleSmall),
        if (error != null)
          Text(LoadErrorText.of(l, error!), style: TextStyle(color: theme.colorScheme.error))
        else if (data == null || data.isEmpty)
          Text(l.dshNoUsage, style: theme.textTheme.bodySmall)
        else
          for (final m in UsageMeter.values) UsageMeterView(meter: m, rows: data, sprint: sprint),
      ],
    );
  }
}
