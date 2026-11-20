// Holds: splitting one markdown table row into cells, honouring \| escapes.
// Depends on: nothing. Used by: SprintRepository, RequirementRepository. Reads or writes: nothing.

/// Helpers for pipe tables.
class MarkdownTable {
  const MarkdownTable._();

  /// The trimmed cells of a row such as `| a | b \| c |` (the cells keep `\|` unescaped to `|`),
  /// or null when [line] is not a table row.
  static List<String>? cells(String line) {
    final text = line.trim();
    if (!text.startsWith('|')) return null;
    final result = <String>[];
    final cell = StringBuffer();
    for (var i = 1; i < text.length; i++) {
      final c = text[i];
      if (c == '\\' && i + 1 < text.length && text[i + 1] == '|') {
        cell.write('|');
        i++;
      } else if (c == '|') {
        result.add(cell.toString().trim());
        cell.clear();
      } else {
        cell.write(c);
      }
    }
    final rest = cell.toString().trim();
    if (rest.isNotEmpty) result.add(rest);
    return result;
  }

  /// A cell ready to write: `|` becomes `\|`.
  static String escape(String cell) => cell.replaceAll('|', '\\|');
}
