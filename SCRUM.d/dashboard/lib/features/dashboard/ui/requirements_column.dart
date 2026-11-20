// Holds: the Requirements column (DSH-03, DSH-04, DSH-11, DSH-15.b): heading, count, the three filters, the expand-all
// switch and the draggable rows as an outline. Depends on: DashboardController, MultiFilterButton, ItemRow,
// ColumnFrame, StatusText, LoadErrorText, RequirementOutline, DashboardLimits. Used by: DashboardPage.
// Reads or writes: nothing itself (filters are saved by the controller; the expanded rows are kept here).

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import '../domain/dashboard_limits.dart';
import '../domain/requirement.dart';
import '../domain/requirement_choices.dart';
import '../domain/requirement_outline.dart';
import '../domain/status.dart';
import 'column_frame.dart';
import 'dashboard_controller.dart';
import 'dashboard_layout.dart';
import 'item_row.dart';
import 'load_error_text.dart';
import 'multi_filter_button.dart';
import 'status_text.dart';

/// The column of requirements, `Key('column-requirements')`; rows are `Key('req-<ID>')`, a requirement with listed
/// sub-requirements has `Key('outline-toggle-<ID>')`, and the switch above the list is `Key('outline-expand-all')`.
/// Every row starts collapsed (DSH-11.d).
class RequirementsColumn extends StatefulWidget {
  const RequirementsColumn({super.key = const Key('column-requirements'), required this.controller});

  final DashboardController controller;

  @override
  State<RequirementsColumn> createState() => _RequirementsColumnState();
}

class _RequirementsColumnState extends State<RequirementsColumn> {
  final Set<String> _expanded = {};

  @override
  Widget build(BuildContext context) {
    final controller = widget.controller;
    final l = AppLocalizations.of(context);
    final theme = Theme.of(context);
    final all = controller.requirements ?? const <Requirement>[];
    final feature = controller.filter('requirements.feature', RequirementChoices.features(all));
    final id = controller.filter('requirements.id', [for (final r in all) r.id]);
    final status = controller.filter('requirements.status', [for (final s in Status.values) s.name]);
    final shown = [
      for (final r in all)
        if (feature.matches(r.feature) && id.matches(r.id) && status.matches(r.status.name)) r
    ];
    final parents = RequirementOutline.parents(shown);
    final allOpen = parents.isNotEmpty && parents.every(_expanded.contains);
    final rows = RequirementOutline.rows(shown, _expanded);
    final indentUnit = (TextPainter(
      text: TextSpan(text: '0' * DashboardLimits.subRequirementIndent, style: theme.textTheme.bodyMedium),
      textDirection: Directionality.of(context),
      textScaler: MediaQuery.textScalerOf(context),
    )..layout())
        .width;
    final error = controller.requirementsError;
    return ColumnFrame(
      header: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(children: [
            Expanded(child: Text(l.dshRequirements, style: theme.textTheme.titleMedium, overflow: TextOverflow.ellipsis)),
            Text(l.dshShownOf(shown.length.toString(), all.length.toString()), style: theme.textTheme.bodySmall),
          ]),
          Wrap(spacing: DashboardLayout.gap, crossAxisAlignment: WrapCrossAlignment.center, children: [
            MultiFilterButton(
              id: 'requirements-feature',
              label: l.dshFilterFeature,
              filter: feature,
              onChanged: (f) => controller.setFilter('requirements.feature', f),
            ),
            MultiFilterButton(
              id: 'requirements-id',
              label: l.dshFilterRequirement,
              filter: id,
              onChanged: (f) => controller.setFilter('requirements.id', f),
            ),
            MultiFilterButton(
              id: 'requirements-status',
              label: l.dshFilterStatus,
              filter: status,
              labelOf: (c) => StatusText.of(l, Status.parse(c)),
              onChanged: (f) => controller.setFilter('requirements.status', f),
            ),
            Row(mainAxisSize: MainAxisSize.min, children: [
              Switch(
                key: const Key('outline-expand-all'),
                value: allOpen,
                onChanged: (on) => setState(() {
                  _expanded
                    ..clear()
                    ..addAll(on ? parents : const <String>[]);
                }),
              ),
              Text(l.dshExpandAll, style: theme.textTheme.labelMedium),
            ]),
          ]),
          if (error != null) Text(LoadErrorText.of(l, error), style: TextStyle(color: theme.colorScheme.error)),
        ],
      ),
      builder: (context, scroll) => ListView.builder(
        controller: scroll,
        itemCount: rows.length,
        itemBuilder: (context, i) {
          final row = rows[i];
          final r = row.requirement;
          return ItemRow(
            key: Key('req-${r.id}'),
            item: r.id,
            indent: row.depth * indentUnit,
            leading: row.hasChildren
                ? Tooltip(
                    message: row.expanded ? l.dshCollapseRow : l.dshExpandRow,
                    child: InkWell(
                      key: Key('outline-toggle-${r.id}'),
                      onTap: () => setState(() => row.expanded ? _expanded.remove(r.id) : _expanded.add(r.id)),
                      child: Icon(row.expanded ? Icons.arrow_drop_down : Icons.arrow_right),
                    ),
                  )
                : null,
            lines: ['${r.id}  ${StatusText.of(l, r.status)}', r.feature, r.statement],
          );
        },
      ),
    );
  }
}
