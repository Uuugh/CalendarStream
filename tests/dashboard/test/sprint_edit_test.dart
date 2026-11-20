// Tests the pure sprint edits (SprintEdit) and what they rest on: DSH-06.c (nesting), DSH-06.b (adding a block),
// DSH-07.a/b/c/e/f/h (moves and membership), DSH-08.b (a story sits in a sprint), DSH-10.a/b (estimate and usage).
// One run covers each ID named in the test name.
import 'package:dashboard/features/dashboard/domain/block.dart';
import 'package:dashboard/features/dashboard/domain/block_kind.dart';
import 'package:dashboard/features/dashboard/domain/member.dart';
import 'package:dashboard/features/dashboard/domain/points_format.dart';
import 'package:dashboard/features/dashboard/domain/sprint.dart';
import 'package:dashboard/features/dashboard/domain/sprint_edit.dart';
import 'package:flutter_test/flutter_test.dart';

const base = Sprint(
  review: 'R',
  retrospective: 'T',
  blocks: [
    Block(id: 'sprint-1', kind: BlockKind.sprint, name: 'Sprint'),
    Block(id: 'epic-1', kind: BlockKind.epic, name: 'Epic', parent: 'sprint-1'),
    Block(id: 'story-1', kind: BlockKind.story, name: 'One', parent: 'epic-1', estimate: 3, usage: 1.5),
    Block(id: 'story-2', kind: BlockKind.story, name: 'Two', parent: 'sprint-1', estimate: 2, usage: 4),
    Block(id: 'story-3', kind: BlockKind.story, name: 'Loose', estimate: 1),
    Block(id: 'epic-2', kind: BlockKind.epic, name: 'Top epic'),
  ],
  members: [Member('story-1', 'AAA-01'), Member('story-2', '#7')],
);

String parentOf(Sprint s, String id) => s.block(id)?.parent ?? '(top)';

void main() {
  group('reading a sprint', () {
    test('DSH-06.d: itemsOf lists the items of a story in order, storyOf finds the story of an item', () {
      final s = SprintEdit.addMember(base, 'story-1', 'AAA-03');
      expect(s.itemsOf('story-1'), ['AAA-01', 'AAA-03']);
      expect(s.itemsOf('story-3'), isEmpty);
      expect(s.storyOf('#7'), 'story-2');
      expect(s.storyOf('AAA-09'), isNull);
    });

    test('DSH-02.c: an issue member is written #N', () => expect(Member.issue(7), '#7'));
  });

  group('adding a block (DSH-06.b)', () {
    test('DSH-06.b: newId is kind-1 for the first block of a kind and one above the highest number after that', () {
      expect(SprintEdit.newId(const Sprint(), BlockKind.story), 'story-1');
      expect(SprintEdit.newId(base, BlockKind.story), 'story-4');
      expect(SprintEdit.newId(base, BlockKind.epic), 'epic-3');
      expect(SprintEdit.newId(base, BlockKind.sprint), 'sprint-2');
      const gap = Sprint(blocks: [Block(id: 'story-7', kind: BlockKind.story, name: 'x'), Block(id: 'story-x', kind: BlockKind.story, name: 'y')]);
      expect(SprintEdit.newId(gap, BlockKind.story), 'story-8');
    });

    test('DSH-06.b: addBlock adds the block at the top of the board with the trimmed name and keeps the rest', () {
      final s = SprintEdit.addBlock(base, BlockKind.epic, '  New epic  ');
      final added = s.blocks.last;
      expect([added.id, added.kind, added.name, added.parent], ['epic-3', BlockKind.epic, 'New epic', null]);
      expect(s.blocks, hasLength(base.blocks.length + 1));
      expect([s.review, s.retrospective, s.members.length], ['R', 'T', 2]);
      expect(base.blocks, hasLength(6), reason: 'the old sprint is not changed');
    });

    test('DSH-06.b: a blank name adds nothing and returns the same sprint', () {
      expect(SprintEdit.addBlock(base, BlockKind.story, '   '), same(base));
    });
  });

  group('nesting and moving blocks (DSH-06.c, DSH-07.a, DSH-07.b)', () {
    test('DSH-07.a: a story is dragged onto an epic and onto a sprint, and then sits there', () {
      expect(parentOf(SprintEdit.moveBlock(base, 'story-3', 'epic-1'), 'story-3'), 'epic-1');
      expect(parentOf(SprintEdit.moveBlock(base, 'story-3', 'sprint-1'), 'story-3'), 'sprint-1');
      expect(parentOf(SprintEdit.moveBlock(base, 'story-1', 'sprint-1'), 'story-1'), 'sprint-1');
    });

    test('DSH-07.a: an epic is dragged onto a sprint', () {
      expect(parentOf(SprintEdit.moveBlock(base, 'epic-2', 'sprint-1'), 'epic-2'), 'sprint-1');
      expect(SprintEdit.moveRefusal(base, 'epic-2', 'sprint-1'), isNull);
    });

    test('DSH-07.b: a block is dragged to the top of the board and then sits there if it may', () {
      expect(parentOf(SprintEdit.moveBlock(base, 'story-1', null), 'story-1'), '(top)');
      expect(parentOf(SprintEdit.moveBlock(base, 'epic-1', null), 'epic-1'), '(top)');
      expect(SprintEdit.moveRefusal(base, 'sprint-1', null), isNull);
    });

    test('DSH-06.c and DSH-07.a: a block that may not sit there is refused with a reason and nothing changes', () {
      for (final c in [
        ['epic-2', 'story-1'], ['epic-2', 'epic-1'], ['sprint-1', 'epic-1'], ['story-3', 'story-1'], ['sprint-1', 'sprint-1'],
      ]) {
        expect(SprintEdit.moveRefusal(base, c[0], c[1]), isNotNull, reason: '${c[0]} into ${c[1]}');
        expect(SprintEdit.moveBlock(base, c[0], c[1]), same(base), reason: '${c[0]} into ${c[1]}');
      }
    });

    test('DSH-07.a: a block cannot sit inside itself or inside what sits in it', () {
      expect(SprintEdit.moveRefusal(base, 'epic-1', 'epic-1'), isNotNull);
      expect(SprintEdit.moveRefusal(base, 'sprint-1', 'story-1'), isNotNull);
    });

    test('DSH-07.a: a block or a target that does not exist is refused', () {
      expect(SprintEdit.moveRefusal(base, 'nope', 'sprint-1'), isNotNull);
      expect(SprintEdit.moveRefusal(base, 'story-1', 'nope'), isNotNull);
      expect(SprintEdit.moveBlock(base, 'nope', null), same(base));
    });

    test('DSH-07.h: moving a block where it already is returns the same sprint', () {
      expect(SprintEdit.moveBlock(base, 'story-1', 'epic-1'), same(base));
      expect(SprintEdit.moveBlock(base, 'story-3', null), same(base));
      expect(SprintEdit.moveBlock(base, 'sprint-1', null), same(base));
    });

    test('DSH-07.a: a move keeps every other block, the members, the review and the retrospective', () {
      final s = SprintEdit.moveBlock(base, 'story-3', 'epic-1');
      expect(s.blocks.map((b) => b.id), base.blocks.map((b) => b.id));
      expect(s.block('story-3')!.estimate, 1);
      expect(s.members, base.members);
      expect([s.review, s.retrospective], ['R', 'T']);
    });
  });

  group('members (DSH-07.c, DSH-07.e, DSH-07.f, DSH-07.h)', () {
    test('DSH-07.e: an item dropped on a story is recorded in that story', () {
      final s = SprintEdit.addMember(base, 'story-3', 'AAA-02');
      expect(s.itemsOf('story-3'), ['AAA-02']);
      expect(s.storyOf('AAA-02'), 'story-3');
    });

    test('DSH-07.e: an item that is in another story moves to the new one, and sits in one story only', () {
      final s = SprintEdit.addMember(base, 'story-2', 'AAA-01');
      expect(s.storyOf('AAA-01'), 'story-2');
      expect(s.members.where((m) => m.item == 'AAA-01'), hasLength(1));
      expect(s.itemsOf('story-1'), isEmpty);
    });

    test('DSH-07.h: dropping an item on the story it is already in returns the same sprint', () {
      expect(SprintEdit.addMember(base, 'story-1', 'AAA-01'), same(base));
    });

    test('DSH-07.c: an item can be dropped on a story only: an epic, a sprint or a missing block takes nothing', () {
      expect(SprintEdit.addMember(base, 'epic-1', 'AAA-02'), same(base));
      expect(SprintEdit.addMember(base, 'sprint-1', 'AAA-02'), same(base));
      expect(SprintEdit.addMember(base, 'nope', 'AAA-02'), same(base));
    });

    test('DSH-07.f: an item taken out of its story (dropped on the Backlog block) is removed from the Members rows', () {
      final s = SprintEdit.removeMember(base, 'AAA-01');
      expect(s.storyOf('AAA-01'), isNull);
      expect(s.itemsOf('story-1'), isEmpty);
      expect(s.storyOf('#7'), 'story-2');
    });

    test('DSH-07.h: removing an item that is in no story returns the same sprint', () {
      expect(SprintEdit.removeMember(base, 'AAA-99'), same(base));
    });
  });

  group('estimate and usage (DSH-10.a, DSH-10.b)', () {
    test('DSH-10.a: setEstimate and setUsage change that story only and keep the rest', () {
      final e = SprintEdit.setEstimate(base, 'story-1', 5);
      expect(e.block('story-1')!.estimate, 5);
      expect(e.block('story-1')!.usage, 1.5);
      expect(e.block('story-2'), same(base.block('story-2')));
      expect([e.review, e.retrospective], ['R', 'T']);
      final u = SprintEdit.setUsage(base, 'story-3', 2.5);
      expect(u.block('story-3')!.usage, 2.5);
    });

    test('DSH-10.a: only a story takes points; a missing block, a negative or NaN value or an unchanged value changes nothing', () {
      expect(SprintEdit.setEstimate(base, 'epic-1', 1), same(base));
      expect(SprintEdit.setUsage(base, 'sprint-1', 1), same(base));
      expect(SprintEdit.setEstimate(base, 'nope', 1), same(base));
      expect(SprintEdit.setEstimate(base, 'story-1', -1), same(base));
      expect(SprintEdit.setUsage(base, 'story-1', double.nan), same(base));
      expect(SprintEdit.setEstimate(base, 'story-1', 3), same(base));
      expect(SprintEdit.setUsage(base, 'story-1', 1.5), same(base));
    });

    test('DSH-10.b: an epic and a sprint show the sums of the stories below them', () {
      expect(SprintEdit.estimateOf(base, 'epic-1'), 3);
      expect(SprintEdit.usageOf(base, 'epic-1'), 1.5);
      expect(SprintEdit.estimateOf(base, 'sprint-1'), 5, reason: 'story-1 in the epic plus story-2');
      expect(SprintEdit.usageOf(base, 'sprint-1'), 5.5);
    });

    test('DSH-10.b: a story shows its own points; an empty epic and a missing block show 0', () {
      expect(SprintEdit.estimateOf(base, 'story-2'), 2);
      expect(SprintEdit.usageOf(base, 'story-2'), 4);
      expect(SprintEdit.estimateOf(base, 'epic-2'), 0);
      expect(SprintEdit.usageOf(base, 'nope'), 0);
    });

    test('DSH-10.b: the sums follow a change', () {
      final s = SprintEdit.moveBlock(SprintEdit.setUsage(base, 'story-3', 10), 'story-3', 'sprint-1');
      expect(SprintEdit.usageOf(s, 'sprint-1'), 15.5);
      expect(SprintEdit.estimateOf(s, 'sprint-1'), 6);
    });

    test('DSH-10.a: points are formatted without a trailing zero and parsed with a comma or spaces; bad values are null', () {
      expect(PointsFormat.format(3.0), '3');
      expect(PointsFormat.format(1.5), '1.5');
      expect(PointsFormat.parse(' 2,5 '), 2.5);
      expect(PointsFormat.parse('4'), 4);
      expect(PointsFormat.parse('-1'), isNull);
      expect(PointsFormat.parse('abc'), isNull);
      expect(PointsFormat.parse(''), isNull);
      expect(PointsFormat.parse('NaN'), isNull);
      expect(PointsFormat.parse('Infinity'), isNull);
    });
  });

  group('sits in a sprint (DSH-08, DSH-08.b)', () {
    test('DSH-08: a story in an epic in a sprint, and a story directly in a sprint, sit in a sprint', () {
      expect(SprintEdit.sitsInSprint(base, 'story-1'), isTrue);
      expect(SprintEdit.sitsInSprint(base, 'story-2'), isTrue);
    });

    test('DSH-08.b: a story at the top, or in an epic at the top, does not sit in a sprint', () {
      expect(SprintEdit.sitsInSprint(base, 'story-3'), isFalse);
      final s = SprintEdit.moveBlock(base, 'story-3', 'epic-2');
      expect(SprintEdit.sitsInSprint(s, 'story-3'), isFalse);
    });

    test('DSH-08.b: a missing block does not sit in a sprint', () {
      expect(SprintEdit.sitsInSprint(base, 'nope'), isFalse);
    });
  });
}
