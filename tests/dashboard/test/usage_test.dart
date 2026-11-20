// Tests the usage chart model: DSH-14.a (the Usage table of usage.md), DSH-14.c (bars), DSH-14.d (estimate bands),
// DSH-14.e (projection), DSH-14.f (over 100), DSH-14.g (no table), DSH-14.b (two meters on a 0 to 100 scale).
// Drawing (colors, marks, tooltips, labels) is a page test and is not here. One run covers each ID named in the test name.
import 'package:dashboard/features/dashboard/data/local_backend.dart';
import 'package:dashboard/features/dashboard/domain/block.dart';
import 'package:dashboard/features/dashboard/domain/block_kind.dart';
import 'package:dashboard/features/dashboard/domain/sprint.dart';
import 'package:dashboard/features/dashboard/domain/usage_chart.dart';
import 'package:dashboard/features/dashboard/domain/usage_meter.dart';
import 'package:dashboard/features/dashboard/domain/usage_row.dart';
import 'package:dashboard/features/dashboard/domain/usage_table.dart';
import 'package:flutter_test/flutter_test.dart';

import '../support/fixtures.dart';
import '../support/memory_file_access.dart';

const header = '| block | estimate session % | estimate weekly % | before session % | before weekly % | after session % | after weekly % |\n|---|---|---|---|---|---|---|\n';

const usageFile = '''# Usage

Readings of the 5-hour session and the 7-day week.

## Usage

$header| sprint-1 | 10 | 5 | 20 | 10 | 32 | 16 |
| sprint-2 | 12 | - | 40 | 30 | - | — |
| sprint-3 |  |  |  |  |  |  |
''';

const sprints = Sprint(blocks: [
  Block(id: 'story-1', kind: BlockKind.story, name: 'S'),
  Block(id: 'sprint-1', kind: BlockKind.sprint, name: 'One'),
  Block(id: 'sprint-2', kind: BlockKind.sprint, name: 'Two'),
  Block(id: 'sprint-3', kind: BlockKind.sprint, name: 'Three'),
]);

void main() {
  group('the Usage table (DSH-14.a, DSH-14.g)', () {
    test('DSH-14.a: a row is block ID, estimate session, estimate weekly, before session, before weekly, after session, after weekly', () {
      final rows = UsageTable.parse(usageFile)!;
      final r = rows.first;
      expect([r.block, r.estimateSession, r.estimateWeek, r.beforeSession, r.beforeWeek, r.afterSession, r.afterWeek],
          ['sprint-1', 10, 5, 20, 10, 32, 16]);
      expect(rows.map((x) => x.block), ['sprint-1', 'sprint-2', 'sprint-3']);
    });

    test('DSH-14.a: a cell that is a dash, blank or not a number is not known', () {
      final rows = UsageTable.parse(usageFile)!;
      expect([rows[1].estimateWeek, rows[1].afterSession, rows[1].afterWeek], [null, null, null]);
      expect([rows[1].estimateSession, rows[1].beforeSession, rows[1].beforeWeek], [12, 40, 30]);
      expect([rows[2].estimateSession, rows[2].beforeWeek, rows[2].afterWeek], [null, null, null]);
    });

    test('DSH-14.a: a row with fewer cells leaves the rest unknown; a percent sign and a decimal comma are read', () {
      final rows = UsageTable.parse('## Usage\n\n$header| s-1 | 5 | 6 |\n| s-2 | 7,5% | 1.5 | 2 | 3 | 4 | 5 |\n')!;
      expect([rows[0].beforeSession, rows[0].afterWeek], [null, null]);
      expect([rows[1].estimateSession, rows[1].estimateWeek], [7.5, 1.5]);
    });

    test('DSH-14.a: a CRLF file is read the same', () {
      expect(UsageTable.parse(usageFile.replaceAll('\n', '\r\n'))!.map((r) => r.block), ['sprint-1', 'sprint-2', 'sprint-3']);
    });

    test('DSH-14.g: no table, no usage heading or an empty text gives no rows at all', () {
      expect(UsageTable.parse(''), isNull);
      expect(UsageTable.parse('# Notes\n\nnothing here\n'), isNull);
      expect(UsageTable.parse('# Other\n\n$header| s-1 | 1 | 1 | 1 | 1 | 1 | 1 |\n'), isNull);
    });

    test('DSH-14.g: a missing usage file is no text, so the chart is empty', () async {
      final b = LocalBackend(files: MemoryFileAccess(memoryFiles()), runner: FakeRunner(createdIssue12), repoRoot: memRoot);
      expect(await b.loadUsage(), isNull);
    });

    test('DSH-14.a: the file is read from SCRUM.d/usage.md and parsed', () async {
      final b = LocalBackend(files: MemoryFileAccess(memoryFiles(extra: {memUsagePath: usageFile})), runner: FakeRunner(createdIssue12), repoRoot: memRoot);
      expect(UsageTable.parse((await b.loadUsage())!)!, hasLength(3));
    });
  });

  group('the meters (DSH-14.b, DSH-14.c)', () {
    final rows = UsageTable.parse(usageFile)!;

    test('DSH-14.b: there are two meters, the session and the week, on a scale from 0 to 100', () {
      expect(UsageMeter.values, [UsageMeter.session, UsageMeter.week]);
      expect(UsageChart.scaleMax, 100);
      expect(UsageChart.position(-5), 0);
      expect(UsageChart.position(42), 42);
      expect(UsageChart.position(130), 100);
    });

    test('DSH-14.c: a row with a before and an after reading gives a bar from before to after, naming its block', () {
      final bars = UsageChart.bars(rows, UsageMeter.session);
      expect(bars.map((b) => [b.block, b.from, b.to]), [['sprint-1', 20, 32]]);
      expect(UsageChart.bars(rows, UsageMeter.week).map((b) => [b.block, b.from, b.to]), [['sprint-1', 10, 16]]);
    });

    test('DSH-14.c: a row that lacks one of the two readings draws no bar', () {
      const only = [UsageRow(block: 'a', beforeSession: 1), UsageRow(block: 'b', afterSession: 2)];
      expect(UsageChart.bars(only, UsageMeter.session), isEmpty);
    });
  });

  group('the estimate band (DSH-14.d)', () {
    test('DSH-14.d: a row with an estimate gives a band from the before reading, as wide as the estimate plus and minus 20 percent', () {
      final bands = UsageChart.bands(UsageTable.parse(usageFile)!, UsageMeter.session);
      expect(bands.map((b) => b.block), ['sprint-1', 'sprint-2']);
      expect(bands[0].from, 20);
      expect(bands[0].low, closeTo(28, 1e-9));
      expect(bands[0].to, closeTo(32, 1e-9));
      expect(bands[1].low, closeTo(40 + 12 * 0.8, 1e-9));
      expect(bands[1].to, closeTo(40 + 12 * 1.2, 1e-9));
    });

    test('DSH-14.d: a row with no estimate or no before reading draws no band; the week uses the weekly cells', () {
      final rows = UsageTable.parse(usageFile)!;
      expect(UsageChart.bands(rows, UsageMeter.week).map((b) => b.block), ['sprint-1']);
      expect(UsageChart.bands(const [UsageRow(block: 'x', estimateSession: 5)], UsageMeter.session), isEmpty);
      expect(UsageChart.bands(const [UsageRow(block: 'x', beforeSession: 5)], UsageMeter.session), isEmpty);
    });
  });

  group('the projection (DSH-14.e)', () {
    final rows = UsageTable.parse(usageFile)!;

    test('DSH-14.e: the first sprint block with no after reading is projected: before plus estimate', () {
      final p = UsageChart.projection(rows, sprints, UsageMeter.session)!;
      expect([p.block, p.from, p.to], ['sprint-2', 40, 52]);
    });

    test('DSH-14.e: a sprint with an after reading is not projected; stories are never projected', () {
      expect(UsageChart.projection(rows, const Sprint(blocks: [Block(id: 'sprint-1', kind: BlockKind.sprint, name: 'One')]), UsageMeter.session), isNull);
      expect(UsageChart.projection(rows, const Sprint(blocks: [Block(id: 'story-1', kind: BlockKind.story, name: 'S')]), UsageMeter.session), isNull);
    });

    test('DSH-14.e: with no before reading or no estimate there is no projection', () {
      expect(UsageChart.projection(rows, sprints, UsageMeter.week), isNull, reason: 'sprint-2 has no estimate on the week');
      expect(UsageChart.projection(const [], sprints, UsageMeter.session), isNull);
    });
  });

  group('over 100 (DSH-14.f)', () {
    test('DSH-14.f: a value above 100 is over and keeps its real number; 100 and below are not', () {
      expect(UsageChart.overHundred(100.5), isTrue);
      expect(UsageChart.overHundred(130), isTrue);
      expect(UsageChart.overHundred(100), isFalse);
      expect(UsageChart.overHundred(0), isFalse);
      final bar = UsageChart.bars(const [UsageRow(block: 'x', beforeSession: 90, afterSession: 130)], UsageMeter.session).single;
      expect(bar.to, 130, reason: 'the real number stays in the data for the tooltip');
      expect(UsageChart.position(bar.to), 100);
    });
  });
}
