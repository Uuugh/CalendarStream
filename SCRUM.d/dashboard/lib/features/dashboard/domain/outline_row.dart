// Holds: one row of the requirements outline (DSH-11): a requirement, its depth and whether it has listed
// sub-requirements. Depends on: Requirement. Used by: RequirementOutline, the Requirements column. Reads or writes: nothing.

import 'requirement.dart';

/// A listed requirement at [depth] (0 at the left, 1 for a sub-requirement under a listed requirement).
class OutlineRow {
  const OutlineRow(this.requirement, this.depth, {required this.hasChildren, required this.expanded});

  final Requirement requirement;
  final int depth;

  /// True when sub-requirements of this requirement are listed (DSH-11.b).
  final bool hasChildren;

  /// True when [hasChildren] and they are shown beneath it.
  final bool expanded;
}
