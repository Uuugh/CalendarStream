// Holds: the filter bar both lists share (DSH-04, DSH-04.a-d, UIC-21): feature and status dropdowns, a requirement
// text box, and the shown-of-total count. Depends on: ListFilter, AppLocalizations. Used by: the dashboard page.
// Reads or writes: nothing.

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import '../domain/list_filter.dart';
import 'dashboard_layout.dart';

/// Shows [filter] and reports changes through [onChanged]. [features] and [statuses] are the dropdown values;
/// [statusLabel] turns a status value into its shown text.
class ListFilterBar extends StatelessWidget {
  const ListFilterBar({
    super.key,
    required this.filter,
    required this.onChanged,
    required this.features,
    required this.statuses,
    required this.statusLabel,
    required this.shown,
    required this.total,
  });

  final ListFilter filter;
  final ValueChanged<ListFilter> onChanged;
  final List<String> features;
  final List<String> statuses;
  final String Function(String status) statusLabel;
  final int shown;
  final int total;

  @override
  Widget build(BuildContext context) {
    final t = AppLocalizations.of(context);
    return Wrap(
      spacing: DashboardLayout.gap,
      runSpacing: DashboardLayout.gap,
      crossAxisAlignment: WrapCrossAlignment.center,
      children: [
        _dropdown(t.dshFilterFeature, t.dshAll, filter.feature, features, (v) => v,
            (v) => onChanged(ListFilter(feature: v, requirement: filter.requirement, status: filter.status))),
        SizedBox(
          width: DashboardLayout.filterWidth,
          child: TextFormField(
            initialValue: filter.requirement,
            decoration: InputDecoration(labelText: t.dshFilterRequirement),
            onChanged: (v) => onChanged(ListFilter(feature: filter.feature, requirement: v, status: filter.status)),
          ),
        ),
        _dropdown(t.dshFilterStatus, t.dshAll, filter.status, statuses, statusLabel,
            (v) => onChanged(ListFilter(feature: filter.feature, requirement: filter.requirement, status: v))),
        Text(t.dshShownOf('$shown', '$total')),
      ],
    );
  }

  Widget _dropdown(String label, String all, String? value, List<String> values, String Function(String) text,
      ValueChanged<String?> onSelected) {
    return SizedBox(
      width: DashboardLayout.filterWidth,
      child: InputDecorator(
        decoration: InputDecoration(labelText: label),
        child: DropdownButtonHideUnderline(
          child: DropdownButton<String?>(
            isDense: true,
            isExpanded: true,
            value: values.contains(value) ? value : null,
            items: [
              DropdownMenuItem<String?>(value: null, child: Text(all)),
              for (final v in values) DropdownMenuItem<String?>(value: v, child: Text(text(v))),
            ],
            onChanged: onSelected,
          ),
        ),
      ),
    );
  }
}
