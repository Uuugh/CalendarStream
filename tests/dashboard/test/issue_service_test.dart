// Tests DSH-05 (issue fields from the tracker), DSH-05.a, DSH-05.b, DSH-01.a (only the tracker is called, no token)
// and DSH-01.b (failure carries a reason). One run covers each ID named in the test name.
import 'dart:convert';

import 'package:dashboard/features/dashboard/data/command_result.dart';
import 'package:dashboard/features/dashboard/data/command_runner.dart';
import 'package:dashboard/features/dashboard/data/issue_service.dart';
import 'package:dashboard/features/dashboard/data/issue_tracker_exception.dart';
import 'package:dashboard/features/dashboard/domain/issue.dart';
import 'package:flutter_test/flutter_test.dart';

import '../support/fixtures.dart';

class ThrowingRunner implements CommandRunner {
  @override
  Future<CommandResult> run(String executable, List<String> arguments) => throw Exception('no such program');
}

void main() {
  test('DSH-05 and DSH-05.a: number, title, status (open or closed) and assignee are read', () {
    final list = IssueService.parse(issuesJson([
      issueJson(1, 'One', assignee: 'ann'),
      issueJson(2, 'Two', state: 'CLOSED'),
    ]));
    expect(list[0].number, 1);
    expect(list[0].title, 'One');
    expect(list[0].status, IssueStatus.open);
    expect(list[0].assignee, 'ann');
    expect(list[1].status, IssueStatus.closed);
    expect(list[1].assignee, '');
  });

  test('DSH-05.b: feature is the name after feature: in the labels', () {
    final i = IssueService.parse(issuesJson([issueJson(1, 'One', feature: 'alpha')])).single;
    expect(i.feature, 'alpha');
  });

  test('DSH-05.b: requirement is the ID on the line starting Requirement:', () {
    final i = IssueService.parse(issuesJson([issueJson(1, 'One', requirement: 'AAA-01')])).single;
    expect(i.requirement, 'AAA-01');
  });

  test('DSH-05.b: an issue without feature label or Requirement line has none (shown as a dash)', () {
    final i = IssueService.parse(issuesJson([issueJson(1, 'One')])).single;
    expect(i.feature, isNull);
    expect(i.requirement, isNull);
  });

  test('DSH-01.a: load asks only the tracker program, with no token or secret in its call', () async {
    final runner = FakeRunner(CommandResult(exitCode: 0, stdout: issuesJson([issueJson(1, 'One')])));
    final list = await IssueService(runner: runner).load();
    expect(list, hasLength(1));
    expect(runner.calls, hasLength(1));
    final call = runner.calls.single.join(' ').toLowerCase();
    expect(call, isNot(contains('token')));
    expect(call, isNot(contains('authorization')));
    expect(call, isNot(contains('secret')));
  });

  test('DSH-01.b: a non-zero exit throws with the trimmed stderr as reason', () async {
    final runner = FakeRunner(const CommandResult(exitCode: 1, stderr: '  not signed in \n'));
    await expectLater(
        IssueService(runner: runner).load(), throwsA(isA<IssueTrackerException>().having((e) => e.reason, 'reason', 'not signed in')));
  });

  test('DSH-01.b: a runner that throws becomes an IssueTrackerException', () async {
    await expectLater(IssueService(runner: ThrowingRunner()).load(), throwsA(isA<IssueTrackerException>()));
  });

  test('DSH-01.b: output that is not a list becomes an IssueTrackerException', () async {
    final runner = FakeRunner(CommandResult(exitCode: 0, stdout: jsonEncode({'a': 1})));
    await expectLater(IssueService(runner: runner).load(), throwsA(isA<IssueTrackerException>()));
  });
}
