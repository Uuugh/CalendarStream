// Holds: the pure sprint edits (DSH-06.b, DSH-07.a, DSH-07.b, DSH-07.e, DSH-07.f, DSH-10.a, DSH-10.b): add a block,
// move it, add or remove a member, set an estimate or usage, and the derived totals.
// Depends on: Sprint, Block, BlockKind, BlockRules, Member. Used by: the board and the page. Reads or writes: nothing.

import 'block.dart';
import 'block_kind.dart';
import 'block_rules.dart';
import 'member.dart';
import 'sprint.dart';

/// Sprint edits as pure functions. Each returns [Sprint] itself (the same instance) when nothing changes, so a caller
/// writes the file only when the result is not identical to the input (DSH-07.h). Review and retrospective are kept.
class SprintEdit {
  const SprintEdit._();

  /// The ID the next block of [kind] gets: `story-N`, `epic-N` or `sprint-N`, N one above the highest used.
  static String newId(Sprint sprint, BlockKind kind) {
    final prefix = '${kind.name}-';
    var highest = 0;
    for (final b in sprint.blocks) {
      final n = b.id.startsWith(prefix) ? int.tryParse(b.id.substring(prefix.length)) : null;
      if (n != null && n > highest) highest = n;
    }
    return '${kind.name}-${highest + 1}';
  }

  /// Adds a block of [kind] named [name] at the top of the board, with the ID [newId] gives (DSH-06.b). A blank name
  /// changes nothing.
  static Sprint addBlock(Sprint sprint, BlockKind kind, String name) {
    final trimmed = name.trim();
    if (trimmed.isEmpty) return sprint;
    return sprint.copyWith(blocks: [...sprint.blocks, Block(id: newId(sprint, kind), kind: kind, name: trimmed)]);
  }

  /// Why block [id] cannot sit in [newParent] (null is the top), or null when it can (DSH-06.c).
  static String? moveRefusal(Sprint sprint, String id, String? newParent) {
    final block = sprint.block(id);
    if (block == null) return 'no block $id';
    Block? parent;
    if (newParent != null) {
      parent = sprint.block(newParent);
      if (parent == null) return 'no block $newParent';
      if (newParent == id || _ancestors(sprint, newParent).contains(id)) return '$id cannot sit inside itself';
    }
    if (!BlockRules.canNest(block.kind, parent?.kind)) {
      return 'a ${block.kind.name} cannot sit in ${parent == null ? 'the top of the board' : 'a ${parent.kind.name}'}';
    }
    return null;
  }

  /// Moves block [id] into [newParent] (null is the top) (DSH-07.a, DSH-07.b); unchanged when the move is refused
  /// (see [moveRefusal]) or the block already sits there.
  static Sprint moveBlock(Sprint sprint, String id, String? newParent) {
    final block = sprint.block(id);
    if (block == null || moveRefusal(sprint, id, newParent) != null || block.parent == newParent) return sprint;
    return sprint.copyWith(blocks: [
      for (final b in sprint.blocks) b.id == id ? (newParent == null ? b.copyWith(clearParent: true) : b.copyWith(parent: newParent)) : b,
    ]);
  }

  /// Makes [item] a member of story [storyId], removing it from any other story first (DSH-07.e); unchanged when
  /// [storyId] is not a story or already holds it.
  static Sprint addMember(Sprint sprint, String storyId, String item) {
    final story = sprint.block(storyId);
    if (story == null || story.kind != BlockKind.story) return sprint;
    if (sprint.members.any((m) => m.blockId == storyId && m.item == item) &&
        sprint.members.where((m) => m.item == item).length == 1) {
      return sprint;
    }
    final kept = [
      for (final m in sprint.members)
        if (m.item != item) m
    ];
    return sprint.copyWith(members: [...kept, Member(storyId, item)]);
  }

  /// Removes [item] from every story (DSH-07.f); unchanged when no story holds it.
  static Sprint removeMember(Sprint sprint, String item) {
    if (!sprint.members.any((m) => m.item == item)) return sprint;
    return sprint.copyWith(members: [
      for (final m in sprint.members)
        if (m.item != item) m
    ]);
  }

  /// Sets the estimate of story [id] (DSH-10.a); unchanged when it is not a story, the value is negative or not a
  /// number, or the estimate already is [value].
  static Sprint setEstimate(Sprint sprint, String id, double value) =>
      _setPoints(sprint, id, value, (b) => b.estimate, (b) => b.copyWith(estimate: value));

  /// Sets the usage of story [id] (DSH-10.a); unchanged under the same conditions as [setEstimate].
  static Sprint setUsage(Sprint sprint, String id, double value) =>
      _setPoints(sprint, id, value, (b) => b.usage, (b) => b.copyWith(usage: value));

  /// The estimate of block [id]: a story's own, the sum over the stories below a sprint or an epic (DSH-10.b).
  static double estimateOf(Sprint sprint, String id) => _total(sprint, id, (b) => b.estimate);

  /// The usage of block [id], summed the same way (DSH-10.b).
  static double usageOf(Sprint sprint, String id) => _total(sprint, id, (b) => b.usage);

  /// True when block [id] sits, directly or through an epic, in a sprint (DSH-08).
  static bool sitsInSprint(Sprint sprint, String id) =>
      _ancestors(sprint, id).any((a) => sprint.block(a)?.kind == BlockKind.sprint);

  static Sprint _setPoints(
      Sprint sprint, String id, double value, double Function(Block) current, Block Function(Block) change) {
    final block = sprint.block(id);
    if (block == null || block.kind != BlockKind.story || value.isNaN || value < 0 || current(block) == value) {
      return sprint;
    }
    return sprint.copyWith(blocks: [for (final b in sprint.blocks) b.id == id ? change(b) : b]);
  }

  static double _total(Sprint sprint, String id, double Function(Block) points, [Set<String> seen = const {}]) {
    final block = sprint.block(id);
    if (block == null || seen.contains(id)) return 0;
    if (block.kind == BlockKind.story) return points(block);
    var sum = 0.0;
    for (final child in sprint.blocks.where((b) => b.parent == id)) {
      sum += _total(sprint, child.id, points, {...seen, id});
    }
    return sum;
  }

  /// The IDs above [id], nearest first; stops at a loop so a damaged file cannot hang the dashboard.
  static List<String> _ancestors(Sprint sprint, String id) {
    final result = <String>[];
    var parent = sprint.block(id)?.parent;
    while (parent != null && !result.contains(parent)) {
      result.add(parent);
      parent = sprint.block(parent)?.parent;
    }
    return result;
  }
}
