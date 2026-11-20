// Holds: one draggable requirement or issue row of a column or of the Backlog block (DSH-03, DSH-05, DSH-07). Depends
// on: ItemDrag, DashboardLayout. Used by: RequirementsColumn, IssuesColumn, BacklogBlock. Reads or writes: nothing.

import 'package:flutter/material.dart';

import 'dashboard_layout.dart';
import 'drag_payload.dart';

/// A row that can be dragged as [item] (a requirement ID or `#N`). [lines] are the texts of the row, the first one bold.
class ItemRow extends StatelessWidget {
  const ItemRow({super.key, required this.item, required this.lines, this.trailing, this.leading, this.indent = 0});

  final String item;
  final List<String> lines;
  final Widget? trailing;

  /// A widget before the text (the outline triangle) and the indent of the row from the left.
  final Widget? leading;
  final double indent;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final card = _Body(lines: lines, trailing: trailing, leading: leading);
    return Padding(
      padding: EdgeInsets.only(top: 2, bottom: 2, left: indent),
      child: Draggable<DragPayload>(
        data: ItemDrag(item),
        feedback: Material(
          type: MaterialType.transparency,
          child: SizedBox(
            width: DashboardLayout.blockWidth,
            child: DecoratedBox(
              decoration: BoxDecoration(
                color: theme.colorScheme.surface,
                border: Border.all(color: theme.colorScheme.primary),
                borderRadius: BorderRadius.circular(6),
              ),
              child: _Body(lines: lines, trailing: null, leading: null),
            ),
          ),
        ),
        childWhenDragging: Opacity(opacity: 0.4, child: card),
        child: card,
      ),
    );
  }
}

class _Body extends StatelessWidget {
  const _Body({required this.lines, required this.trailing, required this.leading});

  final List<String> lines;
  final Widget? trailing;
  final Widget? leading;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Container(
      padding: const EdgeInsets.all(DashboardLayout.pad),
      decoration: BoxDecoration(
        color: theme.colorScheme.surfaceContainer,
        borderRadius: BorderRadius.circular(6),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          ?leading,
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                for (var i = 0; i < lines.length; i++)
                  Text(
                    lines[i],
                    maxLines: i == 0 ? 2 : 3,
                    overflow: TextOverflow.ellipsis,
                    style: i == 0
                        ? theme.textTheme.bodyMedium?.copyWith(fontWeight: FontWeight.bold)
                        : theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant),
                  ),
              ],
            ),
          ),
          ?trailing,
        ],
      ),
    );
  }
}
