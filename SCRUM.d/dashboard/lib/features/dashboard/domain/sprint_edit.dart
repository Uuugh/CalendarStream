// Holds: the pure sprint edits (DSH-07.a-d, DSH-09.a): add a story, move it, remove it, set its estimate or usage.
// Depends on: Sprint, Story, Stage. Used by: the board and the dashboard page. Reads or writes: nothing.

import 'sprint.dart';
import 'stage.dart';
import 'story.dart';

/// Sprint edits as pure functions. Each returns [sprint] itself (same instance) when nothing changes,
/// so a caller writes the file only when the result is not identical to the input (DSH-07.d).
/// Goal, review and retrospective are kept (DSH-02.c).
class SprintEdit {
  const SprintEdit._();

  /// Adds a story for the backlog item [id] titled [title] in [stage], its items being [id] (DSH-07.a).
  /// A story with that ID already in the sprint leaves the sprint unchanged.
  static Sprint addStory(Sprint sprint, {required String id, required String title, required Stage stage}) {
    if (sprint.stories.any((s) => s.id == id)) return sprint;
    return sprint.copyWith(stories: [...sprint.stories, Story(id: id, title: title, items: [id], stage: stage)]);
  }

  /// Sets the stage of story [storyId] (DSH-07.b); unchanged when the story is missing or already in [stage] (DSH-07.d).
  static Sprint moveStory(Sprint sprint, String storyId, Stage stage) {
    final story = sprint.stories.where((s) => s.id == storyId).firstOrNull;
    if (story == null || story.stage == stage) return sprint;
    return sprint.copyWith(stories: [
      for (final s in sprint.stories) s.id == storyId ? s.copyWith(stage: stage) : s,
    ]);
  }

  /// Removes story [storyId] (DSH-07.c); unchanged when the story is missing.
  static Sprint removeStory(Sprint sprint, String storyId) {
    if (!sprint.stories.any((s) => s.id == storyId)) return sprint;
    return sprint.copyWith(stories: [
      for (final s in sprint.stories)
        if (s.id != storyId) s
    ]);
  }

  /// Sets the estimate of story [storyId] (DSH-09.a); unchanged when the story is missing, the value is negative
  /// or the estimate is already [value].
  static Sprint setEstimate(Sprint sprint, String storyId, double value) =>
      _setPoints(sprint, storyId, value, (s) => s.estimate, (s) => s.copyWith(estimate: value));

  /// Sets the usage of story [storyId] (DSH-09.a); unchanged when the story is missing, the value is negative
  /// or the usage is already [value].
  static Sprint setUsage(Sprint sprint, String storyId, double value) =>
      _setPoints(sprint, storyId, value, (s) => s.usage, (s) => s.copyWith(usage: value));

  static Sprint _setPoints(
      Sprint sprint, String storyId, double value, double Function(Story) current, Story Function(Story) change) {
    final story = sprint.stories.where((s) => s.id == storyId).firstOrNull;
    if (story == null || value.isNaN || value < 0 || current(story) == value) return sprint;
    return sprint.copyWith(stories: [
      for (final s in sprint.stories) s.id == storyId ? change(s) : s,
    ]);
  }
}
