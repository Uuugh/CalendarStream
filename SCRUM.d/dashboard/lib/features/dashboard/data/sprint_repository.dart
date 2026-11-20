// Holds: reading and writing SCRUM.d/sprint.md (DSH-02). Depends on: FileAccess, MarkdownTable, the sprint domain
// (Sprint, Block, Member, KeptLine, BlockKind, PointsFormat). Used by: LocalBackend, HttpBackend.
// Reads or writes: the sprint file at the path given.

import '../domain/block.dart';
import '../domain/block_kind.dart';
import '../domain/kept_line.dart';
import '../domain/member.dart';
import '../domain/points_format.dart';
import '../domain/sprint.dart';
import 'file_access.dart';
import 'markdown_table.dart';

/// Source of truth for the sprint file. A missing file is an empty sprint; the first [save] creates it (DSH-02.e).
/// [parse] and [format] are static so the web backend, which has no file, uses the same file format.
class SprintRepository {
  SprintRepository({required this.files, required this.path});

  final FileAccess files;

  /// Path of the sprint file, e.g. `<repo>/SCRUM.d/sprint.md`.
  final String path;

  Future<Sprint> load() async {
    final text = await files.read(path);
    return text == null ? const Sprint() : parse(text);
  }

  /// Writes [sprint] to the file at once (DSH-02.d).
  Future<void> save(Sprint sprint) => files.write(path, format(sprint));

  /// The headings in file order; a heading ends the section being read only when it comes later in this order, so
  /// the same text inside a Review or Retrospective body stays in the body (DSH-02.f).
  static const _headings = ['## Blocks', '## Members', '## Review', '## Retrospective'];
  static final _separatorCell = RegExp(r'^:?-+:?$');

  /// Parses sprint file text (DSH-02.a to DSH-02.c). What it does not edit is kept: the lines above the Blocks
  /// heading, other text and unreadable rows of the two tables (DSH-02.f).
  static Sprint parse(String text) {
    final before = <String>[];
    final blocks = <Block>[];
    final members = <Member>[];
    final blockLines = <KeptLine>[];
    final memberLines = <KeptLine>[];
    final review = <String>[];
    final retrospective = <String>[];
    var state = -1; // -1 above the Blocks heading, then the index in _headings
    var blockHead = false;
    var memberHead = false;
    String? lastBlock;
    String? lastMember;
    final ids = <String>{};
    for (final line in text.split(RegExp(r'\r?\n'))) {
      final next = _headings.indexOf(line.trimRight());
      if (next > state) {
        state = next;
        continue;
      }
      switch (state) {
        case -1:
          before.add(line);
        case 0:
          if (line.trim().isEmpty) break;
          final cells = MarkdownTable.cells(line);
          final block = cells == null ? null : _block(cells);
          if (block != null && ids.add(block.id)) {
            blocks.add(block);
            lastBlock = block.id;
          } else if (cells != null && _isHead(cells, 'id')) {
            blockHead = true;
          } else {
            blockLines.add(KeptLine(text: line, afterRow: lastBlock, beforeTable: !blockHead));
          }
        case 1:
          if (line.trim().isEmpty) break;
          final cells = MarkdownTable.cells(line);
          final member = cells == null ? null : _member(cells);
          if (member != null) {
            members.add(member);
            lastMember = _memberKey(member);
          } else if (cells != null && _isHead(cells, 'story')) {
            memberHead = true;
          } else {
            memberLines.add(KeptLine(text: line, afterRow: lastMember, beforeTable: !memberHead));
          }
        case 2:
          review.add(line);
        default:
          retrospective.add(line);
      }
    }
    return Sprint(
      blocks: blocks,
      members: members,
      review: _body(review),
      retrospective: _body(retrospective),
      before: before,
      blockLines: blockLines,
      memberLines: memberLines,
    );
  }

  /// The block of a table row, or null when it is not a readable Blocks row.
  static Block? _block(List<String> cells) {
    if (cells.length < 3 || cells[0].isEmpty) return null;
    final kind = BlockKind.parse(cells[1]);
    if (kind == null) return null;
    String cell(int i) => i < cells.length ? cells[i] : '';
    return Block(
      id: cells[0],
      kind: kind,
      name: cells[2],
      parent: cell(3).isEmpty ? null : cell(3),
      assignee: cell(4),
      estimate: PointsFormat.parse(cell(5)) ?? 0,
      usage: PointsFormat.parse(cell(6)) ?? 0,
    );
  }

  static Member? _member(List<String> cells) =>
      cells.length < 2 || cells[0].isEmpty || cells[1].isEmpty || _isHead(cells, 'story') ? null : Member(cells[0], cells[1]);

  static String _memberKey(Member m) => '${m.blockId}|${m.item}';

  /// True for a table's header row and its separator row, which [format] writes again.
  static bool _isHead(List<String> cells, String firstHeading) =>
      cells.isNotEmpty && (cells[0].toLowerCase() == firstHeading || cells.every(_separatorCell.hasMatch));

  /// The file text for [sprint]; everything [parse] kept is written back in place (DSH-02.f).
  static String format(Sprint sprint) {
    final b = StringBuffer();
    for (final line in sprint.before ?? const ['# Sprint', '']) {
      b.writeln(line);
    }
    b
      ..writeln(_headings[0])
      ..writeln();
    _table(
      b,
      header: '| id | kind | name | parent | assignee | estimate | usage |',
      separator: '|---|---|---|---|---|---|---|',
      kept: sprint.blockLines,
      rows: [
        for (final x in sprint.blocks)
          (
            x.id,
            '| ${MarkdownTable.escape(x.id)} | ${x.kind.name} | ${MarkdownTable.escape(x.name)} | '
                '${MarkdownTable.escape(x.parent ?? '')} | ${MarkdownTable.escape(x.assignee)} | '
                '${PointsFormat.format(x.estimate)} | ${PointsFormat.format(x.usage)} |'
          ),
      ],
    );
    b
      ..writeln()
      ..writeln(_headings[1])
      ..writeln();
    _table(
      b,
      header: '| story | item |',
      separator: '|---|---|',
      kept: sprint.memberLines,
      rows: [
        for (final m in sprint.members)
          (_memberKey(m), '| ${MarkdownTable.escape(m.blockId)} | ${MarkdownTable.escape(m.item)} |'),
      ],
    );
    b
      ..writeln()
      ..writeln(_headings[2])
      ..writeln();
    if (sprint.review.isNotEmpty) b.writeln(sprint.review);
    b
      ..writeln()
      ..writeln(_headings[3])
      ..writeln();
    if (sprint.retrospective.isNotEmpty) b.writeln(sprint.retrospective);
    return b.toString();
  }

  /// One table: kept lines above the header, the header, kept lines before the first row, each row followed by the
  /// kept lines that stood after it, then kept lines whose row is gone.
  static void _table(
    StringBuffer b, {
    required String header,
    required String separator,
    required List<KeptLine> kept,
    required List<(String, String)> rows,
  }) {
    for (final k in kept.where((k) => k.beforeTable)) {
      b.writeln(k.text);
    }
    b
      ..writeln(header)
      ..writeln(separator);
    for (final k in kept.where((k) => !k.beforeTable && k.afterRow == null)) {
      b.writeln(k.text);
    }
    final keys = {for (final r in rows) r.$1};
    final written = <String>{};
    for (final (key, line) in rows) {
      b.writeln(line);
      if (written.add(key)) {
        for (final k in kept.where((k) => !k.beforeTable && k.afterRow == key)) {
          b.writeln(k.text);
        }
      }
    }
    for (final k in kept.where((k) => !k.beforeTable && k.afterRow != null && !keys.contains(k.afterRow))) {
      b.writeln(k.text);
    }
  }

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
