// Holds: one block of the board (DSH-06.c, DSH-07.a, DSH-10): a card with its name and kind, its children drawn inside
// it, and for a sprint or an epic the sums and a bar. Depends on: DashboardController, BlockRules, SprintEdit, StoryBody,
// UsageBar, DragPayload. Used by: BoardView, BlockCard itself (children). Reads or writes: through the controller.

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import '../domain/block.dart';
import '../domain/block_kind.dart';
import '../domain/points_format.dart';
import '../domain/sprint_edit.dart';
import 'block_kind_text.dart';
import 'dashboard_controller.dart';
import 'dashboard_layout.dart';
import 'drag_payload.dart';
import 'drop_feedback.dart';
import 'story_body.dart';
import 'usage_bar.dart';

/// A block. Keys: the card (and drop target) `block-card-<id>`, the draggable heading `block-<id>`. A block at the top
/// of the board is [bounded] to the height it is given and scrolls its contents on its own (DSH-15.b); a child grows
/// with its content inside the parent's scroll.
class BlockCard extends StatefulWidget {
  const BlockCard({super.key, required this.controller, required this.block, this.bounded = false});

  final DashboardController controller;
  final Block block;
  final bool bounded;

  @override
  State<BlockCard> createState() => _BlockCardState();
}

class _BlockCardState extends State<BlockCard> {
  final ScrollController _scroll = ScrollController();

  @override
  void dispose() {
    _scroll.dispose();
    super.dispose();
  }

  Widget _heading(BuildContext context, AppLocalizations l) {
    final theme = Theme.of(context);
    final block = widget.block;
    final line = Row(children: [
      Icon(Icons.drag_indicator, size: 18, color: theme.colorScheme.onSurfaceVariant),
      const SizedBox(width: 4),
      Expanded(child: Text(block.name, overflow: TextOverflow.ellipsis, style: theme.textTheme.titleSmall)),
      const SizedBox(width: 4),
      Text(BlockKindText.of(l, block.kind), style: theme.textTheme.labelSmall),
    ]);
    return Draggable<DragPayload>(
      key: Key('block-${block.id}'),
      data: BlockDrag(block.id),
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
            child: Padding(padding: const EdgeInsets.all(DashboardLayout.pad), child: line),
          ),
        ),
      ),
      childWhenDragging: Opacity(opacity: 0.4, child: line),
      child: line,
    );
  }

  Widget _body(BuildContext context, AppLocalizations l) {
    final controller = widget.controller;
    final sprint = controller.sprint!;
    final block = widget.block;
    if (block.kind == BlockKind.story) return StoryBody(controller: controller, block: block);
    final theme = Theme.of(context);
    final estimate = SprintEdit.estimateOf(sprint, block.id);
    final usage = SprintEdit.usageOf(sprint, block.id);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      mainAxisSize: MainAxisSize.min,
      children: [
        Wrap(spacing: DashboardLayout.gap, children: [
          Row(mainAxisSize: MainAxisSize.min, children: [
            Text(l.dshEstimate, style: theme.textTheme.bodySmall),
            const SizedBox(width: 4),
            Text(PointsFormat.format(estimate),
                key: Key('estimate-${block.id}'), style: theme.textTheme.bodyMedium?.copyWith(fontWeight: FontWeight.bold)),
          ]),
          Row(mainAxisSize: MainAxisSize.min, children: [
            Text(l.dshUsage, style: theme.textTheme.bodySmall),
            const SizedBox(width: 4),
            Text(PointsFormat.format(usage),
                key: Key('usage-${block.id}'), style: theme.textTheme.bodyMedium?.copyWith(fontWeight: FontWeight.bold)),
          ]),
        ]),
        KeyedSubtree(key: Key('usage-bar-${block.id}'), child: UsageBar(estimate: estimate, usage: usage)),
        const SizedBox(height: DashboardLayout.gap),
        for (final child in sprint.blocks.where((b) => b.parent == block.id))
          Padding(
            padding: const EdgeInsets.only(bottom: DashboardLayout.gap),
            child: BlockCard(key: ValueKey('card-${child.id}'), controller: controller, block: child),
          ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    final l = AppLocalizations.of(context);
    final theme = Theme.of(context);
    final block = widget.block;
    final controller = widget.controller;
    return DragTarget<DragPayload>(
      key: Key('block-card-${block.id}'),
      onWillAcceptWithDetails: (d) => !(d.data is BlockDrag && (d.data as BlockDrag).id == block.id),
      onAcceptWithDetails: (d) => DropFeedback.run(
        context,
        switch (d.data) {
          BlockDrag b => controller.dropBlock(b.id, block.id),
          ItemDrag i => controller.dropItem(i.item, block.id),
        },
      ),
      builder: (context, candidates, _) {
        final body = _body(context, l);
        return DecoratedBox(
          decoration: BoxDecoration(
            color: theme.colorScheme.surface,
            border: Border.all(color: candidates.isEmpty ? theme.colorScheme.outlineVariant : theme.colorScheme.primary, width: candidates.isEmpty ? 1 : 2),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Padding(
            padding: const EdgeInsets.all(DashboardLayout.pad),
            child: Column(
              mainAxisSize: widget.bounded ? MainAxisSize.max : MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                _heading(context, l),
                const SizedBox(height: DashboardLayout.gap),
                if (widget.bounded)
                  Expanded(child: Scrollbar(controller: _scroll, child: SingleChildScrollView(controller: _scroll, child: body)))
                else
                  body,
              ],
            ),
          ),
        );
      },
    );
  }
}
