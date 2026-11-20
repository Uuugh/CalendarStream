// Holds: one agent's progress as the Agent progress column shows it (DSH-12.a). Depends on: nothing.
// Used by: ProgressFile, the backends, the page. Reads or writes: nothing.

/// The agent [label] has done [done] of [total].
class ProgressEntry {
  const ProgressEntry(this.label, this.done, this.total);

  factory ProgressEntry.fromJson(Map<String, dynamic> json) =>
      ProgressEntry('${json['label']}', json['done'] as int, json['total'] as int);

  final String label;
  final int done;
  final int total;

  /// done divided by total, 0 when total is 0, at most 1 (DSH-12.a).
  double get fraction => total <= 0 ? 0 : (done / total).clamp(0.0, 1.0);

  /// The text `done/total` (DSH-12.a).
  String get text => '$done/$total';

  Map<String, dynamic> toJson() => {'label': label, 'done': done, 'total': total};
}
