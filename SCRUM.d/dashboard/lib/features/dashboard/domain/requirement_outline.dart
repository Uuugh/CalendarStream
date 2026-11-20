// Holds: the pure outline of the listed requirements (DSH-11.a to DSH-11.e): sub-requirements beneath their requirement,
// collapsed or expanded. Depends on: Requirement, OutlineRow. Used by: the Requirements column. Reads or writes: nothing.

import 'outline_row.dart';
import 'requirement.dart';

/// Outline as pure functions.
class RequirementOutline {
  const RequirementOutline._();

  /// The ID of the requirement above [id]: the text before the last `.` (`ACC-06.a` has `ACC-06`), or null for a
  /// requirement with no `.`.
  static String? parentOf(String id) {
    final dot = id.lastIndexOf('.');
    return dot <= 0 ? null : id.substring(0, dot);
  }

  /// The IDs of the listed requirements that have a listed sub-requirement, in listed order (DSH-11.b).
  static List<String> parents(List<Requirement> listed) {
    final ids = {for (final r in listed) r.id};
    final withChildren = {for (final c in listed) if (ids.contains(parentOf(c.id))) parentOf(c.id)!};
    return [for (final r in listed) if (withChildren.contains(r.id)) r.id];
  }

  /// The rows to draw: [listed] in order, each requirement followed by its listed sub-requirements when its ID is in
  /// [expanded]. A sub-requirement whose requirement is not listed is a row of its own at depth 0 (DSH-11.e).
  static List<OutlineRow> rows(List<Requirement> listed, Set<String> expanded) {
    final ids = {for (final r in listed) r.id};
    final children = <String, List<Requirement>>{};
    final roots = <Requirement>[];
    for (final r in listed) {
      final p = parentOf(r.id);
      if (p != null && ids.contains(p)) {
        children.putIfAbsent(p, () => []).add(r);
      } else {
        roots.add(r);
      }
    }
    final result = <OutlineRow>[];
    void add(Requirement r, int depth) {
      final kids = children[r.id] ?? const <Requirement>[];
      final open = kids.isNotEmpty && expanded.contains(r.id);
      result.add(OutlineRow(r, depth, hasChildren: kids.isNotEmpty, expanded: open));
      if (open) {
        for (final k in kids) {
          add(k, depth + 1);
        }
      }
    }

    for (final r in roots) {
      add(r, 0);
    }
    return result;
  }
}
