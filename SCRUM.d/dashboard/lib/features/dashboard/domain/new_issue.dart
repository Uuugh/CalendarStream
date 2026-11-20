// Holds: an issue as the New issue form enters it (DSH-08) and the body text it makes (DSH-05.b).
// Depends on: nothing. Used by: IssueService, the New issue dialog. Reads or writes: nothing.

/// A new issue: [feature] and [requirement] are null when not chosen; [closed] makes it be closed after creation.
class NewIssue {
  const NewIssue({
    required this.title,
    this.description = '',
    this.feature,
    this.requirement,
    this.closed = false,
  });

  final String title;
  final String description;
  final String? feature;
  final String? requirement;
  final bool closed;

  /// The description, then a line `Requirement: <ID>` when a requirement is chosen (DSH-05.b).
  String get body {
    final text = description.trim();
    if (requirement == null) return text;
    final line = 'Requirement: $requirement';
    return text.isEmpty ? line : '$text\n\n$line';
  }
}
