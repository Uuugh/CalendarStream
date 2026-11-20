// Tests the page: DSH-01.a (files touched, no token), DSH-01.b (tracker failure shown, requirements still shown),
// DSH-03.b, DSH-03.c, DSH-04 a-d (the filters in the UI), DSH-05 a-f (issue list), DSH-01.f (load failures), DSH-03.d (status messages), DSH-04.e (applied filter shown).
// One run covers each ID named in the test name.
import 'package:dashboard/features/dashboard/data/command_result.dart';
import 'package:dashboard/features/dashboard/data/issue_service.dart';
import 'package:dashboard/features/dashboard/data/requirement_repository.dart';
import 'package:dashboard/features/dashboard/data/sprint_repository.dart';
import 'package:dashboard/features/dashboard/domain/dashboard_limits.dart';
import 'package:dashboard/features/dashboard/ui/dashboard_page.dart';
import 'package:dashboard/l10n/app_localizations.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import '../support/failing_file_access.dart';
import '../support/fixtures.dart';
import '../support/memory_file_access.dart';
import '../support/page_harness.dart';

// Requirements after the sprint drops BBB-01: AAA-01 proposed, AAA-02 backlog, GGG-01 proposed.
// Issues after the sprint drops #7: 8 open alpha AAA-01, 9 closed, 10 open beta.
final tracker = CommandResult(exitCode: 0, stdout: issuesJson([
  issueJson(7, 'Named issue'),
  issueJson(8, 'Issue eight', feature: 'alpha', requirement: 'AAA-01'),
  issueJson(9, 'Issue nine', state: 'CLOSED'),
  issueJson(10, 'Issue ten', feature: 'beta', requirement: 'BBB-09'),
]));

void main() {
  late RecordingFileAccess files;
  late FakeRunner runner;
  Future<void> pump(WidgetTester t, CommandResult result) async {
    files = RecordingFileAccess(MemoryFileAccess(pageFiles()));
    runner = FakeRunner(result);
    await pumpPage(t, files: files, runner: runner);
  }

  testWidgets('DSH-01.a: loading reads only the sprint file and requirement files, writes nothing, sends no token', (t) async {
    await pump(t, tracker);
    for (final p in files.reads) {
      expect(p == memSprintPath || p.startsWith(memRequirementsDir), isTrue, reason: 'read $p');
    }
    expect(files.reads, contains(memSprintPath));
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
    expect(find.textContaining('Gamma one.'), findsNothing); // proposed, not selected
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

  testWidgets('DSH-05.e: an issue without feature or requirement shows a dash', (t) async {
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
        for (final s in ['proposed', 'backlog']) {
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

  testWidgets('DSH-05.d and DSH-05.e: an issue shows the requirement of its Requirement: line, a dash when there is none', (t) async {
    await pump(t, tracker);
    expect(find.text('Issue eight | open | alpha | AAA-01 | -'), findsOneWidget);
    expect(find.text('Issue ten | open | beta | BBB-09 | -'), findsOneWidget);
    await pump(t, CommandResult(exitCode: 0, stdout: issuesJson([issueJson(12, 'No feature', requirement: 'AAA-02'), issueJson(13, 'No requirement', feature: 'alpha')])));
    expect(find.text('No feature | open | - | AAA-02 | -'), findsOneWidget);
    expect(find.text('No requirement | open | alpha | - | -'), findsOneWidget);
  });

  testWidgets('DSH-05.f: when the loaded issues reach the limit the page says only the newest are listed; below it, it does not', (t) async {
    final atLimit = [for (var n = DashboardLimits.issues + 100; n > 100; n--) issueJson(n, 'Issue $n')];
    expect(atLimit, hasLength(DashboardLimits.issues));
    await pump(t, CommandResult(exitCode: 0, stdout: issuesJson(atLimit)));
    expect(find.text('Only the newest ${DashboardLimits.issues} issues are listed'), findsOneWidget);
    await pump(t, CommandResult(exitCode: 0, stdout: issuesJson(atLimit.take(DashboardLimits.issues - 1).toList())));
    expect(find.textContaining('Only the newest'), findsNothing);
  });

  testWidgets('DSH-01.f: an unreadable sprint file is reported with the reason; requirements and issues still work', (t) async {
    final files = FailingFileAccess(MemoryFileAccess(pageFiles()), failsOn: (p) => p == memSprintPath, reason: 'sprint disk gone');
    await pumpPage(t, files: files, runner: FakeRunner(tracker));
    expect(find.textContaining('Could not be read: '), findsOneWidget);
    expect(find.textContaining('sprint disk gone'), findsOneWidget);
    expect(find.textContaining('Alpha two blank.'), findsOneWidget);
    expect(find.textContaining('Issue eight'), findsOneWidget);
  });

  testWidgets('DSH-01.f: unreadable requirement files are reported with the reason; the sprint and the issues still work', (t) async {
    final files = FailingFileAccess(MemoryFileAccess(pageFiles()),
        failsOn: (p) => p.startsWith(memRequirementsDir), reason: 'requirements disk gone');
    await pumpPage(t, files: files, runner: FakeRunner(tracker));
    expect(find.textContaining('Could not be read: '), findsOneWidget);
    expect(find.textContaining('requirements disk gone'), findsOneWidget);
    expect(find.text('Sprint goal: Page goal'), findsOneWidget);
    expect(find.byKey(const Key('card-S-1')), findsOneWidget);
    expect(find.textContaining('Issue eight'), findsOneWidget);
  });

  testWidgets('DSH-01.f: both unreadable are reported each once, the issues still work', (t) async {
    final files = FailingFileAccess(MemoryFileAccess(pageFiles()), failsOn: (_) => true);
    await pumpPage(t, files: files, runner: FakeRunner(tracker));
    expect(find.textContaining('Could not be read: '), findsNWidgets(2));
    expect(find.textContaining('Issue eight'), findsOneWidget);
  });

  testWidgets('DSH-03.d: a requirement status is shown as the message of the locale (msg:dshStatusProposed, msg:dshStatusBacklog)', (t) async {
    final files = MemoryFileAccess(pageFiles());
    bigView(t);
    await t.pumpWidget(testApp(
      DashboardPage(
        sprints: SprintRepository(files: files, path: memSprintPath),
        requirements: RequirementRepository(files: files, directory: memRequirementsDir),
        issues: IssueService(runner: FakeRunner(tracker)),
      ),
      locale: const Locale('de'),
    ));
    await t.pumpAndSettle();
    final de = lookupAppLocalizations(const Locale('de'));
    expect(de.dshStatusProposed, isNot('proposed'));
    // The status filter dropdown of the requirement list offers the messages, not the raw words.
    await t.tap(find.text(de.dshStatusBacklog).first);
    await t.pumpAndSettle();
    expect(find.text(de.dshStatusProposed), findsWidgets);
    expect(find.text('proposed'), findsNothing);
    await t.tap(find.text(de.dshAll).last);
    await t.pumpAndSettle();
    expect(find.textContaining('(${de.dshStatusProposed})'), findsNWidgets(2));
    expect(find.textContaining('(proposed)'), findsNothing);
  });

  testWidgets('DSH-03.d: in English a requirement row shows its status as msg:dshStatusBacklog or msg:dshStatusProposed', (t) async {
    await pump(t, tracker);
    expect(find.textContaining('alpha (backlog): Alpha two blank.'), findsOneWidget);
    await t.tap(find.text('backlog'));
    await t.pumpAndSettle();
    await t.tap(find.text('All').last);
    await t.pumpAndSettle();
    expect(find.textContaining('alpha (proposed): Alpha one.'), findsOneWidget);
  });

  testWidgets('DSH-04.e: a filter shows an applied value no entry has: the issue list status Closed with only open issues', (t) async {
    await pump(t, CommandResult(exitCode: 0, stdout: issuesJson([issueJson(8, 'Only open', feature: 'alpha')])));
    // Choose feature alpha, then reload with no alpha issue: the applied feature is still shown.
    await t.tap(find.text('All').at(1));
    await t.pumpAndSettle();
    await t.tap(find.text('alpha').last);
    await t.pumpAndSettle();
    runner.result = const CommandResult(exitCode: 0, stdout: '[]');
    await t.tap(find.byKey(const Key('reload-button')));
    await t.pumpAndSettle();
    expect(find.text('alpha'), findsWidgets);
    expect(find.text('0 of 0 shown'), findsWidgets);
  });
}
