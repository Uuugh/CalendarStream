// Holds: reading requirement rows from requirements/*.md and requirements/*.d/*.md (DSH-03, DSH-03.a).
// Depends on: FileAccess, MarkdownTable, Requirement. Used by: the dashboard page.
// Reads or writes: the requirement files under the folder given.

import '../domain/requirement.dart';
import 'file_access.dart';
import 'markdown_table.dart';

/// Source of the requirements list. Read only.
class RequirementRepository {
  RequirementRepository({required this.files, required this.directory});

  final FileAccess files;

  /// The requirements folder, e.g. `<repo>/requirements`.
  final String directory;

  static const _skipped = {'README.md', 'oldkey.md', 'open-questions.md'};
  static final _idPattern = RegExp(r'^[A-Z][A-Z0-9]*-\d+(\.[a-z0-9]+)*$');

  Future<List<Requirement>> load() async {
    final paths = [...await files.listFiles(directory)];
    for (final dir in await files.listDirectories(directory)) {
      if (dir.endsWith('.d')) paths.addAll(await files.listFiles(dir));
    }
    final result = <Requirement>[];
    for (final path in paths) {
      final name = path.split('/').last;
      if (!name.endsWith('.md') || _skipped.contains(name)) continue;
      final text = await files.read(path);
      if (text == null) continue;
      result.addAll(parse(text, name.substring(0, name.length - 3)));
    }
    return result;
  }

  /// The requirement rows of one file's [text]; a blank status is `backlog`, `proposed (?)` is `proposed`.
  static List<Requirement> parse(String text, String feature) {
    final result = <Requirement>[];
    for (final line in text.split(RegExp(r'\r?\n'))) {
      final cells = MarkdownTable.cells(line);
      if (cells == null || cells.length < 3 || !_idPattern.hasMatch(cells[0])) continue;
      final status = cells[1].split(RegExp(r'\s+')).first;
      result.add(Requirement(
        id: cells[0],
        status: status.isEmpty ? 'backlog' : status,
        statement: cells[2],
        feature: feature,
      ));
    }
    return result;
  }
}
