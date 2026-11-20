// Holds: an issue as the New issue form enters it (DSH-09) and the body text it makes (DSH-05.c).
// Depends on: Status. Used by: IssueService, the backends, the New issue form. Reads or writes: nothing.

import 'status.dart';

/// A new issue: [feature] and [requirement] are null when not chosen.
class NewIssue {
  const NewIssue({
    required this.title,
    this.description = '',
    this.feature,
    this.requirement,
    this.status = Status.backlog,
  });

  factory NewIssue.fromJson(Map<String, dynamic> json) => NewIssue(
        title: '${json['title']}',
        description: '${json['description'] ?? ''}',
        feature: json['feature'] as String?,
        requirement: json['requirement'] as String?,
        status: Status.tryName(json['status'] as String?) ?? Status.backlog,
      );

  final String title;
  final String description;
  final String? feature;
  final String? requirement;
  final Status status;

  /// The description, then a line `Requirement: <ID>` when a requirement is chosen (DSH-05.c).
  String get body {
    final text = description.trim();
    if (requirement == null) return text;
    final line = 'Requirement: $requirement';
    return text.isEmpty ? line : '$text\n\n$line';
  }

  /// The labels of the new issue: `issue`, `feature:<feature>` when a feature is chosen, and the status (DSH-09.d).
  List<String> get labels => ['issue', if (feature != null) 'feature:$feature', status.name];

  Map<String, dynamic> toJson() => {
        'title': title,
        'description': description,
        'feature': feature,
        'requirement': requirement,
        'status': status.name,
      };
}
