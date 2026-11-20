// Holds: one story of the sprint (DSH-02.b). Depends on: Stage.
// Used by: Sprint, SprintRepository, the board. Reads or writes: nothing.

import 'stage.dart';

/// A story: names the requirement and issue IDs it will meet. Estimate and usage are in usage points (DSH-09.b).
class Story {
  const Story({
    required this.id,
    required this.title,
    this.items = const [],
    this.stage = Stage.backlog,
    this.assignee = '',
    this.estimate = 0,
    this.usage = 0,
  });

  final String id;
  final String title;
  final List<String> items;
  final Stage stage;
  final String assignee;
  final double estimate;
  final double usage;

  Story copyWith({
    String? id,
    String? title,
    List<String>? items,
    Stage? stage,
    String? assignee,
    double? estimate,
    double? usage,
  }) =>
      Story(
        id: id ?? this.id,
        title: title ?? this.title,
        items: items ?? this.items,
        stage: stage ?? this.stage,
        assignee: assignee ?? this.assignee,
        estimate: estimate ?? this.estimate,
        usage: usage ?? this.usage,
      );

  @override
  bool operator ==(Object other) =>
      other is Story &&
      other.id == id &&
      other.title == title &&
      _sameItems(other.items, items) &&
      other.stage == stage &&
      other.assignee == assignee &&
      other.estimate == estimate &&
      other.usage == usage;

  @override
  int get hashCode => Object.hash(id, title, items.join(','), stage, assignee, estimate, usage);

  static bool _sameItems(List<String> a, List<String> b) {
    if (a.length != b.length) return false;
    for (var i = 0; i < a.length; i++) {
      if (a[i] != b[i]) return false;
    }
    return true;
  }
}
