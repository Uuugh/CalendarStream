// Holds: reading and creating issues in the issue tracker (DSH-01.a, DSH-01.b, DSH-05, DSH-05.b, DSH-08.c) through the
// user's own signed-in `gh`; no token is handled here. Depends on: CommandRunner, IssueTracker, Issue, NewIssue, DashboardLimits.
// Used by: the dashboard page, the New issue dialog.
// Reads or writes: the issue tracker, through the runner.

import 'dart:convert';

import '../domain/dashboard_limits.dart';
import '../domain/issue.dart';
import '../domain/new_issue.dart';
import 'command_runner.dart';
import 'issue_tracker.dart';
import 'issue_tracker_exception.dart';

/// Wraps the issue tracker; holds no state.
class IssueService extends IssueTracker {
  const IssueService({required this.runner});

  final CommandRunner runner;

  static const executable = 'gh';
  static const listArguments = [
    'issue', 'list', '--state', 'all', '--limit', '${DashboardLimits.issues}',
    '--json', 'number,title,state,labels,assignees,body',
  ];
  static const _featurePrefix = 'feature:';
  static final _requirementLine = RegExp(r'^Requirement:[ \t]*(\S+)', multiLine: true);

  /// All issues, open and closed. Throws [IssueTrackerException] with the reason when the tracker cannot be reached.
  @override
  Future<List<Issue>> load() async {
    final out = await _run(listArguments);
    try {
      return parse(out);
    } on FormatException catch (e) {
      throw IssueTrackerException(e.message);
    }
  }

  static final _issueNumber = RegExp(r'/issues/(\d+)');

  /// The labels of a new issue: `issue` and `feature:<feature>` (DSH-05.b).
  static List<String> labelsFor(NewIssue issue) =>
      ['issue', if (issue.feature != null) '$_featurePrefix${issue.feature}'];

  /// The arguments that create an issue.
  static List<String> createArguments(String title, String body, List<String> labels) =>
      ['issue', 'create', '--title', title, '--body', body, for (final l in labels) ...['--label', l]];

  /// The issue number in the output of `gh issue create`, or null.
  static int? numberFrom(String output) => int.tryParse(_issueNumber.firstMatch(output)?.group(1) ?? '');

  /// Creates [issue] (DSH-08.e) without closing it; returns its number ([create] closes it afterwards when
  /// [NewIssue.closed]). Throws [IssueTrackerException] with the reason when nothing was created.
  @override
  Future<int> createOpen(NewIssue issue) async {
    final created = await _run(createArguments(issue.title, issue.body, labelsFor(issue)));
    final number = numberFrom(created);
    if (number == null) throw IssueTrackerException(created.trim().isEmpty ? 'no issue number' : created.trim());
    return number;
  }

  /// Closes issue [number]. Throws [IssueTrackerException] with the reason when it cannot.
  @override
  Future<void> close(int number) async {
    await _run(['issue', 'close', '$number']);
  }

  /// Runs `gh` with [arguments]; returns its output or throws [IssueTrackerException] with the reason.
  Future<String> _run(List<String> arguments) async {
    try {
      final r = await runner.run(executable, arguments);
      if (r.exitCode != 0) {
        final reason = r.stderr.trim();
        throw IssueTrackerException(reason.isEmpty ? 'exit code ${r.exitCode}' : reason);
      }
      return r.stdout;
    } on IssueTrackerException {
      rethrow;
    } catch (e) {
      throw IssueTrackerException('$e');
    }
  }

  /// The issues in [json] (the output of `gh issue list --json`). Throws [FormatException] when it is not a list.
  static List<Issue> parse(String json) {
    final data = jsonDecode(json);
    if (data is! List) throw const FormatException('unexpected answer');
    return [for (final m in data) _issue(m as Map<String, dynamic>)];
  }

  static Issue _issue(Map<String, dynamic> m) {
    String? feature;
    for (final l in (m['labels'] as List? ?? const [])) {
      final name = '${(l as Map)['name']}';
      if (name.startsWith(_featurePrefix)) {
        feature = name.substring(_featurePrefix.length).trim();
        break;
      }
    }
    final requirement = _requirementLine.firstMatch('${m['body'] ?? ''}')?.group(1);
    final assignees = [for (final a in (m['assignees'] as List? ?? const [])) '${(a as Map)['login']}'];
    return Issue(
      number: m['number'] as int,
      title: '${m['title']}',
      status: '${m['state']}'.toUpperCase() == 'CLOSED' ? IssueStatus.closed : IssueStatus.open,
      feature: (feature == null || feature.isEmpty) ? null : feature,
      requirement: requirement,
      assignee: assignees.join(', '),
    );
  }
}
