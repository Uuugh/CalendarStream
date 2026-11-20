// Holds: the sprint (DSH-02): goal, stories, and the Review and Retrospective text kept as written.
// Depends on: Story. Used by: SprintRepository, the board. Reads or writes: nothing.

import 'story.dart';

/// The sprint. [review] and [retrospective] are the raw text of those sections, never interpreted.
class Sprint {
  const Sprint({this.goal = '', this.stories = const [], this.review = '', this.retrospective = ''});

  final String goal;
  final List<Story> stories;
  final String review;
  final String retrospective;

  Sprint copyWith({String? goal, List<Story>? stories, String? review, String? retrospective}) => Sprint(
        goal: goal ?? this.goal,
        stories: stories ?? this.stories,
        review: review ?? this.review,
        retrospective: retrospective ?? this.retrospective,
      );
}
