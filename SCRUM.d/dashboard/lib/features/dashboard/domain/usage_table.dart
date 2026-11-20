// Holds: the Usage table of `SCRUM.d/usage.md` read from its text (DSH-14.a). Depends on: UsageRow.
// Used by: the dashboard controller. Reads or writes: nothing.

import 'usage_row.dart';

/// The rows of the Usage table. Pure parsing, no files.
class UsageTable {
  const UsageTable._();

  /// The rows of the first table that follows a heading naming Usage, or null when there is none (DSH-14.g).
  /// A row is: block ID, estimate session %, estimate weekly %, before session %, before weekly %, after session %,
  /// after weekly %; a cell that is a dash, blank or not a number is not known (DSH-14.a).
  static List<UsageRow>? parse(String text) {
    final lines = text.split(RegExp(r'\r?\n'));
    var inUsage = false;
    var headerSeen = false;
    List<UsageRow>? rows;
    for (final raw in lines) {
      final line = raw.trim();
      if (line.startsWith('#')) {
        if (rows != null) return rows;
        inUsage = line.toLowerCase().contains('usage');
        headerSeen = false;
        continue;
      }
      if (!inUsage) continue;
      if (!line.startsWith('|')) {
        if (rows != null) return rows;
        continue;
      }
      final cells = _cells(line);
      if (!headerSeen) {
        headerSeen = true;
        rows = [];
        continue;
      }
      if (cells.isEmpty || cells.every((c) => RegExp(r'^:?-{2,}:?$').hasMatch(c)) || cells.first.isEmpty) continue;
      rows!.add(UsageRow(
        block: cells[0],
        estimateSession: _number(cells, 1),
        estimateWeek: _number(cells, 2),
        beforeSession: _number(cells, 3),
        beforeWeek: _number(cells, 4),
        afterSession: _number(cells, 5),
        afterWeek: _number(cells, 6),
      ));
    }
    return rows;
  }

  static List<String> _cells(String line) {
    var inner = line.trim();
    if (inner.startsWith('|')) inner = inner.substring(1);
    if (inner.endsWith('|')) inner = inner.substring(0, inner.length - 1);
    return [for (final c in inner.split('|')) c.trim()];
  }

  static double? _number(List<String> cells, int i) {
    if (i >= cells.length) return null;
    return double.tryParse(cells[i].replaceAll('%', '').replaceAll(',', '.').trim());
  }
}
