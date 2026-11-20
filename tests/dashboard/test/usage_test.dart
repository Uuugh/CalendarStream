// Tests DSH-09.a (edit on the card, written to the sprint file, via the page), DSH-09.c (bar per story, warning color
// above the estimate), DSH-09.d (sprint line adds up), and DSH-01.c (Reload reads everything again).
// One run covers each ID named in the test name. Logic rows use the domain classes alone; UI rows use the widgets.
import 'package:dashboard/features/dashboard/data/command_result.dart';
import 'package:dashboard/features/dashboard/domain/points_format.dart';
import 'package:dashboard/features/dashboard/domain/sprint.dart';
import 'package:dashboard/features/dashboard/domain/sprint_edit.dart';
import 'package:dashboard/features/dashboard/domain/stage.dart';
import 'package:dashboard/features/dashboard/domain/story.dart';
import 'package:dashboard/features/dashboard/domain/usage_summary.dart';
import 'package:dashboard/features/dashboard/ui/sprint_board.dart';
import 'package:dashboard/features/dashboard/ui/usage_colors.dart';
import 'package:dashboard/features/dashboard/ui/usage_panel.dart';
import 'package:dashboard/theme/app_theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import '../support/fixtures.dart';
import '../support/memory_file_access.dart';
import '../support/mutable_runner.dart';
import '../support/page_harness.dart';
import '../support/theme_colors.dart';

const sprint = Sprint(goal: 'G', review: 'R', retrospective: 'T', stories: [
  Story(id: 'S-1', title: 'First story', stage: Stage.build, estimate: 3, usage: 1.5),
  Story(id: 'S-2', title: 'Second story', stage: Stage.build, estimate: 2, usage: 4),
  Story(id: 'S-3', title: 'Third story', stage: Stage.done),
]);

LinearProgressIndicator bar(WidgetTester t, String key) => t.widget<LinearProgressIndicator>(find.byKey(Key(key)));

Color? barColor(WidgetTester t, String key) {
  final b = bar(t, key);
  return b.valueColor?.value ?? b.color;
}

void main() {
  group('logic', () {
    test('DSH-09.a: setEstimate and setUsage change that story only, keep goal, review, retrospective', () {
      final e = SprintEdit.setEstimate(sprint, 'S-1', 5);
      expect(e.stories.first.estimate, 5);
      expect(e.stories.first.usage, 1.5);
      expect([e.goal, e.review, e.retrospective], ['G', 'R', 'T']);
      expect(e.stories[1], same(sprint.stories[1]));
      final u = SprintEdit.setUsage(sprint, 'S-3', 2.5);
      expect(u.stories.last.usage, 2.5);
      expect([u.goal, u.review, u.retrospective], ['G', 'R', 'T']);
    });

    test('DSH-09.a: a missing story, a negative or NaN value, or an unchanged value returns the same sprint', () {
      expect(SprintEdit.setEstimate(sprint, 'NOPE', 1), same(sprint));
      expect(SprintEdit.setUsage(sprint, 'NOPE', 1), same(sprint));
      expect(SprintEdit.setEstimate(sprint, 'S-1', -1), same(sprint));
      expect(SprintEdit.setUsage(sprint, 'S-1', double.nan), same(sprint));
      expect(SprintEdit.setEstimate(sprint, 'S-1', 3), same(sprint));
      expect(SprintEdit.setUsage(sprint, 'S-1', 1.5), same(sprint));
    });

    test('DSH-09.a: points are formatted without a trailing zero and parsed with a comma or spaces', () {
      expect(PointsFormat.format(3.0), '3');
      expect(PointsFormat.format(2.5), '2.5');
      expect(PointsFormat.parse(' 2,5 '), 2.5);
      expect(PointsFormat.parse('4'), 4);
      expect(PointsFormat.parse('-1'), isNull);
      expect(PointsFormat.parse('abc'), isNull);
      expect(PointsFormat.parse('NaN'), isNull);
    });

    test('DSH-09.c: isOver is true only when usage is above the estimate; fraction is clamped', () {
      expect(UsageSummary.isOver(sprint.stories[0]), isFalse);
      expect(UsageSummary.isOver(sprint.stories[1]), isTrue);
      expect(UsageSummary.isOver(sprint.stories[2]), isFalse);
      expect(UsageSummary.fraction(1.5, 3), 0.5);
      expect(UsageSummary.fraction(4, 2), 1);
      expect(UsageSummary.fraction(0, 2), 0);
      expect(UsageSummary.fraction(1, 0), 1);
    });

    test('DSH-09.d: the summary adds up estimates and usage of all stories', () {
      final s = UsageSummary(sprint);
      expect(s.totalEstimate, 5);
      expect(s.totalUsage, 5.5);
      expect(s.over, isTrue);
      expect(UsageSummary(const Sprint(goal: 'x')).totalEstimate, 0);
    });

    test('DSH-09.c and DSH-01.g: above the estimate the bar color is the warn token (THM-02.j) in light and dark; otherwise it is another theme color', () {
      expect(UsageColors.of(AppTheme.light, over: true), const Color(0xFF946A24));
      expect(UsageColors.of(AppTheme.dark, over: true), const Color(0xFFFBBF24));
      for (final theme in [AppTheme.light, AppTheme.dark]) {
        expect(UsageColors.of(theme, over: true), StatusColors.of(theme).warn);
        expect(UsageColors.of(theme, over: false), isNot(StatusColors.of(theme).warn));
        expect(themeColors(theme), contains(UsageColors.of(theme, over: false).toARGB32()));
      }
    });
  });

  group('panel', () {
    testWidgets('DSH-09.c and DSH-09.d and DSH-01.g: one row and bar per story, warn token only when over, sprint line adds up, in light and dark', (t) async {
      bigView(t);
      for (final theme in [AppTheme.light, AppTheme.dark]) {
      await t.pumpWidget(testApp(const Scaffold(body: UsagePanel(sprint: sprint)), theme: theme));
      await t.pumpAndSettle();
      final warn = theme == AppTheme.light ? const Color(0xFF946A24) : const Color(0xFFFBBF24);
      final under = UsageColors.of(theme, over: false);
      for (final id in ['S-1', 'S-2', 'S-3']) {
        expect(find.byKey(Key('usage-row-$id')), findsOneWidget, reason: id);
        expect(find.byKey(Key('usage-bar-$id')), findsOneWidget, reason: id);
      }
      expect(find.text('Usage: 1.5 / Estimate: 3'), findsOneWidget);
      expect(find.text('Usage: 4 / Estimate: 2'), findsOneWidget);
      expect(bar(t, 'usage-bar-S-1').value, 0.5);
      expect(bar(t, 'usage-bar-S-2').value, 1);
      expect(bar(t, 'usage-bar-S-3').value, 0);
      expect(barColor(t, 'usage-bar-S-1'), under);
      expect(barColor(t, 'usage-bar-S-2'), warn);
      expect(barColor(t, 'usage-bar-S-3'), under);
      // Sprint line: 5 estimate, 5.5 usage, over, so the total bar is in the warning color.
      expect(find.byKey(const Key('usage-total')), findsOneWidget);
      final total = [
        for (final w in t.widgetList<Text>(find.descendant(of: find.byKey(const Key('usage-total')), matching: find.byType(Text)))) w.data ?? ''
      ].join(' ');
      final own = t.widgetList(find.byKey(const Key('usage-total'))).whereType<Text>().map((w) => w.data ?? '').join(' ');
      expect('$total $own', allOf(contains('5.5'), contains('5')));
      expect(bar(t, 'usage-bar-total').value, 1);
      expect(barColor(t, 'usage-bar-total'), warn);
      }
    });
  });

  group('board', () {
    testWidgets('DSH-09.a: editing the estimate and the usage on a card fires onChanged with the edited sprint', (t) async {
      bigView(t);
      final changes = <Sprint>[];
      await t.pumpWidget(testApp(Scaffold(body: SprintBoard(sprint: sprint, onChanged: changes.add))));
      await t.pumpAndSettle();
      await t.tap(find.byKey(const Key('estimate-S-1')));
      await t.pumpAndSettle();
      await t.enterText(find.byKey(const Key('estimate-field-S-1')), '5');
      await t.tap(find.byKey(const Key('points-save')));
      await t.pumpAndSettle();
      expect(changes, hasLength(1));
      expect(changes.last.stories.first.estimate, 5);
      expect(changes.last.review, 'R');
      await t.tap(find.byKey(const Key('usage-S-3')));
      await t.pumpAndSettle();
      await t.enterText(find.byKey(const Key('usage-field-S-3')), '2,5');
      await t.tap(find.byKey(const Key('points-save')));
      await t.pumpAndSettle();
      expect(changes, hasLength(2));
      expect(changes.last.stories.last.usage, 2.5);
    });
  });

  group('page', () {
    const sprintPath = 'repo/SCRUM.d/sprint.md';
    const reqDir = 'repo/requirements';
    late MemoryFileAccess files;
    late MutableRunner runner;

    String sprintFile(String goal, String story) => '''# Sprint

Goal: $goal

## Stories

| story | title | items | stage | assignee | estimate | usage |
|---|---|---|---|---|---|---|
| S-1 | $story | AAA-01 | Build | Ann | 3 | 1.5 |

## Review

Looked fine.

## Retrospective

Do more of X.
''';

    Future<void> pump(WidgetTester t, String goal, String tracker) async {
      files = MemoryFileAccess({
        sprintPath: sprintFile(goal, 'First story'),
        '$reqDir/alpha.md': reqFile(['| AAA-01 | backlog | Alpha one. | — | — |', '| AAA-02 | backlog | Alpha two. | — | — |']),
      });
      runner = MutableRunner(CommandResult(exitCode: 0, stdout: tracker));
      await pumpPage(t, files: files, runner: runner, sprintPath: sprintPath, requirementsDir: reqDir);
    }

    testWidgets('DSH-09.a: editing on a card through the page writes the sprint file and keeps review and retrospective', (t) async {
      await pump(t, 'Page goal', issuesJson([]));
      expect(find.textContaining('Page goal'), findsOneWidget);
      await t.tap(find.byKey(const Key('estimate-S-1')));
      await t.pumpAndSettle();
      await t.enterText(find.byKey(const Key('estimate-field-S-1')), '6');
      await t.tap(find.byKey(const Key('points-save')));
      await t.pumpAndSettle();
      final saved = files.files[sprintPath]!;
      final row = saved.split('\n').firstWhere((l) => l.contains('S-1'));
      expect(row.split('|').map((c) => c.trim()), containsAllInOrder(['S-1', 'First story', 'AAA-01', 'Build', 'Ann', '6', '1.5']));
      expect(saved, contains('Looked fine.'));
      expect(saved, contains('Do more of X.'));
      expect(saved, contains('Goal: Page goal'));
      await t.tap(find.byKey(const Key('usage-S-1')));
      await t.pumpAndSettle();
      await t.enterText(find.byKey(const Key('usage-field-S-1')), '7');
      await t.tap(find.byKey(const Key('points-save')));
      await t.pumpAndSettle();
      final row2 = files.files[sprintPath]!.split('\n').firstWhere((l) => l.contains('S-1'));
      expect(row2.split('|').map((c) => c.trim()), containsAllInOrder(['Ann', '6', '7']));
      // The page's panel shows the new values and the over state (7 > 6).
      expect(find.text('Usage: 7 / Estimate: 6'), findsWidgets);
    });

    testWidgets('DSH-01.c: Reload reads the sprint file, the requirement files and the issues again', (t) async {
      await pump(t, 'Old goal', issuesJson([issueJson(8, 'Old issue')]));
      expect(find.textContaining('Old goal'), findsOneWidget);
      expect(find.textContaining('Alpha two.'), findsOneWidget);
      expect(find.textContaining('Old issue'), findsWidgets);
      final calls = runner.calls.length;
      files.files[sprintPath] = sprintFile('New goal', 'Renamed story');
      files.files['$reqDir/alpha.md'] = reqFile(['| AAA-01 | backlog | Alpha one. | — | — |', '| AAA-02 | backlog | Alpha changed. | — | — |']);
      runner.result = CommandResult(exitCode: 0, stdout: issuesJson([issueJson(9, 'New issue')]));
      await t.tap(find.byKey(const Key('reload-button')));
      await t.pumpAndSettle();
      expect(runner.calls.length, greaterThan(calls));
      expect(find.textContaining('New goal'), findsOneWidget);
      expect(find.textContaining('Old goal'), findsNothing);
      expect(find.textContaining('Renamed story'), findsWidgets);
      expect(find.textContaining('Alpha changed.'), findsOneWidget);
      expect(find.textContaining('Alpha two.'), findsNothing);
      expect(find.textContaining('New issue'), findsWidgets);
      expect(find.textContaining('Old issue'), findsNothing);
    });
  });
}
