// Tests DSH-07.a, DSH-07.b, DSH-07.c, DSH-07.d at the logic level (SprintEdit).
// One run covers each ID named in the test name.
import 'package:dashboard/features/dashboard/domain/sprint.dart';
import 'package:dashboard/features/dashboard/domain/sprint_edit.dart';
import 'package:dashboard/features/dashboard/domain/stage.dart';
import 'package:dashboard/features/dashboard/domain/story.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  const base = Sprint(
    goal: 'G',
    review: 'R',
    retrospective: 'T',
    stories: [Story(id: 'AAA-01', title: 'One', stage: Stage.build, assignee: 'Ann', estimate: 3)],
  );

  test('DSH-07.a: addStory adds a story with the item id as id, the given title and stage, keeping the rest', () {
    final s = SprintEdit.addStory(base, id: '#12', title: 'Issue twelve', stage: Stage.ready);
    expect(s.stories, hasLength(2));
    final added = s.stories.last;
    expect([added.id, added.title, added.stage], ['#12', 'Issue twelve', Stage.ready]);
    expect(s.stories.first, same(base.stories.first));
    expect([s.goal, s.review, s.retrospective], ['G', 'R', 'T']);
  });

  test('DSH-07.b: moveStory sets the stage of that story only', () {
    final s = SprintEdit.moveStory(base, 'AAA-01', Stage.test);
    expect(s.stories.single.stage, Stage.test);
    expect(s.stories.single.assignee, 'Ann');
    expect(s.stories.single.estimate, 3);
  });

  test('DSH-07.c: removeStory drops the story', () {
    final s = SprintEdit.removeStory(base, 'AAA-01');
    expect(s.stories, isEmpty);
    expect(s.goal, 'G');
  });

  test('DSH-07.d: moving to the current stage, an unknown id, or removing an unknown id returns the same sprint', () {
    expect(SprintEdit.moveStory(base, 'AAA-01', Stage.build), same(base));
    expect(SprintEdit.moveStory(base, 'NOPE', Stage.done), same(base));
    expect(SprintEdit.removeStory(base, 'NOPE'), same(base));
  });
}
