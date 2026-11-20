// Holds: the stages a sprint story passes through (DSH-06), in order.
// Depends on: nothing. Used by: Story, SprintRepository, the board.
// Reads or writes: nothing.

/// The stage of a story: Backlog, Ready, Build, Test, Review or Done, in that order.
enum Stage {
  backlog,
  ready,
  build,
  test,
  review,
  done;

  /// The stage whose name equals [text] ignoring case and outer spaces, or null.
  static Stage? parse(String text) {
    final wanted = text.trim().toLowerCase();
    for (final stage in Stage.values) {
      if (stage.name == wanted) return stage;
    }
    return null;
  }
}
