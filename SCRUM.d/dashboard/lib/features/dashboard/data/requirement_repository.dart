// Holds: reading the requirement rows of requirements/*.md and requirements/*.d/*.md and changing the status cell of
// one row (DSH-03, DSH-03.a, DSH-13.d). Depends on: FileAccess, MarkdownTable, Requirement, Status.
// Used by: LocalBackend. Reads or writes: the requirement files under the folder given.

import '../domain/requirement.dart';
import '../domain/status.dart';
import 'file_access.dart';
import 'markdown_table.dart';

/// Source of truth for the requirement rows.
class RequirementRepository {
  RequirementRepository({required this.files, required this.directory});

  final FileAccess files;

  /// The requirements folder, e.g. `<repo>/requirements`.
  final String directory;

  static const _skipped = {'README.md', 'oldkey.md', 'open-questions.md'};
  static final _idPattern = RegExp(r'^[A-Z][A-Z0-9]*-\d+(\.[a-z0-9]+)*$');

  /// The paths of the feature files: `*.md` and `*.d/*.md`, not the skipped ones (DSH-03.a).
  Future<List<String>> paths() async {
    final all = [...await files.listFiles(directory)];
    for (final dir in await files.listDirectories(directory)) {
      if (dir.endsWith('.d')) all.addAll(await files.listFiles(dir));
    }
    return [
      for (final p in all)
        if (p.endsWith('.md') && !_skipped.contains(p.split('/').last)) p
    ];
  }

  Future<List<Requirement>> load() async {
    final result = <Requirement>[];
    for (final path in await paths()) {
      final text = await files.read(path);
      if (text == null) continue;
      final name = path.split('/').last;
      result.addAll(parse(text, name.substring(0, name.length - 3)));
    }
    return result;
  }

  /// Sets the status cell of requirement [id] in the file that holds it, and writes that file as a whole or not at
  /// all (DSH-13.d). Returns false when no file holds the ID.
  Future<bool> setStatus(String id, Status status) async {
    for (final path in await paths()) {
      final text = await files.read(path);
      if (text == null) continue;
      final changed = withStatus(text, id, status);
      if (changed == null) continue;
      if (changed != text) await files.writeAtomic(path, changed);
      return true;
    }
    return false;
  }

  /// The requirement rows of one file's [text]; a blank status is `backlog`, `proposed (?)` is `proposed`.
  static List<Requirement> parse(String text, String feature) {
    final result = <Requirement>[];
    for (final line in text.split(RegExp(r'\r?\n'))) {
      final cells = MarkdownTable.cells(line);
      if (cells == null || cells.length < 3 || !_idPattern.hasMatch(cells[0])) continue;
      result.add(Requirement(id: cells[0], status: Status.parse(cells[1]), statement: cells[2], feature: feature));
    }
    return result;
  }

  /// [text] with the status cell of the row of [id] replaced by [status]; everything else, line endings included, stays
  /// byte for byte. Null when the text has no row for [id].
  static String? withStatus(String text, String id, Status status) {
    final lines = text.split('\n');
    for (var i = 0; i < lines.length; i++) {
      final line = lines[i];
      final cells = MarkdownTable.cells(line);
      if (cells == null || cells.length < 3 || cells[0] != id) continue;
      final first = line.indexOf('|');
      final start = line.indexOf('|', first + 1);
      final end = start < 0 ? -1 : line.indexOf('|', start + 1);
      if (end < 0) continue;
      final old = line.substring(start + 1, end);
      final lead = old.length - old.trimLeft().length;
      final trail = old.length - old.trimRight().length;
      final cell = old.trim().isEmpty ? ' ${status.name} ' : '${old.substring(0, lead)}${status.name}${old.substring(old.length - trail)}';
      lines[i] = '${line.substring(0, start + 1)}$cell${line.substring(end)}';
      return lines.join('\n');
    }
    return null;
  }
}
