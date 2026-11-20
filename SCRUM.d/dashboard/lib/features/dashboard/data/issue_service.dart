// Holds: reading issues from the issue tracker (DSH-01.a, DSH-01.b, DSH-05, DSH-05.b) through the user's own signed-in
// `gh`; no token is handled here. Depends on: CommandRunner, Issue. Used by: the dashboard page.
// Reads or writes: the issue tracker, through the runner.

import 'dart:convert';

import '../domain/issue.dart';
import 'command_runner.dart';
import 'issue_tracker_exception.dart';

/// Wraps the issue tracker; holds no state.
class IssueService {
  const IssueService({required this.runner});

  final CommandRunner runner;

  static const executable = 'gh';
  static const listArguments = [
    'issue', 'list', '--state', 'all', '--limit', '200',
    '--json', 'number,title,state,labels,assignees,body',
  ];
  static const _featurePrefix = 'feature:';
  static final _requirementLine = RegExp(r'^Requirement:[ \t]*(\S+)', multiLine: true);

  /// All issues, open and closed. Throws [IssueTrackerException] with the reason when the tracker cannot be reached.
  Future<List<Issue>> load() async {
    final String out;
    try {
      final r = await runner.run(executable, listArguments);
      if (r.exitCode != 0) {
        final reason = r.stderr.trim();
        throw IssueTrackerException(reason.isEmpty ? 'exit code ${r.exitCode}' : reason);
      }
      out = r.stdout;
    } on IssueTrackerException {
      rethrow;
    } catch (e) {
      throw IssueTrackerException('$e');
    }
    try {
      return parse(out);
    } on FormatException catch (e) {
      throw IssueTrackerException(e.message);
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
