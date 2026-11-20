// Holds: what is dragged on the board (DSH-07): a block or a requirement or an issue. Depends on: nothing.
// Used by: BlockCard, BacklogBlock, BoardView, the rows, DashboardController. Reads or writes: nothing.

/// The data of a drag. A closed family, so both kinds share this file.
sealed class DragPayload {
  const DragPayload();
}

/// A block, by its block ID.
final class BlockDrag extends DragPayload {
  const BlockDrag(this.id);

  final String id;
}

/// A requirement (its ID) or an issue (its number written `#N`, see Member.issue).
final class ItemDrag extends DragPayload {
  const ItemDrag(this.item);

  final String item;
}
