// Holds: the Backlog block, the first block of the board (DSH-06.a, DSH-07.c, DSH-07.d, DSH-07.f): the requirements and
// issues whose status is backlog, and the drop target that sets a status back to backlog. Depends on:
// DashboardController, ItemRow, DragPayload, StatusText. Used by: BoardView. Reads or writes: through the controller.

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import '../domain/status.dart';
import 'dashboard_controller.dart';
import 'dashboard_layout.dart';
import 'drag_payload.dart';
import 'drop_feedback.dart';
import 'item_row.dart';
import 'load_error_text.dart';

/// The block, `Key('backlog-block')`; its rows are `Key('backlog-req-<ID>')` and `Key('backlog-issue-<number>')`.
class BacklogBlock extends StatefulWidget {
  const BacklogBlock({required this.controller}) : super(key: const Key('backlog-block'));

  final DashboardController controller;

  @override
  State<BacklogBlock> createState() => _BacklogBlockState();
}

class _BacklogBlockState extends State<BacklogBlock> {
  final ScrollController _scroll = ScrollController();

  @override
  void dispose() {
    _scroll.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l = AppLocalizations.of(context);
    final theme = Theme.of(context);
    final controller = widget.controller;
    final requirements = [
      for (final r in controller.requirements ?? const []) if (r.status == Status.backlog) r
    ];
    final issues = [
      for (final i in controller.issues ?? const []) if (i.status == Status.backlog) i
    ];
    final errors = [
      if (controller.requirementsError != null) LoadErrorText.of(l, controller.requirementsError!),
      if (controller.issuesError != null) LoadErrorText.of(l, controller.issuesError!, tracker: true),
    ];
    return DragTarget<DragPayload>(
      onWillAcceptWithDetails: (_) => true,
      onAcceptWithDetails: (d) => DropFeedback.run(
        context,
        switch (d.data) {
          ItemDrag i => controller.dropItem(i.item, null),
          BlockDrag _ => Future.value(controller.dropBlockOnBacklog()),
        },
      ),
      builder: (context, candidates, _) => DecoratedBox(
        decoration: BoxDecoration(
          color: theme.colorScheme.surface,
          border: Border.all(color: candidates.isEmpty ? theme.colorScheme.outlineVariant : theme.colorScheme.primary, width: candidates.isEmpty ? 1 : 2),
          borderRadius: BorderRadius.circular(8),
        ),
        child: Padding(
          padding: const EdgeInsets.all(DashboardLayout.pad),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(l.dshBacklog, style: theme.textTheme.titleSmall),
              const SizedBox(height: DashboardLayout.gap),
              Expanded(
                child: Scrollbar(
                  controller: _scroll,
                  child: SingleChildScrollView(
                    controller: _scroll,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        for (final e in errors) Text(e, style: TextStyle(color: theme.colorScheme.error)),
                        for (final r in requirements)
                          ItemRow(key: Key('backlog-req-${r.id}'), item: r.id, lines: [r.id, r.statement]),
                        for (final i in issues)
                          ItemRow(
                            key: Key('backlog-issue-${i.number}'),
                            item: DashboardController.issueItem(i.number),
                            lines: ['#${i.number}', i.title],
                          ),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
