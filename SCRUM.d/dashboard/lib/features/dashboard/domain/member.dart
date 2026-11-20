// Holds: one Members row of the sprint file (DSH-02.c). Depends on: nothing.
// Used by: Sprint, SprintRepository, SprintEdit. Reads or writes: nothing.

/// [item] (a requirement ID or an issue number written `#N`) is held by the story [blockId].
class Member {
  const Member(this.blockId, this.item);

  final String blockId;
  final String item;

  /// The `#N` form of issue number [number].
  static String issue(int number) => '#$number';
}
