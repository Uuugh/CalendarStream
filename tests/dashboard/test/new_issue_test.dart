// Tests DSH-08 a-h (the new-issue form and the creation of an issue) and the write side of DSH-01.a (the only tracker
// commands that write are issue create and issue close; no token in any argument).
// One run covers each ID named in the test name.
import 'package:dashboard/features/dashboard/data/command_result.dart';
import 'package:dashboard/features/dashboard/data/command_runner.dart';
import 'package:dashboard/features/dashboard/data/issue_service.dart';
import 'package:dashboard/features/dashboard/data/issue_partial_failure.dart';
import 'package:dashboard/features/dashboard/data/issue_tracker_exception.dart';
import 'package:dashboard/features/dashboard/domain/new_issue.dart';
import 'package:dashboard/features/dashboard/domain/requirement.dart';
import 'package:dashboard/features/dashboard/domain/requirement_choices.dart';
import 'package:dashboard/features/dashboard/ui/new_issue_dialog.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import '../support/fixtures.dart';
import '../support/memory_file_access.dart';
import '../support/page_harness.dart';

const reqs = [
  Requirement(id: 'AAA-01', status: 'proposed', statement: 'a1', feature: 'alpha'),
  Requirement(id: 'AAA-02', status: 'backlog', statement: 'a2', feature: 'alpha'),
  Requirement(id: 'BBB-01', status: 'backlog', statement: 'b1', feature: 'beta'),
];

/// Answers `issue list` with [listJson], `issue create` with [createResult], `issue close` with [closeResult], anything else with success.
class TrackerRunner implements CommandRunner {
  TrackerRunner({this.listJson = '[]', this.createResult, this.closeResult});
  String listJson;
  CommandResult? createResult;
  CommandResult? closeResult;
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
    if (arguments.length >= 2 && arguments[0] == 'issue' && arguments[1] == 'close' && closeResult != null) {
      return closeResult!;
    }
    return const CommandResult(exitCode: 0);
  }
}

void main() {
  group('NewIssue.body (DSH-08.e)', () {
    test('DSH-08.e: description plus a final Requirement line after a blank line', () {
      expect(NewIssue(title: 't', description: '  Text here \n', requirement: 'AAA-01').body, 'Text here\n\nRequirement: AAA-01');
    });
    test('DSH-08.e: no description gives only the Requirement line', () {
      expect(NewIssue(title: 't', requirement: 'AAA-01').body, 'Requirement: AAA-01');
    });
    test('DSH-08.e: neither gives an empty body; description alone is trimmed', () {
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

  group('IssueService.create (DSH-08.e, DSH-08.d, DSH-08.g, DSH-01.a)', () {
    test('DSH-08.e and DSH-01.a: create runs gh issue create with title, body, labels; returns the number', () async {
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

    test('DSH-08.e: the feature label is omitted when there is no feature', () async {
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

    test('DSH-08.g: a closed issue whose close fails throws IssuePartialFailure with the number and reason, after one create', () async {
      final runner = TrackerRunner(closeResult: const CommandResult(exitCode: 1, stderr: 'no permission'));
      await expectLater(
          IssueService(runner: runner).create(NewIssue(title: 'T', closed: true)),
          throwsA(isA<IssuePartialFailure>()
              .having((e) => e.number, 'number', 11)
              .having((e) => e.reason, 'reason', 'no permission')
              .having((e) => e is IssueTrackerException, 'not a tracker exception', false)));
      expect(runner.calls.where((c) => c[2] == 'create'), hasLength(1));
    });

    test('DSH-08.g: close(N) runs one gh issue close N and nothing else; a failing close throws', () async {
      final ok = TrackerRunner();
      await IssueService(runner: ok).close(11);
      expect(ok.calls, [['gh', 'issue', 'close', '11']]);
      final bad = TrackerRunner(closeResult: const CommandResult(exitCode: 1, stderr: 'nope'));
      await expectLater(IssueService(runner: bad).close(11), throwsA(anything));
      expect(bad.calls, hasLength(1));
    });
  });

  group('NewIssueDialog (DSH-08)', () {
      late bool? result;
    Future<void> open(WidgetTester t, TrackerRunner runner) async {
      result = null;
      t.view.physicalSize = const Size(1600, 1400);
      t.view.devicePixelRatio = 1;
      addTearDown(t.view.reset);
      await t.pumpWidget(testApp(Builder(
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

    testWidgets('DSH-08.e: saving creates the issue with feature label and Requirement line and pops true', (t) async {
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

    testWidgets('DSH-08.b and DSH-08.e: choosing closed also closes the issue', (t) async {
      final runner = TrackerRunner();
      await open(t, runner);
      await t.enterText(find.byKey(const Key('issue-title')), 'T');
      await choose(t, 'issue-status', 'closed');
      await t.tap(find.byKey(const Key('issue-save')));
      await t.pumpAndSettle();
      expect(runner.calls.last, ['gh', 'issue', 'close', '11']);
      expect(result, isTrue);
    });

    testWidgets('DSH-08.d: a failure keeps the form filled and shows the reason (msg:dshIssueFailed)', (t) async {
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

  group('NewIssueDialog cancel and partial failure', () {
    late bool? result;
    Future<void> open(WidgetTester t, TrackerRunner runner) async {
      result = null;
      bigView(t, size: const Size(1600, 1400));
      await t.pumpWidget(testApp(Builder(
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

    Future<void> chooseClosed(WidgetTester t) async {
      await t.tap(find.byKey(const Key('issue-status')));
      await t.pumpAndSettle();
      await t.tap(find.text('closed').last);
      await t.pumpAndSettle();
    }

    const partial = CommandResult(exitCode: 1, stderr: 'no permission');

    testWidgets('DSH-08.h: Cancel (msg:cancel) closes the form without creating an issue and pops false', (t) async {
      final runner = TrackerRunner();
      await open(t, runner);
      await t.enterText(find.byKey(const Key('issue-title')), 'Never saved');
      await t.pump();
      expect(find.descendant(of: find.byKey(const Key('issue-cancel')), matching: find.text('Cancel')), findsOneWidget);
      await t.tap(find.byKey(const Key('issue-cancel')));
      await t.pumpAndSettle();
      expect(find.byKey(const Key('issue-save')), findsNothing);
      expect(result, isFalse);
      expect(runner.calls, isEmpty);
    });

    testWidgets('DSH-08.b: the status dropdown offers open and closed and nothing else', (t) async {
      await open(t, TrackerRunner());
      final dd = t.widget<DropdownButton<String?>>(find.byKey(const Key('issue-status')));
      expect(dd.items!.map((i) => i.value), ['open', 'closed']);
      await t.tap(find.byKey(const Key('issue-status')));
      await t.pumpAndSettle();
      expect(find.text('All'), findsNothing);
    });

    testWidgets('DSH-08.g: when the close fails the form says the issue exists with its number and the reason, and stays', (t) async {
      final runner = TrackerRunner(closeResult: partial);
      await open(t, runner);
      await t.enterText(find.byKey(const Key('issue-title')), 'Half done');
      await chooseClosed(t);
      await t.tap(find.byKey(const Key('issue-save')));
      await t.pumpAndSettle();
      expect(find.text('Issue #11 was created, but a later step failed: no permission'), findsOneWidget);
      expect(find.byKey(const Key('issue-save')), findsOneWidget);
      expect(result, isNull);
      expect(runner.calls.where((c) => c[2] == 'create'), hasLength(1));
    });

    testWidgets('DSH-08.g: saving again runs close only, never create again, and then pops true', (t) async {
      final runner = TrackerRunner(closeResult: partial);
      await open(t, runner);
      await t.enterText(find.byKey(const Key('issue-title')), 'Half done');
      await chooseClosed(t);
      await t.tap(find.byKey(const Key('issue-save')));
      await t.pumpAndSettle();
      runner.closeResult = null; // the close now succeeds
      await t.tap(find.byKey(const Key('issue-save')));
      await t.pumpAndSettle();
      expect(runner.calls.where((c) => c[2] == 'create'), hasLength(1));
      expect(runner.calls.where((c) => c[2] == 'close'), hasLength(2));
      expect(runner.calls.last, ['gh', 'issue', 'close', '11']);
      expect(result, isTrue);
    });

    testWidgets('DSH-08.g: a second failing save still creates nothing and keeps the message', (t) async {
      final runner = TrackerRunner(closeResult: partial);
      await open(t, runner);
      await t.enterText(find.byKey(const Key('issue-title')), 'Half done');
      await chooseClosed(t);
      await t.tap(find.byKey(const Key('issue-save')));
      await t.pumpAndSettle();
      await t.tap(find.byKey(const Key('issue-save')));
      await t.pumpAndSettle();
      expect(runner.calls.where((c) => c[2] == 'create'), hasLength(1));
      expect(find.textContaining('Issue #11 was created'), findsOneWidget);
    });

    testWidgets('DSH-08.g and DSH-08.h: Cancel after a partial failure pops true because the issue exists', (t) async {
      final runner = TrackerRunner(closeResult: partial);
      await open(t, runner);
      await t.enterText(find.byKey(const Key('issue-title')), 'Half done');
      await chooseClosed(t);
      await t.tap(find.byKey(const Key('issue-save')));
      await t.pumpAndSettle();
      await t.tap(find.byKey(const Key('issue-cancel')));
      await t.pumpAndSettle();
      expect(result, isTrue);
      expect(runner.calls.where((c) => c[2] == 'create'), hasLength(1));
    });
  });

  group('DashboardPage new issue', () {
    late TrackerRunner runner;

    Future<void> pump(WidgetTester t) async {
      runner = TrackerRunner(listJson: issuesJson([issueJson(8, 'Existing issue')]));
      await pumpPage(t, files: MemoryFileAccess(pageFiles()), runner: runner);
    }

    Future<void> fillAndSave(WidgetTester t, {bool closed = false}) async {
      await t.tap(find.byKey(const Key('new-issue-button')));
      await t.pumpAndSettle();
      await t.enterText(find.byKey(const Key('issue-title')), 'Created from form');
      await t.pump();
      if (closed) {
        await t.tap(find.byKey(const Key('issue-status')));
        await t.pumpAndSettle();
        await t.tap(find.text('closed').last);
        await t.pumpAndSettle();
      }
      runner.listJson = issuesJson([
        issueJson(8, 'Existing issue'),
        issueJson(11, 'Created from form', state: closed ? 'CLOSED' : 'OPEN'),
      ]);
      await t.tap(find.byKey(const Key('issue-save')));
      await t.pumpAndSettle();
    }

    testWidgets('DSH-08.f: after saving, the issue appears in the issue list', (t) async {
      await pump(t);
      expect(find.textContaining('Existing issue'), findsOneWidget);
      expect(find.textContaining('Created from form'), findsNothing);
      await fillAndSave(t);
      expect(find.textContaining('Created from form'), findsOneWidget);
      expect(runner.calls.where((c) => c.length > 2 && c[2] == 'create'), hasLength(1));
    });

    testWidgets('DSH-08.f: a closed new issue is listed too, because the issue status filter becomes All', (t) async {
      await pump(t);
      expect(find.text('1 of 2 shown'), findsNothing);
      await fillAndSave(t, closed: true);
      expect(find.textContaining('Created from form'), findsOneWidget);
      expect(find.text('2 of 2 shown'), findsOneWidget);
      // The filter shows the applied value: All (DSH-04.e).
      expect(find.text('open'), findsNothing);
    });

    testWidgets('DSH-08.d: a failed creation leaves the form open, filled and with the reason', (t) async {
      await pump(t);
      runner.createResult = const CommandResult(exitCode: 1, stderr: 'rate limited');
      await t.tap(find.byKey(const Key('new-issue-button')));
      await t.pumpAndSettle();
      await t.enterText(find.byKey(const Key('issue-title')), 'Keep me');
      await t.pump();
      await t.tap(find.byKey(const Key('issue-save')));
      await t.pumpAndSettle();
      expect(find.text('The issue could not be created: rate limited'), findsOneWidget);
      expect(t.widget<TextField>(find.byKey(const Key('issue-title'))).controller!.text, 'Keep me');
    });
  });
}
