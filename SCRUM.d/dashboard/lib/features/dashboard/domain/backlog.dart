// Holds: which requirements and issues are backlog items (DSH-03.b, DSH-05.c).
// Depends on: Sprint, Requirement, Issue. Used by: the dashboard page. Reads or writes: nothing.

import 'issue.dart';
import 'requirement.dart';
import 'sprint.dart';

/// The backlog rules, as pure functions.
class Backlog {
  const Backlog._();

  /// Every ID a story of [sprint] names: its story ID and its items.
  static Set<String> named(Sprint sprint) => {
        for (final s in sprint.stories) ...[s.id, ...s.items]
      };

  /// The requirements no story names (DSH-03.b). The status filter then picks `backlog` (DSH-03.c).
  static List<Requirement> requirements(List<Requirement> all, Sprint sprint) {
    final named = Backlog.named(sprint);
    return [
      for (final r in all)
        if (!named.contains(r.id)) r
    ];
  }

  /// The issues no story names, open and closed (DSH-05.c). A story names an issue as its number, with or without `#`.
  static List<Issue> issues(List<Issue> all, Sprint sprint) {
    final named = Backlog.named(sprint);
    return [
      for (final i in all)
        if (!named.contains('${i.number}') && !named.contains('#${i.number}')) i
    ];
  }
}
