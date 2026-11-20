// Tests DSH-08 a-d (the new-issue form) and the write side of DSH-01.a (the only tracker commands that write are
// issue create and issue close; no token in any argument). One run covers each ID named in the test name.
import 'dart:io';

import 'package:dashboard/features/dashboard/data/command_result.dart';
import 'package:dashboard/features/dashboard/data/command_runner.dart';
import 'package:dashboard/features/dashboard/data/issue_service.dart';
import 'package:dashboard/features/dashboard/data/issue_tracker_exception.dart';
import 'package:dashboard/features/dashboard/data/requirement_repository.dart';
import 'package:dashboard/features/dashboard/data/sprint_repository.dart';
import 'package:dashboard/features/dashboard/domain/new_issue.dart';
import 'package:dashboard/features/dashboard/domain/requirement.dart';
import 'package:dashboard/features/dashboard/domain/requirement_choices.dart';
import 'package:dashboard/features/dashboard/ui/dashboard_page.dart';
import 'package:dashboard/features/dashboard/ui/new_issue_dialog.dart';
import 'package:dashboard/l10n/app_localizations.dart';
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_test/flutter_test.dart';

import '../support/fixtures.dart';

const reqs = [
  Requirement(id: 'AAA-01', status: 'proposed', statement: 'a1', feature: 'alpha'),
  Requirement(id: 'AAA-02', status: 'backlog', statement: 'a2', feature: 'alpha'),
  Requirement(id: 'BBB-01', status: 'backlog', statement: 'b1', feature: 'beta'),
];

/// Answers `issue list` with [listJson], `issue create` with [createResult], anything else with success.
class TrackerRunner implements CommandRunner {
  TrackerRunner({this.listJson = '[]', this.createResult});
  String listJson;
  CommandResult? createResult;
  final calls = <List<String>>[];

  @override
  Future<CommandResult> run(String executable, List<String> arguments) async {
    calls.add([executable, ...arguments]);
    if (arguments.length >= 2 && arguments[0] == 'issue' && arguments[1] == 'list') {
      return CommandResult(exitCode: 0, stdout: listJson);
    }
    if (arguments.length >= 2 && arguments[0] == 'issue' && arguments[1] == 'create') {
      return createResult ?? const CommandResult(exitCode: 0, stdout: 'https://example.test/o/r/issues/11\n');
    }
    return const CommandResult(exitCode: 0);
  }
}

void main() {
  group('NewIssue.body (DSH-08.c)', () {
    test('DSH-08.c: description plus a final Requirement line after a blank line', () {
      expect(NewIssue(title: 't', description: '  Text here \n', requirement: 'AAA-01').body, 'Text here\n\nRequirement: AAA-01');
    });
    test('DSH-08.c: no description gives only the Requirement line', () {
      expect(NewIssue(title: 't', requirement: 'AAA-01').body, 'Requirement: AAA-01');
    });
    test('DSH-08.c: neither gives an empty body; description alone is trimmed', () {
      expect(NewIssue(title: 't').body, '');
      expect(NewIssue(title: 't', description: ' x ').body, 'x');
    });
  });

  group('RequirementChoices (DSH-08.a)', () {
    test('DSH-08.a: features lists each feature once', () {
      expect(RequirementChoices.features(reqs).toSet(), {'alpha', 'beta'});
      expect(RequirementChoices.features(reqs), hasLength(2));
    });
    test('DSH-08.a: requirementsOf lists only the chosen feature', () {
      expect(RequirementChoices.requirementsOf(reqs, 'alpha').toSet(), {'AAA-01', 'AAA-02'});
      expect(RequirementChoices.requirementsOf(reqs, 'beta'), ['BBB-01']);
    });
    test('DSH-08.a: keepRequirement keeps a requirement of the feature and clears one of another feature', () {
      expect(RequirementChoices.keepRequirement(reqs, 'alpha', 'AAA-01'), 'AAA-01');
      expect(RequirementChoices.keepRequirement(reqs, 'beta', 'AAA-01'), isNull);
    });
  });

  group('IssueService.create (DSH-08.c, DSH-08.d, DSH-01.a)', () {
    test('DSH-08.c and DSH-01.a: create runs gh issue create with title, body, labels; returns the number', () async {
      final runner = TrackerRunner();
      final n = await IssueService(runner: runner)
          .create(NewIssue(title: 'T', description: 'D', feature: 'alpha', requirement: 'AAA-01'));
      expect(n, 11);
      expect(runner.calls, hasLength(1));
      expect(runner.calls.single, [
        'gh', 'issue', 'create', '--title', 'T', '--body', 'D\n\nRequirement: AAA-01',
        '--label', 'issue', '--label', 'feature:alpha',
      ]);
    });

    test('DSH-08.c: the feature label is omitted when there is no feature', () async {
      final runner = TrackerRunner();
      await IssueService(runner: runner).create(NewIssue(title: 'T'));
      expect(runner.calls.single.join(' '), isNot(contains('feature:')));
      expect(runner.calls.single, containsAllInOrder(['--label', 'issue']));
    });

    test('DSH-08.b and DSH-01.a: a closed issue is created then closed with issue close N', () async {
      final runner = TrackerRunner();
      await IssueService(runner: runner).create(NewIssue(title: 'T', closed: true));
      expect(runner.calls, hasLength(2));
      expect(runner.calls[1], ['gh', 'issue', 'close', '11']);
    });

    test('DSH-08.b: an open issue is not closed', () async {
      final runner = TrackerRunner();
      await IssueService(runner: runner).create(NewIssue(title: 'T'));
      expect(runner.calls.where((c) => c.contains('close')), isEmpty);
    });

    test('DSH-01.a: the only writing tracker commands are issue create and issue close; no token in any argument', () async {
      final runner = TrackerRunner();
      final s = IssueService(runner: runner);
      await s.create(NewIssue(title: 'T', closed: true, feature: 'alpha', requirement: 'AAA-01'));
      await s.load();
      for (final c in runner.calls) {
        expect(c.first, 'gh');
        expect(['list', 'create', 'close'], contains(c[2]));
        expect(c[1], 'issue');
        final text = c.join(' ').toLowerCase();
        for (final w in ['token', 'authorization', 'secret', 'password']) {
          expect(text, isNot(contains(w)));
        }
      }
    });

    test('DSH-08.d: a failing create throws IssueTrackerException with the reason', () async {
      final runner = TrackerRunner(createResult: const CommandResult(exitCode: 1, stderr: ' denied \n'));
      await expectLater(IssueService(runner: runner).create(NewIssue(title: 'T')),
          throwsA(isA<IssueTrackerException>().having((e) => e.reason, 'reason', 'denied')));
    });

    test('DSH-08.d: output without an issue URL throws IssueTrackerException', () async {
      final runner = TrackerRunner(createResult: const CommandResult(exitCode: 0, stdout: 'done'));
      await expectLater(IssueService(runner: runner).create(NewIssue(title: 'T')), throwsA(isA<IssueTrackerException>()));
    });
  });

  group('NewIssueDialog (DSH-08)', () {
    Widget app(Widget home) => MaterialApp(
          localizationsDelegates: const [
            AppLocalizations.delegate,
            GlobalMaterialLocalizations.delegate,
            GlobalWidgetsLocalizations.delegate,
            GlobalCupertinoLocalizations.delegate,
          ],
          supportedLocales: AppLocalizations.supportedLocales,
          home: home,
        );

    late bool? result;
    Future<void> open(WidgetTester t, TrackerRunner runner) async {
      result = null;
      t.view.physicalSize = const Size(1600, 1400);
      t.view.devicePixelRatio = 1;
      addTearDown(t.view.reset);
      await t.pumpWidget(app(Builder(
        builder: (c) => Scaffold(
          body: TextButton(
            key: const Key('open'),
            onPressed: () async => result = await showDialog<bool>(
                context: c, builder: (_) => NewIssueDialog(issues: IssueService(runner: runner), requirements: reqs)),
            child: const Text('go'),
          ),
        ),
      )));
      await t.tap(find.byKey(const Key('open')));
      await t.pumpAndSettle();
    }

    Future<void> choose(WidgetTester t, String key, String text) async {
      await t.tap(find.byKey(Key(key)));
      await t.pumpAndSettle();
      await t.tap(find.text(text).last);
      await t.pumpAndSettle();
    }

    bool saveEnabled(WidgetTester t) {
      final b = find.byKey(const Key('issue-save'));
      final w = t.widget(b);
      return (w as dynamic).onPressed != null;
    }

    testWidgets('DSH-08: the form has title, description, feature, requirement and status controls', (t) async {
      await open(t, TrackerRunner());
      for (final k in ['issue-title', 'issue-description', 'issue-feature', 'issue-requirement', 'issue-status', 'issue-save']) {
        expect(find.byKey(Key(k)), findsOneWidget, reason: k);
      }
      expect(find.text('New issue'), findsWidgets);
    });

    testWidgets('DSH-08.c: Save is off until the trimmed title is filled', (t) async {
      await open(t, TrackerRunner());
      expect(saveEnabled(t), isFalse);
      await t.enterText(find.byKey(const Key('issue-title')), '   ');
      await t.pump();
      expect(saveEnabled(t), isFalse);
      await t.enterText(find.byKey(const Key('issue-title')), 'A title');
      await t.pump();
      expect(saveEnabled(t), isTrue);
    });

    testWidgets('DSH-08.b: status starts open and offers open and closed', (t) async {
      await open(t, TrackerRunner());
      final dd = t.widget<DropdownButton<String?>>(find.byKey(const Key('issue-status')));
      expect(dd.value, 'open');
      await t.tap(find.byKey(const Key('issue-status')));
      await t.pumpAndSettle();
      expect(find.text('open'), findsWidgets);
      expect(find.text('closed'), findsWidgets);
    });

    testWidgets('DSH-08.a: requirement dropdown lists the chosen feature only; choosing another feature clears it', (t) async {
      await open(t, TrackerRunner());
      await choose(t, 'issue-feature', 'alpha');
      await t.tap(find.byKey(const Key('issue-requirement')));
      await t.pumpAndSettle();
      expect(find.text('AAA-01'), findsWidgets);
      expect(find.text('AAA-02'), findsWidgets);
      expect(find.text('BBB-01'), findsNothing);
      await t.tap(find.text('AAA-01').last);
      await t.pumpAndSettle();
      expect(t.widget<DropdownButton<String?>>(find.byKey(const Key('issue-requirement'))).value, 'AAA-01');
      await choose(t, 'issue-feature', 'beta');
      expect(t.widget<DropdownButton<String?>>(find.byKey(const Key('issue-requirement'))).value, isNull);
      await t.tap(find.byKey(const Key('issue-requirement')));
      await t.pumpAndSettle();
      expect(find.text('BBB-01'), findsWidgets);
      expect(find.text('AAA-02'), findsNothing);
    });

    testWidgets('DSH-08.c: saving creates the issue with feature label and Requirement line and pops true', (t) async {
      final runner = TrackerRunner();
      await open(t, runner);
      await t.enterText(find.byKey(const Key('issue-title')), 'My title');
      await t.enterText(find.byKey(const Key('issue-description')), 'My text');
      await choose(t, 'issue-feature', 'alpha');
      await choose(t, 'issue-requirement', 'AAA-02');
      await t.tap(find.byKey(const Key('issue-save')));
      await t.pumpAndSettle();
      expect(runner.calls, hasLength(1));
      expect(runner.calls.single, containsAllInOrder(['--title', 'My title', '--body', 'My text\n\nRequirement: AAA-02']));
      expect(runner.calls.single, containsAllInOrder(['--label', 'feature:alpha']));
      expect(result, isTrue);
      expect(find.byKey(const Key('issue-save')), findsNothing);
    });

    testWidgets('DSH-08.b and DSH-08.c: choosing closed also closes the issue', (t) async {
      final runner = TrackerRunner();
      await open(t, runner);
      await t.enterText(find.byKey(const Key('issue-title')), 'T');
      await choose(t, 'issue-status', 'closed');
      await t.tap(find.byKey(const Key('issue-save')));
      await t.pumpAndSettle();
      expect(runner.calls.last, ['gh', 'issue', 'close', '11']);
      expect(result, isTrue);
    });

    testWidgets('DSH-08.d: a failure keeps the form filled and shows the reason', (t) async {
      final runner = TrackerRunner(createResult: const CommandResult(exitCode: 1, stderr: 'rate limited'));
      await open(t, runner);
      await t.enterText(find.byKey(const Key('issue-title')), 'Keep me');
      await t.enterText(find.byKey(const Key('issue-description')), 'Keep text');
      await choose(t, 'issue-feature', 'alpha');
      await t.tap(find.byKey(const Key('issue-save')));
      await t.pumpAndSettle();
      expect(find.textContaining('rate limited'), findsOneWidget);
      expect(find.byKey(const Key('issue-save')), findsOneWidget);
      expect(result, isNull);
      expect(t.widget<TextField>(find.byKey(const Key('issue-title'))).controller!.text, 'Keep me');
      expect(t.widget<TextField>(find.byKey(const Key('issue-description'))).controller!.text, 'Keep text');
      expect(t.widget<DropdownButton<String?>>(find.byKey(const Key('issue-feature'))).value, 'alpha');
    });
  });

  group('DashboardPage new issue (DSH-08.c)', () {
    late Directory repo;
    setUp(() => repo = makeRepo());
    tearDown(() => repo.deleteSync(recursive: true));

    testWidgets('DSH-08.c: after saving, the issue appears in the issue list', (t) async {
      final dir = makePageRepo(repo);
      final files = RecordingFileAccess(disk);
      final runner = TrackerRunner(listJson: issuesJson([issueJson(8, 'Existing issue')]));
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
      for (var i = 0; i < 200 && find.text('Sprint goal: Page goal').evaluate().isEmpty; i++) {
        await t.runAsync(() => Future<void>.delayed(const Duration(milliseconds: 20)));
        await t.pump();
      }
      await t.pumpAndSettle();
      expect(find.textContaining('Existing issue'), findsOneWidget);
      expect(find.textContaining('Created from form'), findsNothing);

      await t.tap(find.byKey(const Key('new-issue-button')));
      await t.pumpAndSettle();
      await t.enterText(find.byKey(const Key('issue-title')), 'Created from form');
      await t.pump();
      runner.listJson = issuesJson([issueJson(8, 'Existing issue'), issueJson(11, 'Created from form')]);
      await t.tap(find.byKey(const Key('issue-save')));
      for (var i = 0; i < 200 && (find.byType(NewIssueDialog).evaluate().isNotEmpty || find.textContaining('Created from form').evaluate().isEmpty); i++) {
        await t.runAsync(() => Future<void>.delayed(const Duration(milliseconds: 20)));
        await t.pump();
      }
      await t.pumpAndSettle();
      expect(find.textContaining('Created from form'), findsOneWidget);
      expect(runner.calls.where((c) => c.length > 2 && c[2] == 'create'), hasLength(1));
    });
  });
}
