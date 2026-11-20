// Tests the issue side of the data layer (IssueService): DSH-05 (a-e) reading, DSH-09.d creating, DSH-13.e status
// labels, DSH-13.f arguments, DSH-13.g failures, DSH-01.b (the tracker's reason), DSH-01.a (only the tracker's commands).
// A fake runner records every call; nothing runs gh. One run covers each ID named in the test name.
import 'dart:convert';

import 'package:dashboard/features/dashboard/data/command_result.dart';
import 'package:dashboard/features/dashboard/data/command_runner.dart';
import 'package:dashboard/features/dashboard/data/issue_service.dart';
import 'package:dashboard/features/dashboard/data/issue_tracker_exception.dart';
import 'package:dashboard/features/dashboard/domain/dashboard_limits.dart';
import 'package:dashboard/features/dashboard/domain/issue.dart';
import 'package:dashboard/features/dashboard/domain/new_issue.dart';
import 'package:dashboard/features/dashboard/domain/status.dart';
import 'package:flutter_test/flutter_test.dart';

import '../support/fixtures.dart';

class ThrowingRunner implements CommandRunner {
  @override
  Future<CommandResult> run(String executable, List<String> arguments) => throw Exception('no such program');
}

void main() {
  group('reading issues (DSH-05)', () {
    test('DSH-05: number, title, status, feature, requirement and assignee are read', () {
      final list = IssueService.parse(issuesJson([
        issueJson(1, 'One', assignee: 'ann', feature: 'alpha', requirement: 'AAA-01', labels: ['planned']),
      ]));
      final i = list.single;
      expect([i.number, i.title, i.status, i.feature, i.requirement, i.assignee], [1, 'One', Status.planned, 'alpha', 'AAA-01', 'ann']);
    });

    test('DSH-05.a: the status is the one of the labels proposed, backlog, planned or done', () {
      for (final s in Status.values) {
        expect(IssueService.parse(issuesJson([issueJson(1, 'x', labels: [s.name])])).single.status, s);
      }
    });

    test('DSH-05.a: an issue with none of those labels counts as backlog', () {
      expect(IssueService.parse(issuesJson([issueJson(1, 'x')])).single.status, Status.backlog);
      expect(IssueService.parse(issuesJson([issueJson(1, 'x', labels: ['bug', 'Done'])])).single.status, Status.backlog);
    });

    test('DSH-05.b: the feature is the name after feature: in the labels', () {
      expect(IssueService.parse(issuesJson([issueJson(1, 'x', feature: 'alpha')])).single.feature, 'alpha');
      expect(IssueService.parse(issuesJson([issueJson(1, 'x', labels: ['feature:  spaced '])])).single.feature, 'spaced');
    });

    test('DSH-05.c: the requirement is the ID on the line starting Requirement:', () {
      expect(IssueService.parse(issuesJson([issueJson(1, 'x', requirement: 'AAA-01.b')])).single.requirement, 'AAA-01.b');
    });

    test('DSH-05.c: Requirement: inside a line, in lower case, or with nothing after it is no requirement', () {
      for (final body in ['See Requirement: AAA-01', 'requirement: AAA-01', 'Requirement:', '']) {
        final json = jsonEncode([{'number': 1, 'title': 't', 'labels': [], 'assignees': [], 'body': body}]);
        expect(IssueService.parse(json).single.requirement, isNull, reason: body);
      }
    });

    test('DSH-05.d: an issue without a feature label or a Requirement line has none (the page shows a dash)', () {
      final i = IssueService.parse(issuesJson([issueJson(1, 'x')])).single;
      expect([i.feature, i.requirement, i.assignee], [null, null, '']);
      expect(IssueService.parse(issuesJson([issueJson(1, 'x', labels: ['feature:'])])).single.feature, isNull);
    });

    test('DSH-05.e: the list command asks for the number of issues in DEF-01, open issues only', () async {
      final runner = FakeRunner(CommandResult(exitCode: 0, stdout: issuesJson([])));
      await IssueService(runner: runner).load();
      expect(runner.calls.single, [
        'gh', 'issue', 'list', '--state', 'open', '--limit', '${DashboardLimits.issues}', '--json', 'number,title,labels,assignees,body',
      ]);
      expect(DashboardLimits.issues, 200);
    });

    test('DSH-05.e: the issues come back in the order the tracker gave them (newest first)', () {
      final list = IssueService.parse(issuesJson([issueJson(30, 'c'), issueJson(20, 'b'), issueJson(10, 'a')]));
      expect(list.map((i) => i.number), [30, 20, 10]);
    });

    test('DSH-05: an issue round trips through JSON', () {
      const i = Issue(number: 4, title: 'T', status: Status.done, feature: 'f', requirement: 'AAA-01', assignee: 'bo');
      final back = Issue.fromJson(i.toJson());
      expect([back.number, back.title, back.status, back.feature, back.requirement, back.assignee], [4, 'T', Status.done, 'f', 'AAA-01', 'bo']);
    });
  });

  group('creating an issue (DSH-09.d)', () {
    test('DSH-09.d: one status label is created, then exactly one issue with issue, feature and status labels and the Requirement line', () async {
      final runner = FakeRunner(createdIssue12);
      final n = await IssueService(runner: runner).create(const NewIssue(
          title: 'T', description: 'D', feature: 'alpha', requirement: 'AAA-01', status: Status.proposed));
      expect(n, 12);
      expect(runner.calls, [
        ['gh', 'label', 'create', 'proposed', '--force'],
        ['gh', 'issue', 'create', '--title', 'T', '--body', 'D\n\nRequirement: AAA-01', '--label', 'issue', '--label', 'feature:alpha', '--label', 'proposed'],
      ]);
    });

    test('DSH-09.d: with no feature there is no feature label; the status starts as backlog', () async {
      final runner = FakeRunner(createdIssue12);
      await IssueService(runner: runner).create(const NewIssue(title: 'T'));
      expect(runner.calls.last, ['gh', 'issue', 'create', '--title', 'T', '--body', '', '--label', 'issue', '--label', 'backlog']);
      expect(runner.calls.where((c) => c.contains('create') && c.contains('issue')), hasLength(1));
    });

    test('DSH-09.e: when the tracker refuses the reason is the trimmed stderr, and no second issue is tried', () async {
      final runner = FakeRunner(const CommandResult(exitCode: 1, stderr: ' denied \n'));
      await expectLater(IssueService(runner: runner).create(const NewIssue(title: 'T')),
          throwsA(isA<IssueTrackerException>().having((e) => e.reason, 'reason', 'denied')));
      expect(runner.calls.where((c) => c.contains('create') && c.contains('issue')), isEmpty);
    });

    test('DSH-09.e: output with no issue URL is a failure with the output as reason', () async {
      final runner = FakeRunner(const CommandResult(exitCode: 0, stdout: 'done'));
      await expectLater(IssueService(runner: runner).create(const NewIssue(title: 'T')),
          throwsA(isA<IssueTrackerException>().having((e) => e.reason, 'reason', 'done')));
    });
  });

  group('status labels (DSH-13.e)', () {
    test('DSH-13.e: view asks for the labels and the status labels are picked out, others ignored', () async {
      final runner = FakeRunner(viewResult(['issue', 'feature:alpha', 'planned']));
      expect(await IssueService(runner: runner).statusLabelsOf(5), [Status.planned]);
      expect(runner.calls.single, ['gh', 'issue', 'view', '5', '--json', 'labels']);
    });

    test('DSH-13.e: relabel creates the label, adds it and removes each other status label, and never touches open or closed', () async {
      final runner = FakeRunner(const CommandResult(exitCode: 0));
      await IssueService(runner: runner).relabel(5, [Status.proposed, Status.backlog], Status.planned);
      expect(runner.calls, [
        ['gh', 'label', 'create', 'planned', '--force'],
        ['gh', 'issue', 'edit', '5', '--add-label', 'planned', '--remove-label', 'proposed', '--remove-label', 'backlog'],
      ]);
      final text = runner.calls.expand((c) => c).join(' ');
      for (final w in ['close', 'reopen', '--state']) {
        expect(text, isNot(contains(w)));
      }
    });

    test('DSH-13.e: an issue that already has only that status label is left alone', () async {
      final runner = FakeRunner(const CommandResult(exitCode: 0));
      await IssueService(runner: runner).relabel(5, [Status.planned], Status.planned);
      expect(runner.calls, isEmpty);
    });

    test('DSH-13.e: an issue with no status label only gets the new one', () async {
      final runner = FakeRunner(const CommandResult(exitCode: 0));
      await IssueService(runner: runner).relabel(5, const [], Status.done);
      expect(runner.calls.last, ['gh', 'issue', 'edit', '5', '--add-label', 'done']);
    });
  });

  group('failures and arguments (DSH-01.b, DSH-13.f, DSH-13.g, DSH-01.a)', () {
    test('DSH-01.b and DSH-13.g: a non-zero exit throws with the trimmed stderr as the reason', () async {
      final runner = FakeRunner(const CommandResult(exitCode: 1, stderr: '  not signed in \n'));
      await expectLater(IssueService(runner: runner).load(), throwsA(isA<IssueTrackerException>().having((e) => e.reason, 'reason', 'not signed in')));
    });

    test('DSH-13.g: a non-zero exit without stderr gives the reason exit code N', () async {
      final runner = FakeRunner(const CommandResult(exitCode: 4));
      await expectLater(IssueService(runner: runner).load(), throwsA(isA<IssueTrackerException>().having((e) => e.reason, 'reason', 'exit code 4')));
    });

    test('DSH-01.b: a runner that throws, and output that is not an issue list, become an IssueTrackerException', () async {
      await expectLater(IssueService(runner: ThrowingRunner()).load(), throwsA(isA<IssueTrackerException>()));
      await expectLater(IssueService(runner: FakeRunner(CommandResult(exitCode: 0, stdout: jsonEncode({'a': 1})))).load(),
          throwsA(isA<IssueTrackerException>()));
      await expectLater(IssueService(runner: FakeRunner(const CommandResult(exitCode: 0, stdout: 'not json'))).load(),
          throwsA(isA<IssueTrackerException>()));
    });

    test('DSH-13.f: text with shell characters stays one argument each', () async {
      final runner = FakeRunner(createdIssue12);
      await IssueService(runner: runner).create(const NewIssue(title: 'x; rm -rf', description: r'$(id) `id` | a && b', feature: 'l1; l2'));
      expect(runner.calls.last, [
        'gh', 'issue', 'create', '--title', 'x; rm -rf', '--body', r'$(id) `id` | a && b', '--label', 'issue', '--label', 'feature:l1; l2', '--label', 'backlog',
      ]);
    });

    test('DSH-01.a: every call is gh label create, issue list, issue view, issue create or issue edit, with no token or secret', () async {
      final runner = FakeRunner(createdIssue12, handler: (a) => a.contains('list') ? CommandResult(exitCode: 0, stdout: issuesJson([])) : a.contains('view') ? viewResult(['backlog']) : createdIssue12);
      final s = IssueService(runner: runner);
      await s.load();
      await s.create(const NewIssue(title: 'T'));
      await s.relabel(3, await s.statusLabelsOf(3), Status.planned);
      for (final c in runner.calls) {
        expect(c.first, 'gh');
        expect(['label create', 'issue list', 'issue view', 'issue create', 'issue edit'], contains('${c[1]} ${c[2]}'.replaceAll(RegExp(r' \d+$'), '')), reason: '$c');
      }
      final text = runner.calls.expand((c) => c).join(' ').toLowerCase();
      for (final w in ['token', 'authorization', 'secret']) {
        expect(text, isNot(contains(w)));
      }
    });
  });
}
