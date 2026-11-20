// Holds: the drop area around the backlog lists (DSH-07.c): a card dropped here leaves the sprint.
// Depends on: DragPayload. Used by: the dashboard page. Reads or writes: nothing.

import 'package:flutter/material.dart';

import 'drag_payload.dart';

/// Wraps [child]; key `backlog-area`. Accepts cards only and calls [onRemove] with the story ID.
class BacklogDropArea extends StatelessWidget {
  const BacklogDropArea({super.key, required this.onRemove, required this.child});

  final ValueChanged<String> onRemove;
  final Widget child;

  @override
  Widget build(BuildContext context) {
    return DragTarget<DragPayload>(
      key: const Key('backlog-area'),
      onWillAcceptWithDetails: (d) => d.data is CardDrag,
      onAcceptWithDetails: (d) => onRemove((d.data as CardDrag).storyId),
      builder: (context, candidates, rejected) => child,
    );
  }
}
