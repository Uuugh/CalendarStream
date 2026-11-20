// Holds: reading and writing SCRUM.d/sprint.md (DSH-02). Depends on: FileAccess, MarkdownTable, the sprint domain.
// Used by: the dashboard page. Reads or writes: the sprint file at the path given.

import '../domain/points_format.dart';
import '../domain/sprint.dart';
import '../domain/stage.dart';
import '../domain/story.dart';
import 'file_access.dart';
import 'markdown_table.dart';

/// Source of truth for the sprint file. A missing file is an empty sprint; the first [save] creates it (DSH-02.d).
class SprintRepository {
  SprintRepository({required this.files, required this.path});

  final FileAccess files;

  /// Path of the sprint file, e.g. `<repo>/SCRUM.d/sprint.md`.
  final String path;

  Future<Sprint> load() async {
    final text = await files.read(path);
    return text == null ? const Sprint() : parse(text);
  }

  /// Writes [sprint] to the file at once (DSH-02.c).
  Future<void> save(Sprint sprint) => files.write(path, format(sprint));

  /// Parses sprint file text (DSH-02.a, DSH-02.b).
  static Sprint parse(String text) {
    var goal = '';
    final stories = <Story>[];
    final sections = <String, List<String>>{};
    String? section;
    for (final line in text.split(RegExp(r'\r?\n'))) {
      final heading = RegExp(r'^##\s+(.*?)\s*$').firstMatch(line);
      if (heading != null) {
        section = heading.group(1)!.toLowerCase();
        sections[section] = [];
        continue;
      }
      if (section == null) {
        final g = RegExp(r'^Goal:\s*(.*?)\s*$').firstMatch(line);
        if (g != null) goal = g.group(1)!;
      } else {
        sections[section]!.add(line);
      }
    }
    for (final line in sections['stories'] ?? const <String>[]) {
      final cells = MarkdownTable.cells(line);
      if (cells == null || cells.length < 4) continue;
      final stage = Stage.parse(cells[3]);
      if (stage == null || cells[0].isEmpty) continue; // header and separator rows
      stories.add(Story(
        id: cells[0],
        title: cells[1],
        items: cells[2].split(',').map((e) => e.trim()).where((e) => e.isNotEmpty).toList(),
        stage: stage,
        assignee: cells.length > 4 ? cells[4] : '',
        estimate: cells.length > 5 ? (double.tryParse(cells[5]) ?? 0) : 0,
        usage: cells.length > 6 ? (double.tryParse(cells[6]) ?? 0) : 0,
      ));
    }
    return Sprint(
      goal: goal,
      stories: stories,
      review: _body(sections['review']),
      retrospective: _body(sections['retrospective']),
    );
  }

  /// The file text for [sprint]; review and retrospective text is written as kept.
  static String format(Sprint sprint) {
    final b = StringBuffer()
      ..writeln('# Sprint')
      ..writeln()
      ..writeln('Goal: ${sprint.goal}')
      ..writeln()
      ..writeln('## Stories')
      ..writeln()
      ..writeln('| story | title | items | stage | assignee | estimate | usage |')
      ..writeln('|---|---|---|---|---|---|---|');
    for (final s in sprint.stories) {
      b.writeln('| ${MarkdownTable.escape(s.id)} | ${MarkdownTable.escape(s.title)} | '
          '${MarkdownTable.escape(s.items.join(', '))} | ${_stageName(s.stage)} | '
          '${MarkdownTable.escape(s.assignee)} | ${PointsFormat.format(s.estimate)} | ${PointsFormat.format(s.usage)} |');
    }
    b
      ..writeln()
      ..writeln('## Review')
      ..writeln();
    if (sprint.review.isNotEmpty) b.writeln(sprint.review);
    b
      ..writeln()
      ..writeln('## Retrospective')
      ..writeln();
    if (sprint.retrospective.isNotEmpty) b.writeln(sprint.retrospective);
    return b.toString();
  }

  static String _stageName(Stage s) => s.name[0].toUpperCase() + s.name.substring(1);

  /// Section lines without the blank lines around them.
  static String _body(List<String>? lines) {
    if (lines == null) return '';
    var start = 0;
    var end = lines.length;
    while (start < end && lines[start].trim().isEmpty) {
      start++;
    }
    while (end > start && lines[end - 1].trim().isEmpty) {
      end--;
    }
    return lines.sublist(start, end).join('\n');
  }
}
