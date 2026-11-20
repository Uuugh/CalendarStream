// Holds: the filter shared by the requirement list and the issue list (DSH-04, DSH-04.a-d): feature, requirement ID text, status.
// Depends on: nothing. Used by: Backlog, the filter bar, the dashboard page. Reads or writes: nothing.

/// An immutable filter. A null [feature] or [status] means All; [requirement] is a case-insensitive substring ('' keeps all).
class ListFilter {
  const ListFilter({this.feature, this.requirement = '', this.status});

  final String? feature;
  final String requirement;
  final String? status;

  /// True when an entry with these values meets all three filters (DSH-04.d). An entry without a
  /// feature or requirement ([feature] or [requirementId] null) meets only an unset filter of that kind.
  bool matches({String? feature, String? requirementId, required String status}) {
    if (this.feature != null && this.feature != feature) return false;
    if (requirement.isNotEmpty && !(requirementId ?? '').toLowerCase().contains(requirement.toLowerCase())) {
      return false;
    }
    if (this.status != null && this.status != status) return false;
    return true;
  }

  /// The entries of [items] that meet the filter, in order.
  List<T> apply<T>(
    List<T> items, {
    required String? Function(T) feature,
    required String? Function(T) requirementId,
    required String Function(T) status,
  }) =>
      [
        for (final i in items)
          if (matches(feature: feature(i), requirementId: requirementId(i), status: status(i))) i
      ];

  /// The sorted distinct non-null [values], for a dropdown (DSH-04.a, DSH-04.c).
  static List<String> choices(Iterable<String?> values) => ({...values}..remove(null)).cast<String>().toList()..sort();
}
