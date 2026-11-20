// Holds: one open issue of the issue tracker as the dashboard lists it (DSH-05). Depends on: Status.
// Used by: IssueService, the backends, the page. Reads or writes: nothing.

import 'status.dart';

/// An issue. [feature] and [requirement] are null when the issue names none (shown as a dash, DSH-05.d);
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

  factory Issue.fromJson(Map<String, dynamic> json) => Issue(
        number: json['number'] as int,
        title: '${json['title']}',
        status: Status.parse('${json['status']}'),
        feature: json['feature'] as String?,
        requirement: json['requirement'] as String?,
        assignee: '${json['assignee'] ?? ''}',
      );

  final int number;
  final String title;
  final Status status;
  final String? feature;
  final String? requirement;
  final String assignee;

  Map<String, dynamic> toJson() => {
        'number': number,
        'title': title,
        'status': status.name,
        'feature': feature,
        'requirement': requirement,
        'assignee': assignee,
      };
}
