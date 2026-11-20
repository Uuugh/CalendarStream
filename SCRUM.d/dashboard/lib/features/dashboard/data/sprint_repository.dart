// Holds: reading and writing SCRUM.d/sprint.md (DSH-02). Depends on: FileAccess, MarkdownTable, the sprint domain (Sprint, Story, KeptLine, Stage).
// Used by: the dashboard page. Reads or writes: the sprint file at the path given.

import '../domain/kept_line.dart';
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

  /// The known top-level headings in file order; a heading ends the section being read only when it comes later
  /// in this order, so the same text inside a Review or Retrospective body stays in the body (DSH-02.e).
  static const _headings = ['## Stories', '## Review', '## Retrospective'];
  static final _goalLine = RegExp(r'^Goal:\s*(.*?)\s*$');
  static final _separatorCell = RegExp(r'^:?-+:?$');

  /// Parses sprint file text (DSH-02.a, DSH-02.b). What it does not edit is kept: the lines above the Goal line and
  /// between it and the Stories heading, unknown headings and notes, and story rows it cannot read (DSH-02.e).
  static Sprint parse(String text) {
    String? goal;
    final before = <String>[];
    final afterGoal = <String>[];
    final stories = <Story>[];
    final kept = <KeptLine>[];
    final review = <String>[];
    final retrospective = <String>[];
    var state = -1; // -1 above the Stories heading, then the index in _headings
    var headerSeen = false;
    String? lastStory;
    for (final line in text.split(RegExp(r'\r?\n'))) {
      final next = _headings.indexOf(line.trimRight());
      if (next > state) {
        state = next;
        continue;
      }
      switch (state) {
        case -1:
          final g = goal == null ? _goalLine.firstMatch(line) : null;
          if (g != null) {
            goal = g.group(1)!;
          } else {
            (goal == null ? before : afterGoal).add(line);
          }
        case 0:
          if (line.trim().isEmpty) break;
          final cells = MarkdownTable.cells(line);
          final story = cells == null ? null : _story(cells);
          if (story != null) {
            stories.add(story);
            lastStory = story.id;
          } else if (cells != null && _isTableHead(cells)) {
            headerSeen = true;
          } else {
            kept.add(KeptLine(text: line, afterStory: lastStory, beforeTable: !headerSeen));
          }
        case 1:
          review.add(line);
        default:
          retrospective.add(line);
      }
    }
    return Sprint(
      goal: goal ?? '',
      stories: stories,
      review: _body(review),
      retrospective: _body(retrospective),
      before: before,
      afterGoal: afterGoal,
      keptLines: kept,
    );
  }

  /// The story of a table row, or null when it is not a readable story row.
  static Story? _story(List<String> cells) {
    if (cells.length < 4 || cells[0].isEmpty) return null;
    final stage = Stage.parse(cells[3]);
    if (stage == null) return null;
    return Story(
      id: cells[0],
      title: cells[1],
      items: cells[2].split(',').map((e) => e.trim()).where((e) => e.isNotEmpty).toList(),
      stage: stage,
      assignee: cells.length > 4 ? cells[4] : '',
      estimate: cells.length > 5 ? (double.tryParse(cells[5]) ?? 0) : 0,
      usage: cells.length > 6 ? (double.tryParse(cells[6]) ?? 0) : 0,
    );
  }

  /// True for the table's header row and its separator row, which [format] writes again.
  static bool _isTableHead(List<String> cells) =>
      cells.isNotEmpty && (cells[0].toLowerCase() == 'story' || cells.every(_separatorCell.hasMatch));

  /// The file text for [sprint]; everything [parse] kept is written back in place (DSH-02.c, DSH-02.e).
  static String format(Sprint sprint) {
    final b = StringBuffer();
    for (final line in sprint.before ?? const ['# Sprint', '']) {
      b.writeln(line);
    }
    b.writeln('Goal: ${sprint.goal}');
    for (final line in sprint.afterGoal ?? const ['']) {
      b.writeln(line);
    }
    b
      ..writeln('## Stories')
      ..writeln();
    final kept = sprint.keptLines;
    for (final k in kept.where((k) => k.beforeTable)) {
      b.writeln(k.text);
    }
    b
      ..writeln('| story | title | items | stage | assignee | estimate | usage |')
      ..writeln('|---|---|---|---|---|---|---|');
    final written = <String>{};
    final ids = {for (final s in sprint.stories) s.id};
    for (final k in kept.where((k) => !k.beforeTable && k.afterStory == null)) {
      b.writeln(k.text);
    }
    for (final s in sprint.stories) {
      b.writeln('| ${MarkdownTable.escape(s.id)} | ${MarkdownTable.escape(s.title)} | '
          '${MarkdownTable.escape(s.items.join(', '))} | ${_stageName(s.stage)} | '
          '${MarkdownTable.escape(s.assignee)} | ${PointsFormat.format(s.estimate)} | ${PointsFormat.format(s.usage)} |');
      if (written.add(s.id)) {
        for (final k in kept.where((k) => k.afterStory == s.id)) {
          b.writeln(k.text);
        }
      }
    }
    for (final k in kept.where((k) => k.afterStory != null && !ids.contains(k.afterStory))) {
      b.writeln(k.text);
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
  static String _body(List<String> lines) {
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
