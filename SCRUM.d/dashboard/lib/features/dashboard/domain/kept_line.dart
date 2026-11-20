// Holds: one line of a sprint table section that the dashboard does not edit (DSH-02.f) and where it sits.
// Depends on: nothing. Used by: Sprint, SprintRepository. Reads or writes: nothing.

/// A line of the Blocks or Members section that is not a row it can read (an unreadable row, a note, text of another
/// section). It is written back as [text] right after the row whose key is [afterRow]; null means before the first
/// row, and [beforeTable] says it stood above the table's header row.
class KeptLine {
  const KeptLine({required this.text, this.afterRow, this.beforeTable = false});

  final String text;
  final String? afterRow;
  final bool beforeTable;
}
