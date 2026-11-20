// Holds: which block may sit in which (DSH-06.c), written once. Depends on: BlockKind.
// Used by: SprintEdit, the board. Reads or writes: nothing.

import 'block_kind.dart';

/// Nesting rules as pure functions.
class BlockRules {
  const BlockRules._();

  /// True when a block of kind [child] may sit in a block of kind [parent] (null is the top of the board): a story in
  /// an epic, a sprint or the top, an epic in a sprint or the top, a sprint at the top only.
  static bool canNest(BlockKind child, BlockKind? parent) => switch (child) {
        BlockKind.story => parent == null || parent == BlockKind.epic || parent == BlockKind.sprint,
        BlockKind.epic => parent == null || parent == BlockKind.sprint,
        BlockKind.sprint => parent == null,
      };
}
