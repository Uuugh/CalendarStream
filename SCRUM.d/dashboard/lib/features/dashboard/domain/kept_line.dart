// Holds: one line of the Stories section that the dashboard does not edit (DSH-02.e) and where it sits.
// Depends on: nothing. Used by: Sprint, SprintRepository. Reads or writes: nothing.

/// A line of the Stories section that is not a story row it can read (an unreadable row, a note, an unknown heading).
/// It is written back as [text] right after the row of story [afterStory]; [afterStory] null means before the first
/// row, and [beforeTable] says it stood above the table's header row.
class KeptLine {
  const KeptLine({required this.text, this.afterStory, this.beforeTable = false});

  final String text;
  final String? afterStory;
  final bool beforeTable;
}
