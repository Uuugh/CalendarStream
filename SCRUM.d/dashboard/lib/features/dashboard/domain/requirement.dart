// Holds: one requirement row as the dashboard lists it (DSH-03). Depends on: Status.
// Used by: RequirementRepository, the backends, the page. Reads or writes: nothing.

import 'status.dart';

/// A requirement: [feature] is the file name without extension.
class Requirement {
  const Requirement({required this.id, required this.status, required this.statement, required this.feature});

  factory Requirement.fromJson(Map<String, dynamic> json) => Requirement(
        id: '${json['id']}',
        status: Status.parse('${json['status']}'),
        statement: '${json['statement']}',
        feature: '${json['feature']}',
      );

  final String id;
  final Status status;
  final String statement;
  final String feature;

  Map<String, dynamic> toJson() => {'id': id, 'status': status.name, 'statement': statement, 'feature': feature};
}
