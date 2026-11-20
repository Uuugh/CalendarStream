// Holds: one issue of the issue tracker as the backlog shows it (DSH-05, DSH-05.a, DSH-05.b), and its status.
// Depends on: nothing. Used by: IssueService, Backlog, the issue list. Reads or writes: nothing.

/// The status of an issue (DSH-05.a).
enum IssueStatus { open, closed }

/// An issue. [feature] and [requirement] are null when the issue names none (shown as a dash, DSH-05.b);
/// [assignee] is empty when nobody is assigned.
class Issue {
  const Issue({
    required this.number,
    required this.title,
    required this.status,
    this.feature,
    this.requirement,
    this.assignee = '',
  });

  final int number;
  final String title;
  final IssueStatus status;
  final String? feature;
  final String? requirement;
  final String assignee;
}
