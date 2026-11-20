// Holds: the Agent progress column (DSH-12, DSH-14, DSH-15.b): the usage chart on top, then one bar per progress file, or
// the note that there are none. Depends on: DashboardController, UsageChartView, ProgressEntry, StatusColors, LoadErrorText.
// Used by: DashboardPage. Reads or writes: nothing.

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import '../../../theme/app_theme.dart';
import '../domain/progress_entry.dart';
import 'column_frame.dart';
import 'dashboard_controller.dart';
import 'dashboard_layout.dart';
import 'load_error_text.dart';
import 'usage_chart_view.dart';

/// The column, `Key('column-progress')`; each bar is `Key('progress-bar-<label>')`.
class ProgressColumn extends StatelessWidget {
  const ProgressColumn({required this.controller}) : super(key: const Key('column-progress'));

  final DashboardController controller;

  @override
  Widget build(BuildContext context) {
    final l = AppLocalizations.of(context);
    final theme = Theme.of(context);
    final colors = StatusColors.of(theme);
    final entries = controller.progress ?? const <ProgressEntry>[];
    return ColumnFrame(
      header: Text(l.dshAgentProgress, style: theme.textTheme.titleMedium),
      builder: (context, scroll) => ListView(
        controller: scroll,
        children: [
          UsageChartView(rows: controller.usage, sprint: controller.sprint, error: controller.usageError),
          const SizedBox(height: DashboardLayout.gap),
          if (controller.progressError != null)
            Text(LoadErrorText.of(l, controller.progressError!), style: TextStyle(color: theme.colorScheme.error))
          else if (entries.isEmpty)
            Text(l.dshNoProgress, style: theme.textTheme.bodySmall),
          for (final e in entries)
            Padding(
              key: Key('progress-bar-${e.label}'),
              padding: const EdgeInsets.only(bottom: DashboardLayout.gap),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Row(children: [
                    Expanded(child: Text(e.label, overflow: TextOverflow.ellipsis, style: theme.textTheme.bodyMedium)),
                    Text(e.text, style: theme.textTheme.bodySmall),
                  ]),
                  const SizedBox(height: 2),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(DashboardLayout.barHeight),
                    child: LinearProgressIndicator(
                      value: e.fraction,
                      minHeight: DashboardLayout.barHeight,
                      color: e.fraction >= 1 ? colors.ok : colors.run,
                      backgroundColor: theme.colorScheme.surfaceContainerHigh,
                    ),
                  ),
                ],
              ),
            ),
        ],
      ),
    );
  }
}
