// Holds: one backlog row (requirement or issue) that can be dragged onto the board (DSH-07.a).
// Depends on: DragPayload. Used by: the dashboard page. Reads or writes: nothing.

import 'package:flutter/material.dart';

import 'drag_payload.dart';

/// A draggable row for item [id] (requirement ID, or `#N` for an issue); key `backlog-item-<id>`.
class BacklogItemTile extends StatelessWidget {
  const BacklogItemTile({super.key, required this.id, required this.title, required this.subtitle});

  final String id;
  final String title;
  final String subtitle;

  @override
  Widget build(BuildContext context) {
    final tile = ListTile(title: Text(id), subtitle: Text(subtitle));
    return Draggable<DragPayload>(
      key: Key('backlog-item-$id'),
      data: BacklogDrag(id: id, title: title),
      feedback: Material(
        elevation: 4,
        child: ConstrainedBox(constraints: const BoxConstraints(maxWidth: 360), child: tile),
      ),
      childWhenDragging: Opacity(opacity: 0.4, child: tile),
      child: tile,
    );
  }
}
