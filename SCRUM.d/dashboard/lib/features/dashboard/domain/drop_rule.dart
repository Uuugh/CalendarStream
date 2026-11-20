// Holds: why a drop on the board is refused when BlockRules and StatusRule do not say (DSH-07.c, DSH-07.g). Depends on:
// Sprint, BlockKind. Used by: the dashboard controller. Reads or writes: nothing.

import 'block_kind.dart';
import 'sprint.dart';

/// Drop rules as pure functions; the reasons are shown as {reason} of msg:dshMoveRefused.
class DropRule {
  const DropRule._();

  /// Why a requirement or an issue cannot be dropped on [targetId] (null is the Backlog block), or null when it can
  /// (DSH-07.c): only the Backlog block and a story take one.
  static String? itemRefusal(Sprint sprint, String? targetId) {
    if (targetId == null) return null;
    final target = sprint.block(targetId);
    if (target == null) return 'no block $targetId';
    if (target.kind != BlockKind.story) return itemTargets;
    return null;
  }

  /// The reason a requirement or an issue is refused where it cannot go (DSH-07.c).
  static const String itemTargets = 'a requirement or an issue can be dropped only on the Backlog block or on a story';

  /// Why a block cannot be dropped on the Backlog block (it holds no blocks).
  static const String blockOnBacklog = 'a block cannot be dropped on the Backlog block';
}
