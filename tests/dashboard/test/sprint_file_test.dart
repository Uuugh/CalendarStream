// Tests DSH-02 (a-f): the sprint file, read and written by SprintRepository and through LocalBackend; and DSH-01.f for
// the sprint file (an unreadable file gives a reason and the other loads keep working).
// One run covers each ID named in the test name.
import 'dart:io';

import 'package:dashboard/features/dashboard/data/local_backend.dart';
import 'package:dashboard/features/dashboard/data/sprint_repository.dart';
import 'package:dashboard/features/dashboard/domain/block.dart';
import 'package:dashboard/features/dashboard/domain/block_kind.dart';
import 'package:dashboard/features/dashboard/domain/member.dart';
import 'package:dashboard/features/dashboard/domain/sprint.dart';
import 'package:dashboard/features/dashboard/domain/sprint_edit.dart';
import 'package:flutter_test/flutter_test.dart';

import '../support/failing_file_access.dart';
import '../support/fixtures.dart';
import '../support/memory_file_access.dart';

const rich = '''Preamble above the title.

# Sprint

Intro note.

## Blocks

A note above the Blocks table.

| id | kind | name | parent | assignee | estimate | usage |
|---|---|---|---|---|---|---|
| sprint-1 | sprint | Spr |  |  | 0 | 0 |
| story-1 | story | First | sprint-1 | Ann | 3 | 1.5 |
| a row that cannot be read |
| x-9 | feature | Unknown kind | | | | |
| story-2 | story | Second | sprint-1 |  | 2 | 0 |

Trailing note of the Blocks.

## Members

A note above the Members table.

| story | item |
|---|---|
| story-1 | AAA-01 |
| not a member row |
| story-2 | #7 |

## Review

Review text.

## Lessons

A heading that is not a section.

## Members

Not the table: an earlier section's heading, inside the review.

## Retrospective

Retro text.

## Review

An earlier section's heading, inside the retrospective.

### Sub heading

## Another heading
''';

String again(String text) => SprintRepository.format(SprintRepository.parse(text));

String summary(Sprint s) =>
    '${s.blocks.map((b) => [b.id, b.kind.name, b.name, b.parent, b.assignee, b.estimate, b.usage])}|'
    '${s.members.map((m) => '${m.blockId}:${m.item}')}|${s.review}|${s.retrospective}';

void main() {
  const path = '/r/SCRUM.d/sprint.md';

  group('the file layout (DSH-02.a, DSH-02.b, DSH-02.c)', () {
    test('DSH-02.a: the Blocks table, the Members table, the Review and the Retrospective are read', () {
      final s = SprintRepository.parse(sampleSprintFile);
      expect(s.blocks, hasLength(4));
      expect(s.members, hasLength(3));
      expect(s.review, 'Looked fine.');
      expect(s.retrospective, 'Do more of X.');
    });

    test('DSH-02.a: a written file has the four parts in order', () {
      final text = SprintRepository.format(const Sprint(review: 'R', retrospective: 'T'));
      final at = ['## Blocks', '## Members', '## Review', '## Retrospective'].map(text.indexOf).toList();
      expect(at, everyElement(greaterThanOrEqualTo(0)));
      expect([...at]..sort(), at);
    });

    test('DSH-02.b: a Blocks row gives block ID, kind, name, parent, assignee, estimate and usage', () {
      final s = SprintRepository.parse(sampleSprintFile);
      final b = s.block('story-1')!;
      expect([b.id, b.kind, b.name, b.parent, b.assignee, b.estimate, b.usage],
          ['story-1', BlockKind.story, 'First story', 'epic-1', 'Ann', 3.0, 1.5]);
      final top = s.block('sprint-1')!;
      expect(top.parent, isNull, reason: 'a blank parent is the top of the board');
      expect(top.kind, BlockKind.sprint);
      expect(s.block('epic-1')!.kind, BlockKind.epic);
    });

    test('DSH-02.b: a blank assignee reads as empty; missing or bad points read as 0', () {
      final s = SprintRepository.parse('## Blocks\n\n| id | kind | name | parent | assignee | estimate | usage |\n|---|---|---|---|---|---|---|\n| story-1 | story | A |  |  | x |  |\n| story-2 | Story | B |\n');
      expect(s.block('story-1')!.assignee, '');
      expect([s.block('story-1')!.estimate, s.block('story-1')!.usage], [0, 0]);
      expect(s.block('story-2')!.kind, BlockKind.story);
      expect(s.block('story-2')!.parent, isNull);
    });

    test('DSH-02.c: a Members row gives a story block ID and one item, a requirement ID or #N', () {
      final s = SprintRepository.parse(sampleSprintFile);
      expect(s.members.map((m) => [m.blockId, m.item]), [['story-1', 'AAA-01'], ['story-1', 'AAA-03'], ['story-2', '#7']]);
    });

    test('DSH-02.b and DSH-02.c: blocks and members round trip through format and parse, including a pipe in a name', () {
      const sprint = Sprint(
        blocks: [
          Block(id: 'sprint-1', kind: BlockKind.sprint, name: 'S'),
          Block(id: 'story-9', kind: BlockKind.story, name: 'A | B', parent: 'sprint-1', assignee: 'Bo', estimate: 4, usage: 2.5),
        ],
        members: [Member('story-9', 'AAA-01'), Member('story-9', '#3')],
        review: 'R',
        retrospective: 'T',
      );
      final back = SprintRepository.parse(SprintRepository.format(sprint));
      expect(summary(back), summary(sprint));
    });

    test('DSH-02.a: a block whose ID repeats is kept as a line and not as a second block', () {
      final s = SprintRepository.parse('## Blocks\n\n| id | kind | name | parent | assignee | estimate | usage |\n|---|---|---|---|---|---|---|\n| story-1 | story | A |  |  | 1 | 0 |\n| story-1 | story | B |  |  | 2 | 0 |\n');
      expect(s.blocks, hasLength(1));
      expect(s.blocks.single.name, 'A');
    });

    test('DSH-02.a: a file with CRLF line endings is read the same', () {
      expect(summary(SprintRepository.parse(sampleSprintFile.replaceAll('\n', '\r\n'))), summary(SprintRepository.parse(sampleSprintFile)));
    });
  });

  group('every change is written at once (DSH-02.d)', () {
    test('DSH-02.d: a change saved through LocalBackend is in the file and the review and retrospective are kept', () async {
      final files = MemoryFileAccess(memoryFiles());
      final backend = LocalBackend(files: files, runner: FakeRunner(createdIssue12), repoRoot: memRoot);
      final loaded = await backend.loadSprint();
      await backend.saveSprint(SprintEdit.setUsage(SprintEdit.moveBlock(loaded, 'story-2', 'epic-1'), 'story-2', 3));
      expect(files.writes, [memSprintPath]);
      final again = SprintRepository.parse(files.files[memSprintPath]!);
      expect(again.block('story-2')!.parent, 'epic-1');
      expect(again.block('story-2')!.usage, 3);
      expect(again.review, 'Looked fine.');
      expect(again.retrospective, 'Do more of X.');
      expect((await backend.loadSprint()).members.map((m) => m.item), ['AAA-01', 'AAA-03', '#7']);
    });

    test('DSH-02.d: multi-line review and retrospective text, with a pipe and a list, is kept as it was', () {
      const review = 'Line one.\n\nLine two with | a pipe.';
      const retro = '- keep\n- change';
      final back = SprintRepository.parse(SprintRepository.format(const Sprint(review: review, retrospective: retro)));
      expect(back.review, review);
      expect(back.retrospective, retro);
    });

    test('DSH-02.d: every successive change reaches the file, one write each', () async {
      final files = MemoryFileAccess(memoryFiles(sprint: null));
      final backend = LocalBackend(files: files, runner: FakeRunner(createdIssue12), repoRoot: memRoot);
      var s = await backend.loadSprint();
      for (final step in [
        (Sprint x) => SprintEdit.addBlock(x, BlockKind.sprint, 'S'),
        (Sprint x) => SprintEdit.addBlock(x, BlockKind.story, 'T'),
        (Sprint x) => SprintEdit.moveBlock(x, 'story-1', 'sprint-1'),
        (Sprint x) => SprintEdit.addMember(x, 'story-1', 'AAA-01'),
      ]) {
        s = step(s);
        await backend.saveSprint(s);
        expect(summary(SprintRepository.parse(files.files[memSprintPath]!)), summary(s));
      }
      expect(files.writes, hasLength(4));
    });
  });

  group('no file (DSH-02.e)', () {
    test('DSH-02.e: when the file does not exist the sprint is empty', () async {
      final files = MemoryFileAccess(memoryFiles(sprint: null));
      final s = await SprintRepository(files: files, path: memSprintPath).load();
      expect([s.blocks, s.members, s.review, s.retrospective], [isEmpty, isEmpty, '', '']);
      expect(files.files.containsKey(memSprintPath), isFalse, reason: 'reading does not create the file');
    });

    test('DSH-02.e: the first change creates the file, on disk, with its folder', () async {
      final repo = makeRepo();
      addTearDown(() => repo.deleteSync(recursive: true));
      final p = join(repo, 'SCRUM.d/sprint.md');
      final r = SprintRepository(files: disk, path: p);
      expect(File(p).existsSync(), isFalse);
      await r.save(SprintEdit.addBlock(await r.load(), BlockKind.sprint, 'New'));
      expect(File(p).existsSync(), isTrue);
      expect((await r.load()).blocks.single.id, 'sprint-1');
    });
  });

  group('what the dashboard does not edit (DSH-02.f)', () {
    test('DSH-02.f: text before the first table, other sections, headings inside the Review or Retrospective and unreadable rows come back in their places', () {
      final out = again(rich);
      var from = 0;
      for (final line in [
        'Preamble above the title.', '# Sprint', 'Intro note.', '## Blocks', 'A note above the Blocks table.',
        '| sprint-1 |', '| story-1 |', '| a row that cannot be read |', '| x-9 | feature | Unknown kind |', '| story-2 |',
        'Trailing note of the Blocks.', '## Members', 'A note above the Members table.', '| story-1 | AAA-01 |',
        '| not a member row |', '| story-2 | #7 |', '## Review', 'Review text.', '## Lessons', 'A heading that is not a section.',
        "Not the table: an earlier section's heading, inside the review.", '## Retrospective', 'Retro text.',
        "An earlier section's heading, inside the retrospective.", '### Sub heading', '## Another heading',
      ]) {
        final at = out.indexOf(line, from);
        expect(at, greaterThanOrEqualTo(from), reason: 'missing or out of order: $line\n$out');
        from = at;
      }
      expect(out, contains('## Members\n\nNot the table'));
      expect(out, contains('## Review\n\nAn earlier section'));
    });

    test('DSH-02.f: only an exact heading that comes later in the order ends a section', () {
      final s = SprintRepository.parse(rich);
      expect(s.review, contains('## Lessons'));
      expect(s.review, contains('## Members'));
      expect(s.review, isNot(contains('Retro text.')));
      expect(s.retrospective, contains('## Review'));
      expect(s.retrospective, contains('## Another heading'));
      expect(s.blocks.map((b) => b.id), ['sprint-1', 'story-1', 'story-2']);
      expect(s.members.map((m) => m.item), ['AAA-01', '#7']);
    });

    test('DSH-02.f: a row that cannot be read stays where it stood, between its neighbours', () {
      final out = again(rich);
      final bad = out.indexOf('| a row that cannot be read |');
      expect(bad, greaterThan(out.indexOf('| story-1 | story |')));
      expect(bad, lessThan(out.indexOf('| story-2 | story |')));
      final member = out.indexOf('| not a member row |');
      expect(member, greaterThan(out.indexOf('| story-1 | AAA-01 |')));
      expect(member, lessThan(out.indexOf('| story-2 | #7 |')));
    });

    test('DSH-02.f: formatting twice changes nothing more, and every field survives', () {
      final once = again(rich);
      expect(again(once), once);
      expect(summary(SprintRepository.parse(once)), summary(SprintRepository.parse(rich)));
    });

    test('DSH-02.f and DSH-02.d: a change keeps everything it does not edit', () async {
      final files = MemoryFileAccess({memSprintPath: rich});
      final backend = LocalBackend(files: files, runner: FakeRunner(createdIssue12), repoRoot: memRoot);
      await backend.saveSprint(SprintEdit.setUsage(await backend.loadSprint(), 'story-1', 2));
      final text = files.files[memSprintPath]!;
      for (final line in [
        'Preamble above the title.', 'Intro note.', 'A note above the Blocks table.', '| a row that cannot be read |',
        'Trailing note of the Blocks.', '| not a member row |', '## Lessons', '### Sub heading',
      ]) {
        expect(text, contains(line));
      }
      expect(SprintRepository.parse(text).block('story-1')!.usage, 2);
    });

    test('DSH-02.f: a sprint that was never loaded is written in the default layout and read back', () {
      final out = SprintRepository.format(SprintEdit.addBlock(const Sprint(), BlockKind.story, 'New'));
      expect(out, contains('## Blocks'));
      expect(SprintRepository.parse(out).blocks.single.id, 'story-1');
    });
  });

  group('an unreadable file (DSH-01.f)', () {
    test('DSH-01.f: an unreadable sprint file fails with its reason and the requirements still load', () async {
      final inner = MemoryFileAccess(memoryFiles());
      final files = FailingFileAccess(inner, failsOn: (p) => p == path || p == memSprintPath, reason: 'disk gone');
      final backend = LocalBackend(files: files, runner: FakeRunner(createdIssue12), repoRoot: memRoot);
      await expectLater(backend.loadSprint(), throwsA(predicate((e) => '$e'.contains('disk gone'))));
      expect(await backend.loadRequirements(), isNotEmpty);
    });

    test('DSH-01.f: an unreadable requirements folder fails with its reason and the sprint still loads', () async {
      final inner = MemoryFileAccess(memoryFiles());
      final files = FailingFileAccess(inner, failsOn: (p) => p.startsWith(memRequirementsDir), reason: 'no access');
      final backend = LocalBackend(files: files, runner: FakeRunner(createdIssue12), repoRoot: memRoot);
      await expectLater(backend.loadRequirements(), throwsA(predicate((e) => '$e'.contains('no access'))));
      expect((await backend.loadSprint()).blocks, hasLength(4));
    });
  });
}
