// Holds: the kinds of block and where each may sit (DSH-02.b, DSH-06.c). Depends on: nothing.
// Used by: Block, BlockRules, SprintRepository. Reads or writes: nothing.

/// A story, an epic or a sprint.
enum BlockKind {
  story,
  epic,
  sprint;

  /// The kind named [text] ignoring case and outer spaces, or null.
  static BlockKind? parse(String text) {
    final wanted = text.trim().toLowerCase();
    for (final k in BlockKind.values) {
      if (k.name == wanted) return k;
    }
    return null;
  }
}
