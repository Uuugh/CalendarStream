// Holds: the board along the top (DSH-06, DSH-07.b, DSH-15): the Backlog block, the add control, the top-level blocks in file order
// in a row that scrolls sideways; the board background takes a block dropped to move it to the top.
// Depends on: DashboardController, BacklogBlock, BlockCard, AddBlockDialog, DragPayload.
// Used by: DashboardPage. Reads or writes: through the controller.

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import 'add_block_dialog.dart';
import 'backlog_block.dart';
import 'block_card.dart';
import 'dashboard_controller.dart';
import 'dashboard_layout.dart';
import 'drag_payload.dart';
import 'drop_feedback.dart';
import 'load_error_text.dart';

/// The board, `Key('board')`; the add control is `Key('add-block-button')`.
class BoardView extends StatefulWidget {
  const BoardView({required this.controller}) : super(key: const Key('board'));

  final DashboardController controller;

  @override
  State<BoardView> createState() => _BoardViewState();
}

class _BoardViewState extends State<BoardView> {
  final ScrollController _scroll = ScrollController();

  @override
  void dispose() {
    _scroll.dispose();
    super.dispose();
  }

  Future<void> _add() async {
    final made = await AddBlockDialog.show(context);
    if (made == null || !mounted) return;
    await DropFeedback.run(context, widget.controller.addBlock(made.kind, made.name));
  }

  @override
  Widget build(BuildContext context) {
    final l = AppLocalizations.of(context);
    final theme = Theme.of(context);
    final controller = widget.controller;
    final sprint = controller.sprint;
    return DragTarget<DragPayload>(
      onWillAcceptWithDetails: (_) => true,
      onAcceptWithDetails: (d) => DropFeedback.run(
        context,
        switch (d.data) {
          BlockDrag b => controller.dropBlock(b.id, null),
          ItemDrag _ => Future.value(controller.dropItemOnBoard()),
        },
      ),
      builder: (context, candidates, _) => LayoutBuilder(
        builder: (context, box) {
          final height = box.maxHeight - 2 * DashboardLayout.pad;
          return Scrollbar(
            controller: _scroll,
            child: SingleChildScrollView(
              controller: _scroll,
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.all(DashboardLayout.pad),
              child: SizedBox(
                height: height < 0 ? 0 : height,
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    SizedBox(width: DashboardLayout.blockWidth, child: BacklogBlock(controller: controller)),
                    Padding(
                      padding: const EdgeInsets.only(left: DashboardLayout.gap),
                      child: FilledButton.icon(
                        key: const Key('add-block-button'),
                        onPressed: sprint == null ? null : _add,
                        icon: const Icon(Icons.add),
                        label: Text(l.dshAddBlock),
                      ),
                    ),
                    if (sprint != null)
                      for (final b in sprint.blocks.where((b) => b.parent == null))
                        Padding(
                          padding: const EdgeInsets.only(left: DashboardLayout.gap),
                          child: SizedBox(
                            width: DashboardLayout.blockWidth,
                            child: BlockCard(key: ValueKey('card-${b.id}'), controller: controller, block: b, bounded: true),
                          ),
                        ),
                    if (controller.sprintError != null)
                      Padding(
                        padding: const EdgeInsets.only(left: DashboardLayout.gap),
                        child: SizedBox(
                          width: DashboardLayout.blockWidth,
                          child: Text(LoadErrorText.of(l, controller.sprintError!), style: TextStyle(color: theme.colorScheme.error)),
                        ),
                      ),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
