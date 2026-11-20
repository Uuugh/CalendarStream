// Tests DSH-02 (a-d): the sprint file. One run covers each ID named in the test name.
import 'dart:io';

import 'package:dashboard/features/dashboard/data/sprint_repository.dart';
import 'package:dashboard/features/dashboard/domain/sprint.dart';
import 'package:dashboard/features/dashboard/domain/sprint_edit.dart';
import 'package:dashboard/features/dashboard/domain/stage.dart';
import 'package:dashboard/features/dashboard/domain/story.dart';
import 'package:flutter_test/flutter_test.dart';

import '../support/fixtures.dart';
import '../support/memory_file_access.dart';

void main() {
  late Directory repo;
  late String path;
  SprintRepository repoFor() => SprintRepository(files: disk, path: path);

  setUp(() {
    repo = makeRepo();
    path = join(repo, 'SCRUM.d/sprint.md');
  });
  tearDown(() => repo.deleteSync(recursive: true));

  test('DSH-02.a: file with Goal line, Stories table, Review and Retrospective is read', () async {
    writeFile(repo, 'SCRUM.d/sprint.md', sampleSprintFile);
    final s = await repoFor().load();
    expect(s.goal, 'Ship the demo board');
    expect(s.stories, hasLength(2));
    expect(s.review.trim(), 'Looked fine.');
    expect(s.retrospective.trim(), 'Do more of X.');
  });

  test('DSH-02.a: saved file has the four parts', () async {
    await repoFor().save(const Sprint(goal: 'G', review: 'R', retrospective: 'T'));
    final text = File(path).readAsStringSync();
    expect(text, contains('Goal: G'));
    expect(text, contains('## Stories'));
    expect(text, contains('## Review'));
    expect(text, contains('## Retrospective'));
  });

  test('DSH-02.b: a Stories row yields id, title, items, stage, assignee, estimate, usage', () async {
    writeFile(repo, 'SCRUM.d/sprint.md', sampleSprintFile);
    final s = (await repoFor().load()).stories.first;
    expect(s.id, 'S-1');
    expect(s.title, 'First story');
    expect(s.items, ['AAA-01', 'AAA-02']);
    expect(s.stage, Stage.build);
    expect(s.assignee, 'Ann');
    expect(s.estimate, 3.0);
    expect(s.usage, 1.5);
  });

  test('DSH-02.b: a row with blank assignee reads as empty assignee', () async {
    writeFile(repo, 'SCRUM.d/sprint.md', sampleSprintFile);
    final s = (await repoFor().load()).stories[1];
    expect(s.assignee, '');
    expect(s.stage, Stage.backlog);
    expect(s.items, ['#7']);
  });

  test('DSH-02.b: story round-trips through save and load', () async {
    const story = Story(
        id: 'X-9', title: 'Round trip', items: ['AAA-01', '#3'], stage: Stage.review, assignee: 'Bo', estimate: 4, usage: 2.5);
    await repoFor().save(const Sprint(goal: 'G', stories: [story]));
    final back = (await repoFor().load()).stories.single;
    expect(back.id, 'X-9');
    expect(back.title, 'Round trip');
    expect(back.items, ['AAA-01', '#3']);
    expect(back.stage, Stage.review);
    expect(back.assignee, 'Bo');
    expect(back.estimate, 4.0);
    expect(back.usage, 2.5);
  });

  test('DSH-02.c: a change is written to the file and goal, review and retrospective are kept', () async {
    writeFile(repo, 'SCRUM.d/sprint.md', sampleSprintFile);
    final r = repoFor();
    final loaded = await r.load();
    final first = loaded.stories.first;
    final changed = Sprint(
      goal: loaded.goal,
      review: loaded.review,
      retrospective: loaded.retrospective,
      stories: [
        Story(id: first.id, title: first.title, items: first.items, stage: Stage.done, assignee: first.assignee, estimate: first.estimate, usage: 3),
        ...loaded.stories.skip(1),
      ],
    );
    await r.save(changed);
    final again = await repoFor().load();
    expect(again.stories.first.stage, Stage.done);
    expect(again.stories.first.usage, 3.0);
    expect(again.goal, 'Ship the demo board');
    expect(again.review.trim(), 'Looked fine.');
    expect(again.retrospective.trim(), 'Do more of X.');
  });

  test('DSH-02.c: multi-line review and retrospective text is kept as it was', () async {
    const review = 'Line one.\n\nLine two with | a pipe.';
    const retro = '- keep\n- change';
    await repoFor().save(const Sprint(goal: 'G', review: review, retrospective: retro));
    final back = await repoFor().load();
    expect(back.review.trim(), review);
    expect(back.retrospective.trim(), retro);
  });

  test('DSH-02.d: missing file loads as an empty sprint', () async {
    final s = await repoFor().load();
    expect(s.stories, isEmpty);
    expect(s.goal, '');
    expect(s.review, '');
    expect(s.retrospective, '');
    expect(File(path).existsSync(), isFalse);
  });

  test('DSH-02.d: the first change creates the file', () async {
    expect(File(path).existsSync(), isFalse);
    await repoFor().save(const Sprint(stories: [Story(id: 'N-1', title: 'New')]));
    expect(File(path).existsSync(), isTrue);
    expect((await repoFor().load()).stories.single.id, 'N-1');
  });

  group('what the dashboard does not edit (DSH-02.e) and round trips (DSH-02.c)', () {
    const rich = '''Preamble above the title.

# Sprint

Intro note.

Goal: Keep goals

Note after the goal.

## Stories

A note above the table.

| story | title | items | stage | assignee | estimate | usage |
|---|---|---|---|---|---|---|
| S-1 | First | AAA-01 | Build | Ann | 3 | 1.5 |
| a row that cannot be read |
| S-2 | Second | #7 | Ready |  | 2 | 0 |

Trailing note of the stories.

## Review

Review text.

## Lessons

A heading that is not a section.

## Stories

Not the table: an earlier section's heading, inside the review.

## Retrospective

Retro text.

## Review

An earlier section's heading, inside the retrospective.

### Sub heading

## Another heading
''';

    String again(String text) => SprintRepository.format(SprintRepository.parse(text));

    void sameSprint(Sprint a, Sprint b) {
      expect(a.goal, b.goal);
      expect(a.review, b.review);
      expect(a.retrospective, b.retrospective);
      expect(a.stories.map((s) => [s.id, s.title, s.items, s.stage, s.assignee, s.estimate, s.usage]),
          b.stories.map((s) => [s.id, s.title, s.items, s.stage, s.assignee, s.estimate, s.usage]));
    }

    test('DSH-02.e: text before the Goal line, between it and Stories, other lines and headings are written back as they were', () {
      final out = again(rich);
      var from = 0;
      for (final line in [
        'Preamble above the title.', '# Sprint', 'Intro note.', 'Goal: Keep goals', 'Note after the goal.', '## Stories',
        'A note above the table.', '| S-1 | First |', '| a row that cannot be read |', '| S-2 | Second |',
        'Trailing note of the stories.', '## Review', 'Review text.', '## Lessons', 'A heading that is not a section.',
        'Not the table: an earlier section\'s heading, inside the review.', '## Retrospective', 'Retro text.',
        'An earlier section\'s heading, inside the retrospective.', '### Sub heading', '## Another heading',
      ]) {
        final at = out.indexOf(line, from);
        expect(at, greaterThanOrEqualTo(from), reason: 'missing or out of order: $line\n$out');
        from = at;
      }
      expect(out, contains('## Stories\n\nNot the table'));
      expect(out, contains('## Review\n\nAn earlier section'));
    });

    test('DSH-02.e: only an exact heading that comes later in the order ends a section', () {
      final s = SprintRepository.parse(rich);
      expect(s.review, contains('## Lessons'));
      expect(s.review, contains('## Stories'));
      expect(s.review, isNot(contains('Retro text.')));
      expect(s.retrospective, contains('## Review'));
      expect(s.retrospective, contains('## Another heading'));
      expect(s.stories.map((x) => x.id), ['S-1', 'S-2']);
    });

    test('DSH-02.e: a story row it cannot read is kept where it stood', () {
      final s = SprintRepository.parse(rich);
      expect(s.keptLines.map((k) => k.text), contains('| a row that cannot be read |'));
      final out = again(rich);
      final bad = out.indexOf('| a row that cannot be read |');
      expect(bad, greaterThan(out.indexOf('| S-1 |')));
      expect(bad, lessThan(out.indexOf('| S-2 |')));
    });

    test('DSH-02.e and DSH-02.c: formatting twice changes nothing more (a round trip is stable) and keeps every field', () {
      final once = again(rich);
      expect(again(once), once);
      sameSprint(SprintRepository.parse(once), SprintRepository.parse(rich));
    });

    test('DSH-02.c: a change to one story keeps the goal, the review, the retrospective and everything it does not edit', () {
      final changed = SprintEdit.moveStory(SprintRepository.parse(rich), 'S-2', Stage.done);
      final out = SprintRepository.format(changed);
      expect(SprintRepository.parse(out).stories.last.stage, Stage.done);
      for (final line in ['Preamble above the title.', 'Intro note.', 'Note after the goal.', 'A note above the table.', '| a row that cannot be read |', 'Trailing note of the stories.', 'A heading that is not a section.', '### Sub heading']) {
        expect(out, contains(line));
      }
      final back = SprintRepository.parse(out);
      expect(back.goal, 'Keep goals');
      expect(back.review, SprintRepository.parse(rich).review);
      expect(back.retrospective, SprintRepository.parse(rich).retrospective);
    });

    test('DSH-02.c: saving and loading through the file keeps what is not edited (in memory)', () async {
      final files = MemoryFileAccess({'/r/sprint.md': rich});
      final repo = SprintRepository(files: files, path: '/r/sprint.md');
      final loaded = await repo.load();
      await repo.save(SprintEdit.setUsage(loaded, 'S-1', 2));
      final text = files.files['/r/sprint.md']!;
      expect(text, contains('Preamble above the title.'));
      expect(text, contains('| a row that cannot be read |'));
      expect(text, contains('## Lessons'));
      sameSprint(await repo.load(), SprintEdit.setUsage(loaded, 'S-1', 2));
    });

    test('DSH-02.d: a sprint that was never loaded (no text before, no kept lines) is written in the default layout and read back', () {
      final out = SprintRepository.format(const Sprint(goal: 'G', stories: [Story(id: 'N-1', title: 'New')]));
      expect(out, contains('Goal: G'));
      expect(out, contains('## Stories'));
      expect(SprintRepository.parse(out).stories.single.id, 'N-1');
    });
  });
}
