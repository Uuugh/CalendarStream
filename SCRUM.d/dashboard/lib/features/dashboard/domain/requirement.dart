// Holds: one requirement row as the backlog shows it (DSH-03). Depends on: nothing.
// Used by: RequirementRepository, the backlog list. Reads or writes: nothing.

/// A requirement: [status] is `backlog` when the file left it blank; [feature] is the file name without extension.
class Requirement {
  const Requirement({required this.id, required this.status, required this.statement, required this.feature});

  final String id;
  final String status;
  final String statement;
  final String feature;
}
