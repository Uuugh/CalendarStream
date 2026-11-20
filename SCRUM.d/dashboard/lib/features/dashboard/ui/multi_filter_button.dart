// Holds: the shared filter control (UIC-21, UIC-12, DSH-04): one button that opens a menu with a checkbox per choice
// and Select all / Select none rows, and shows when the filter hides something. Depends on: MultiFilter,
// AppLocalizations. Used by: RequirementsColumn, IssuesColumn. Reads or writes: nothing.

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import '../domain/multi_filter.dart';
import 'dashboard_layout.dart';

/// A filter dropdown. Keys: the button is `Key('filter-<id>')`, the rows `Key('filter-<id>-all')`,
/// `Key('filter-<id>-none')` and `Key('filter-<id>-option-<choice>')`. A change applies at once through [onChanged].
class MultiFilterButton extends StatelessWidget {
  MultiFilterButton({
    required this.id,
    required this.label,
    required this.filter,
    required this.onChanged,
    this.labelOf,
  }) : super(key: Key('filter-$id'));

  final String id;
  final String label;
  final MultiFilter filter;
  final ValueChanged<MultiFilter> onChanged;

  /// How a choice is shown; the choice itself when null.
  final String Function(String choice)? labelOf;

  @override
  Widget build(BuildContext context) {
    final l = AppLocalizations.of(context);
    final theme = Theme.of(context);
    final active = filter.isActive;
    return MenuAnchor(
      style: const MenuStyle(maximumSize: WidgetStatePropertyAll(Size(360, 420))),
      menuChildren: [
        MenuItemButton(
          key: Key('filter-$id-all'),
          closeOnActivate: false,
          onPressed: () => onChanged(filter.selectAll()),
          child: Text(l.selectAll),
        ),
        MenuItemButton(
          key: Key('filter-$id-none'),
          closeOnActivate: false,
          onPressed: () => onChanged(filter.selectNone()),
          child: Text(l.selectNone),
        ),
        for (final c in filter.choices)
          MenuItemButton(
            key: Key('filter-$id-option-$c'),
            closeOnActivate: false,
            onPressed: () => onChanged(filter.toggle(c)),
            leadingIcon: Icon(filter.isSelected(c) ? Icons.check_box : Icons.check_box_outline_blank),
            child: Text(labelOf == null ? c : labelOf!(c)),
          ),
      ],
      builder: (context, controller, _) => TextButton.icon(
        onPressed: () => controller.isOpen ? controller.close() : controller.open(),
        icon: Badge(
          isLabelVisible: active,
          smallSize: DashboardLayout.gap,
          child: Icon(active ? Icons.filter_alt : Icons.filter_alt_outlined, size: 18),
        ),
        label: Text(label, overflow: TextOverflow.ellipsis, style: theme.textTheme.labelMedium),
      ),
    );
  }
}
