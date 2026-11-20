// Holds: one block of the sprint file (DSH-02.b). Depends on: BlockKind. Used by: Sprint, SprintRepository,
// SprintEdit, the board. Reads or writes: nothing.

import 'block_kind.dart';

/// A story, an epic or a sprint. [parent] is null at the top of the board; [assignee] is empty when nobody is
/// assigned; [estimate] and [usage] are in usage points (DEF-01).
class Block {
  const Block({
    required this.id,
    required this.kind,
    required this.name,
    this.parent,
    this.assignee = '',
    this.estimate = 0,
    this.usage = 0,
  });

  final String id;
  final BlockKind kind;
  final String name;
  final String? parent;
  final String assignee;
  final double estimate;
  final double usage;

  /// A copy with [parent] replaced; [clearParent] puts it at the top.
  Block copyWith({String? parent, bool clearParent = false, String? name, double? estimate, double? usage}) => Block(
        id: id,
        kind: kind,
        name: name ?? this.name,
        parent: clearParent ? null : (parent ?? this.parent),
        assignee: assignee,
        estimate: estimate ?? this.estimate,
        usage: usage ?? this.usage,
      );
}
