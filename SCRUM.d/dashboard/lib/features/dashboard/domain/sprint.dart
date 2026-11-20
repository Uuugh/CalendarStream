// Holds: the sprint (DSH-02): goal, stories, the Review and Retrospective text, and the text the dashboard does not
// edit, all kept as written (DSH-02.c, DSH-02.e). Depends on: Story, KeptLine.
// Used by: SprintRepository, the board. Reads or writes: nothing.

import 'kept_line.dart';
import 'story.dart';

/// The sprint. [review] and [retrospective] are the raw text of those sections, never interpreted.
/// [before] are the lines above the Goal line and [afterGoal] the lines between the Goal line and the Stories
/// heading, both verbatim; null means a new sprint, which gets the default layout. [keptLines] are the Stories
/// section lines that are not readable story rows.
class Sprint {
  const Sprint({
    this.goal = '',
    this.stories = const [],
    this.review = '',
    this.retrospective = '',
    this.before,
    this.afterGoal,
    this.keptLines = const [],
  });

  final String goal;
  final List<Story> stories;
  final String review;
  final String retrospective;
  final List<String>? before;
  final List<String>? afterGoal;
  final List<KeptLine> keptLines;

  Sprint copyWith({
    String? goal,
    List<Story>? stories,
    String? review,
    String? retrospective,
    List<String>? before,
    List<String>? afterGoal,
    List<KeptLine>? keptLines,
  }) =>
      Sprint(
        goal: goal ?? this.goal,
        stories: stories ?? this.stories,
        review: review ?? this.review,
        retrospective: retrospective ?? this.retrospective,
        before: before ?? this.before,
        afterGoal: afterGoal ?? this.afterGoal,
        keptLines: keptLines ?? this.keptLines,
      );
}
