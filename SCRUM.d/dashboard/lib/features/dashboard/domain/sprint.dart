// Holds: the sprint (DSH-02): blocks, members, the Review and Retrospective text and the text the dashboard does not
// edit, all kept as written (DSH-02.d, DSH-02.f). Depends on: Block, Member, KeptLine.
// Used by: SprintRepository, SprintEdit, the board. Reads or writes: nothing.

import 'block.dart';
import 'kept_line.dart';
import 'member.dart';

/// The sprint. [review] and [retrospective] are the raw text of those sections. [before] holds the lines above the
/// Blocks heading verbatim (null for a new sprint, which gets the default layout); [blockLines] and [memberLines]
/// are the lines of the two table sections that are not readable rows.
class Sprint {
  const Sprint({
    this.blocks = const [],
    this.members = const [],
    this.review = '',
    this.retrospective = '',
    this.before,
    this.blockLines = const [],
    this.memberLines = const [],
  });

  final List<Block> blocks;
  final List<Member> members;
  final String review;
  final String retrospective;
  final List<String>? before;
  final List<KeptLine> blockLines;
  final List<KeptLine> memberLines;

  /// The block with [id], or null.
  Block? block(String id) {
    for (final b in blocks) {
      if (b.id == id) return b;
    }
    return null;
  }

  /// The items story [blockId] holds, in file order.
  List<String> itemsOf(String blockId) => [
        for (final m in members)
          if (m.blockId == blockId) m.item
      ];

  /// The ID of the story that holds [item], or null.
  String? storyOf(String item) {
    for (final m in members) {
      if (m.item == item) return m.blockId;
    }
    return null;
  }

  Sprint copyWith({List<Block>? blocks, List<Member>? members}) => Sprint(
        blocks: blocks ?? this.blocks,
        members: members ?? this.members,
        review: review,
        retrospective: retrospective,
        before: before,
        blockLines: blockLines,
        memberLines: memberLines,
      );
}
