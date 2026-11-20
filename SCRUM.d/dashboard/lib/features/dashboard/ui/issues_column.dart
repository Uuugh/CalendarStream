// Holds: the Issues column (DSH-05, DSH-04, DSH-09, DSH-01.b, DSH-15.b): heading, truncation note, New issue button,
// the three filters and the draggable rows. Depends on: DashboardController, MultiFilterButton, ItemRow, NewIssueDialog,
// ColumnFrame, StatusText, LoadErrorText, DashboardLimits. Used by: DashboardPage. Reads or writes: through the controller.

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import '../domain/dashboard_limits.dart';
import '../domain/issue.dart';
import '../domain/status.dart';
import 'column_frame.dart';
import 'dashboard_controller.dart';
import 'dashboard_layout.dart';
import 'item_row.dart';
import 'load_error_text.dart';
import 'multi_filter_button.dart';
import 'new_issue_dialog.dart';
import 'status_text.dart';

/// The column of issues, `Key('column-issues')`; rows are `Key('issue-<number>')`, the button `Key('new-issue-button')`.
class IssuesColumn extends StatelessWidget {
  const IssuesColumn({required this.controller}) : super(key: const Key('column-issues'));

  final DashboardController controller;

  @override
  Widget build(BuildContext context) {
    final l = AppLocalizations.of(context);
    final theme = Theme.of(context);
    final all = controller.issues ?? const <Issue>[];
    final features = <String>{for (final i in all) if (i.feature != null) i.feature!}.toList();
    final ids = <String>{for (final i in all) if (i.requirement != null) i.requirement!}.toList();
    final feature = controller.filter('issues.feature', features);
    final id = controller.filter('issues.id', ids);
    final status = controller.filter('issues.status', [for (final s in Status.values) s.name]);
    final shown = [
      for (final i in all)
        if (feature.matches(i.feature) && id.matches(i.requirement) && status.matches(i.status.name)) i
    ];
    final error = controller.issuesError;
    return ColumnFrame(
      header: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(children: [
            Expanded(child: Text(l.dshIssues, style: theme.textTheme.titleMedium, overflow: TextOverflow.ellipsis)),
            Text(l.dshShownOf(shown.length.toString(), all.length.toString()), style: theme.textTheme.bodySmall),
            const SizedBox(width: DashboardLayout.gap),
            FilledButton(
              key: const Key('new-issue-button'),
              onPressed: () => NewIssueDialog.show(context, controller),
              child: Text(l.dshNewIssue),
            ),
          ]),
          if (all.length >= DashboardLimits.issues) Text(l.dshIssuesTruncated(DashboardLimits.issues.toString()), style: theme.textTheme.bodySmall),
          Wrap(spacing: DashboardLayout.gap, children: [
            MultiFilterButton(
              id: 'issues-feature',
              label: l.dshFilterFeature,
              filter: feature,
              onChanged: (f) => controller.setFilter('issues.feature', f),
            ),
            MultiFilterButton(
              id: 'issues-id',
              label: l.dshFilterRequirement,
              filter: id,
              onChanged: (f) => controller.setFilter('issues.id', f),
            ),
            MultiFilterButton(
              id: 'issues-status',
              label: l.dshFilterStatus,
              filter: status,
              labelOf: (c) => StatusText.of(l, Status.parse(c)),
              onChanged: (f) => controller.setFilter('issues.status', f),
            ),
          ]),
          if (error != null) Text(LoadErrorText.of(l, error, tracker: true), style: TextStyle(color: theme.colorScheme.error)),
        ],
      ),
      builder: (context, scroll) => ListView.builder(
        controller: scroll,
        itemCount: shown.length,
        itemBuilder: (context, i) {
          final issue = shown[i];
          return ItemRow(
            key: Key('issue-${issue.number}'),
            item: DashboardController.issueItem(issue.number),
            lines: [
              '#${issue.number}  ${issue.title}',
              StatusText.of(l, issue.status),
              '${issue.feature ?? DashboardLayout.dash}  ${issue.requirement ?? DashboardLayout.dash}  ${issue.assignee.isEmpty ? DashboardLayout.dash : issue.assignee}',
            ],
          );
        },
      ),
    );
  }
}
