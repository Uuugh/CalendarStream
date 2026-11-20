// Tests DSH-02 (a-d): the sprint file. One run covers each ID named in the test name.
import 'dart:io';

import 'package:dashboard/features/dashboard/data/sprint_repository.dart';
import 'package:dashboard/features/dashboard/domain/sprint.dart';
import 'package:dashboard/features/dashboard/domain/stage.dart';
import 'package:dashboard/features/dashboard/domain/story.dart';
import 'package:flutter_test/flutter_test.dart';

import '../support/fixtures.dart';

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
}
