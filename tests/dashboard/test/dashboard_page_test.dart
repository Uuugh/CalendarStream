// Tests the page: DSH-01.a (files touched, no token), DSH-01.b (tracker failure shown, requirements still shown),
// DSH-03.b, DSH-03.c, DSH-04 a-d (the filters in the UI), DSH-05 a-c (issue list).
// One run covers each ID named in the test name.
import 'dart:io';

import 'package:dashboard/features/dashboard/data/command_result.dart';
import 'package:dashboard/features/dashboard/data/issue_service.dart';
import 'package:dashboard/features/dashboard/data/requirement_repository.dart';
import 'package:dashboard/features/dashboard/data/sprint_repository.dart';
import 'package:dashboard/features/dashboard/ui/dashboard_page.dart';
import 'package:dashboard/l10n/app_localizations.dart';
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_test/flutter_test.dart';

import '../support/fixtures.dart';

// Requirements after the sprint drops BBB-01: AAA-01 proposed, AAA-02 backlog, GGG-01 done.
// Issues after the sprint drops #7: 8 open alpha AAA-01, 9 closed, 10 open beta.
final tracker = CommandResult(exitCode: 0, stdout: issuesJson([
  issueJson(7, 'Named issue'),
  issueJson(8, 'Issue eight', feature: 'alpha', requirement: 'AAA-01'),
  issueJson(9, 'Issue nine', state: 'CLOSED'),
  issueJson(10, 'Issue ten', feature: 'beta', requirement: 'BBB-09'),
]));

void main() {
  late Directory repo;
  late RecordingFileAccess files;
  late FakeRunner runner;
  setUp(() => repo = makeRepo());
  tearDown(() => repo.deleteSync(recursive: true));

  Future<void> pump(WidgetTester t, CommandResult result) async {
    final dir = makePageRepo(repo);
    files = RecordingFileAccess(disk);
    runner = FakeRunner(result);
    t.view.physicalSize = const Size(2400, 1800);
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.reset);
    await t.pumpWidget(MaterialApp(
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: AppLocalizations.supportedLocales,
      home: DashboardPage(
        sprints: SprintRepository(files: files, path: join(repo, 'SCRUM.d/sprint.md')),
        requirements: RequirementRepository(files: files, directory: dir),
        issues: IssueService(runner: runner),
      ),
    ));
    // Real file IO needs real time: alternate real waits with frame pumps until the sprint has loaded.
    for (var i = 0; i < 200 && find.text('Sprint goal: Page goal').evaluate().isEmpty; i++) {
      await t.runAsync(() => Future<void>.delayed(const Duration(milliseconds: 20)));
      await t.pump();
    }
    await t.pumpAndSettle();
  }

  testWidgets('DSH-01.a: loading reads only the sprint file and requirement files, writes nothing, sends no token', (t) async {
    await pump(t, tracker);
    final reqDir = join(repo, 'requirements');
    final sprint = join(repo, 'SCRUM.d/sprint.md');
    for (final p in files.reads) {
      expect(p == sprint || p.replaceAll('\\', '/').startsWith(reqDir.replaceAll('\\', '/')), isTrue, reason: 'read $p');
    }
    expect(files.reads, contains(sprint));
    expect(files.writes, isEmpty);
    final call = runner.calls.expand((c) => c).join(' ').toLowerCase();
    expect(call, isNot(contains('token')));
    expect(call, isNot(contains('authorization')));
  });

  testWidgets('DSH-01.b: a tracker failure shows the reason and the requirements list still shows', (t) async {
    await pump(t, const CommandResult(exitCode: 1, stderr: 'gh: not signed in'));
    expect(find.textContaining('The issue tracker could not be reached: gh: not signed in'), findsOneWidget);
    expect(find.text('Requirements'), findsWidgets);
    expect(find.textContaining('Alpha two blank.'), findsOneWidget);
  });

  testWidgets('DSH-03.b: a requirement named by a story is not listed, even with every status chosen', (t) async {
    await pump(t, tracker);
    await t.pump();
    // BBB-01 is backlog status and named by S-1: it must not appear.
    expect(find.textContaining('Beta one.'), findsNothing);
    expect(find.textContaining('BBB-01'), findsNothing);
  });

  testWidgets('DSH-03.c and DSH-04.d: the requirement status filter starts as backlog; count shows shown of total', (t) async {
    await pump(t, tracker);
    expect(find.textContaining('Alpha two blank.'), findsOneWidget); // blank counts as backlog
    expect(find.textContaining('Alpha one.'), findsNothing); // proposed, not selected
    expect(find.textContaining('Gamma one.'), findsNothing); // done
    expect(find.text('1 of 3 shown'), findsOneWidget);
  });

  testWidgets('DSH-05.a and DSH-05.c: the issue status filter starts as open; a named issue is not listed', (t) async {
    await pump(t, tracker);
    expect(find.textContaining('Issue eight'), findsOneWidget);
    expect(find.textContaining('Issue ten'), findsOneWidget);
    expect(find.textContaining('Issue nine'), findsNothing); // closed
    expect(find.textContaining('Named issue'), findsNothing); // #7 named by S-1
    expect(find.text('2 of 3 shown'), findsOneWidget);
  });

  testWidgets('DSH-05.b: an issue without feature or requirement shows a dash', (t) async {
    await pump(t, CommandResult(exitCode: 0, stdout: issuesJson([issueJson(11, 'Bare issue')])));
    expect(find.textContaining('Bare issue'), findsOneWidget);
    expect(find.textContaining('open | - | - | -'), findsOneWidget);
  });

  testWidgets('DSH-04.b and DSH-04.d: typing in a requirement text box filters ignoring case and updates the count', (t) async {
    await pump(t, tracker);
    final boxes = find.byType(TextField);
    expect(boxes, findsWidgets);
    // First text box belongs to the requirement list; issue list shows requirement IDs AAA-01 and BBB-09.
    await t.enterText(boxes.last, 'bbb');
    await t.pumpAndSettle();
    expect(find.textContaining('Issue ten'), findsOneWidget);
    expect(find.textContaining('Issue eight'), findsNothing);
    expect(find.text('1 of 3 shown'), findsWidgets);
    await t.enterText(boxes.last, 'zzz');
    await t.pumpAndSettle();
    expect(find.text('0 of 3 shown'), findsOneWidget);
  });

  testWidgets('DSH-04.a and DSH-04.c: the filters are dropdowns that start as All or the list start', (t) async {
    await pump(t, tracker);
    // Two lists, each with a feature and a status dropdown (4 in all), plus labels.
    expect(find.text('Feature'), findsWidgets);
    expect(find.text('Status'), findsWidgets);
    expect(find.text('Requirement'), findsWidgets);
    expect(find.text('All'), findsWidgets);
  });

  testWidgets('DSH-04.c: choosing All in the requirement status dropdown lists every status', (t) async {
    await pump(t, tracker);
    await t.tap(find.text('backlog'));
    await t.pumpAndSettle();
    await t.tap(find.text('All').last);
    await t.pumpAndSettle();
    expect(find.textContaining('Alpha one.'), findsOneWidget);
    expect(find.textContaining('Alpha two blank.'), findsOneWidget);
    expect(find.textContaining('Gamma one.'), findsOneWidget);
    expect(find.text('3 of 3 shown'), findsOneWidget);
    expect(find.textContaining('Beta one.'), findsNothing); // still named by the sprint (DSH-03.b)
  });

  testWidgets('DSH-04.c: the status dropdown offers the statuses of what is listed', (t) async {
    await pump(t, tracker);
    await t.tap(find.text('backlog'));
    await t.pumpAndSettle();
    for (final s in ['proposed', 'backlog', 'done']) {
      expect(find.text(s), findsWidgets, reason: s);
    }
  });

  testWidgets('DSH-04.c and DSH-05.a: choosing All in the issue status dropdown lists closed issues too', (t) async {
    await pump(t, tracker);
    // The issue list status starts as open.
    await t.tap(find.text('open').first);
    await t.pumpAndSettle();
    await t.tap(find.text('All').last);
    await t.pumpAndSettle();
    expect(find.textContaining('Issue nine'), findsOneWidget);
    expect(find.text('3 of 3 shown'), findsWidgets);
  });

  testWidgets('DSH-04.b: the requirement list text box filters requirement IDs ignoring case', (t) async {
    await pump(t, tracker);
    await t.tap(find.text('backlog'));
    await t.pumpAndSettle();
    await t.tap(find.text('All').last);
    await t.pumpAndSettle();
    await t.enterText(find.byType(TextField).first, 'gg');
    await t.pumpAndSettle();
    expect(find.textContaining('Gamma one.'), findsOneWidget);
    expect(find.textContaining('Alpha one.'), findsNothing);
    expect(find.text('1 of 3 shown'), findsWidgets);
  });

  testWidgets('DSH-04.a and DSH-04.d: choosing a feature in the issue list keeps that feature and combines with status', (t) async {
    await pump(t, tracker);
    await t.tap(find.text('All').at(1)); // the issue list's feature dropdown
    await t.pumpAndSettle();
    await t.tap(find.text('beta').last);
    await t.pumpAndSettle();
    expect(find.textContaining('Issue ten'), findsOneWidget);
    expect(find.textContaining('Issue eight'), findsNothing);
    expect(find.text('1 of 3 shown'), findsWidgets);
    // Feature beta and status open and requirement text 'aaa' together keep nothing.
    await t.enterText(find.byType(TextField).last, 'aaa');
    await t.pumpAndSettle();
    expect(find.textContaining('Issue ten'), findsNothing);
    expect(find.text('0 of 3 shown'), findsOneWidget);
  });
}
