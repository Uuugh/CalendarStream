// Holds: what a drag carries (DSH-07): a backlog item or a board card.
// Depends on: nothing. Used by: BacklogItemTile, StoryCard, SprintBoard, BacklogDropArea.
// Reads or writes: nothing.

/// The data of a drag: a closed family, so it shares this file.
sealed class DragPayload {
  const DragPayload();
}

/// A backlog row: [id] is the requirement ID or `#N` for an issue; [title] its statement or title.
class BacklogDrag extends DragPayload {
  const BacklogDrag({required this.id, required this.title});

  final String id;
  final String title;
}

/// A board card: the ID of its story.
class CardDrag extends DragPayload {
  const CardDrag(this.storyId);

  final String storyId;
}
