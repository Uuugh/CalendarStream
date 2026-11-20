// Holds: the contents of a story block (DSH-06.d, DSH-08, DSH-10): its members, its estimate and usage (tap to edit),
// the usage bar and the Accept control. Depends on: DashboardController, Block, SprintEdit, PointsDialog, UsageBar,
// ItemRow. Used by: BlockCard. Reads or writes: through the controller (the sprint file, statuses).

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import '../domain/block.dart';
import '../domain/points_format.dart';
import '../domain/sprint_edit.dart';
import 'dashboard_controller.dart';
import 'dashboard_layout.dart';
import 'drop_feedback.dart';
import 'item_row.dart';
import 'points_dialog.dart';
import 'usage_bar.dart';

/// The body of a story. Keys: `estimate-<id>`, `usage-<id>`, `usage-bar-<id>`, `accept-<id>`, `member-<item>`.
class StoryBody extends StatelessWidget {
  const StoryBody({super.key, required this.controller, required this.block});

  final DashboardController controller;
  final Block block;

  Widget _points(BuildContext context, Key key, String label, double value, {required bool estimate}) {
    return InkWell(
      key: key,
      onTap: () async {
        final next = await PointsDialog.show(context, label: label, initial: value);
        if (next == null || !context.mounted) return;
        await DropFeedback.run(
            context, estimate ? controller.setPoints(block.id, estimate: next) : controller.setPoints(block.id, usage: next));
      },
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 2, horizontal: 4),
        child: Row(mainAxisSize: MainAxisSize.min, children: [
          Text(label, style: Theme.of(context).textTheme.bodySmall),
          const SizedBox(width: 4),
          Text(PointsFormat.format(value), style: Theme.of(context).textTheme.bodyMedium?.copyWith(fontWeight: FontWeight.bold)),
        ]),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final l = AppLocalizations.of(context);
    final sprint = controller.sprint!;
    final items = sprint.itemsOf(block.id);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      mainAxisSize: MainAxisSize.min,
      children: [
        Wrap(spacing: DashboardLayout.gap, children: [
          _points(context, Key('estimate-${block.id}'), l.dshEstimate, block.estimate, estimate: true),
          _points(context, Key('usage-${block.id}'), l.dshUsage, block.usage, estimate: false),
        ]),
        KeyedSubtree(key: Key('usage-bar-${block.id}'), child: UsageBar(estimate: block.estimate, usage: block.usage)),
        const SizedBox(height: DashboardLayout.gap),
        for (final item in items)
          ItemRow(key: Key('member-$item'), item: item, lines: [item, if (controller.titleOf(item) != null) controller.titleOf(item)!]),
        if (SprintEdit.sitsInSprint(sprint, block.id))
          Align(
            alignment: Alignment.centerLeft,
            child: FilledButton(
              key: Key('accept-${block.id}'),
              onPressed: () => DropFeedback.run(context, controller.accept(block.id)),
              child: Text(l.dshAccept),
            ),
          ),
      ],
    );
  }
}
