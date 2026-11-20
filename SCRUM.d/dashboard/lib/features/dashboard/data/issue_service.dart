// Holds: reading, creating and relabelling issues in the issue tracker (DSH-01.a, DSH-01.b, DSH-05, DSH-09.d, DSH-13.e,
// DSH-13.f) through the user's own signed-in `gh`; no token is handled here. Depends on: CommandRunner, Issue, NewIssue,
// Status, DashboardLimits, IssueTrackerException. Used by: LocalBackend. Reads or writes: the issue tracker, through the runner.

import 'dart:convert';

import '../domain/dashboard_limits.dart';
import '../domain/issue.dart';
import '../domain/new_issue.dart';
import '../domain/status.dart';
import 'command_runner.dart';
import 'issue_tracker_exception.dart';

/// Wraps the issue tracker; holds no state. Every method throws [IssueTrackerException] with the reason on failure.
class IssueService {
  const IssueService({required this.runner});

  final CommandRunner runner;

  static const executable = 'gh';

  /// The open issues, newest first, at most [DashboardLimits.issues] (DSH-05.e).
  static const listArguments = [
    'issue', 'list', '--state', 'open', '--limit', '${DashboardLimits.issues}',
    '--json', 'number,title,labels,assignees,body',
  ];
  static const _featurePrefix = 'feature:';
  static final _requirementLine = RegExp(r'^Requirement:[ \t]*(\S+)', multiLine: true);
  static final _issueNumber = RegExp(r'/issues/(\d+)');

  /// The open issues. Throws when the tracker cannot be reached (DSH-01.b).
  Future<List<Issue>> load() async {
    final out = await _run(listArguments);
    try {
      return parse(out);
    } on FormatException catch (e) {
      throw IssueTrackerException(e.message);
    }
  }

  /// Creates [issue] with the label `issue`, its `feature:` label and its status label (DSH-09.d); returns its number.
  Future<int> create(NewIssue issue) async {
    await _run(labelArguments(issue.status));
    final created = await _run(createArguments(issue));
    final number = numberFrom(created);
    if (number == null) throw IssueTrackerException(created.trim().isEmpty ? 'no issue number' : created.trim());
    return number;
  }

  /// The status labels issue [number] has now (`gh issue view`); none means the issue counts as `backlog` (DSH-05.a).
  Future<List<Status>> statusLabelsOf(int number) async => statusLabels(await _run(viewArguments(number)));

  /// Gives issue [number] the status label [status] and takes the other status labels off, [current] being the ones
  /// it has (DSH-13.e); the issue's open or closed state is not touched.
  Future<void> relabel(int number, List<Status> current, Status status) async {
    if (current.length == 1 && current.contains(status)) return;
    await _run(labelArguments(status));
    await _run(editArguments(number, status, [for (final s in current) if (s != status) s]));
  }

  /// `gh label create <status> --force`: creates the label or updates it, so a missing label is made.
  static List<String> labelArguments(Status status) => ['label', 'create', status.name, '--force'];

  /// `gh issue create` with one `--label` per label of [issue].
  static List<String> createArguments(NewIssue issue) =>
      ['issue', 'create', '--title', issue.title, '--body', issue.body, for (final l in issue.labels) ...['--label', l]];

  /// `gh issue view <number> --json labels`.
  static List<String> viewArguments(int number) => ['issue', 'view', '$number', '--json', 'labels'];

  /// `gh issue edit <number> --add-label <status>` and one `--remove-label` for each of [remove].
  static List<String> editArguments(int number, Status status, List<Status> remove) =>
      ['issue', 'edit', '$number', '--add-label', status.name, for (final s in remove) ...['--remove-label', s.name]];

  /// The issue number in the output of `gh issue create`, or null.
  static int? numberFrom(String output) => int.tryParse(_issueNumber.firstMatch(output)?.group(1) ?? '');

  /// The status labels in the output of `gh issue view --json labels`.
  static List<Status> statusLabels(String json) {
    final data = jsonDecode(json);
    final labels = data is Map ? data['labels'] : null;
    return [
      for (final l in (labels as List? ?? const []))
        ?Status.tryName('${(l as Map)['name']}')
    ];
  }

  /// Runs `gh` with [arguments], each passed separately and never through a shell (DSH-13.f); returns its output or
  /// throws [IssueTrackerException] with the reason (DSH-13.g).
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
    Status? status;
    for (final l in (m['labels'] as List? ?? const [])) {
      final name = '${(l as Map)['name']}';
      if (feature == null && name.startsWith(_featurePrefix)) feature = name.substring(_featurePrefix.length).trim();
      final s = Status.tryName(name);
      if (s != null && (status == null || s.index > status.index)) status = s;
    }
    final requirement = _requirementLine.firstMatch('${m['body'] ?? ''}')?.group(1);
    final assignees = [for (final a in (m['assignees'] as List? ?? const [])) '${(a as Map)['login']}'];
    return Issue(
      number: m['number'] as int,
      title: '${m['title']}',
      status: status ?? Status.backlog,
      feature: (feature == null || feature.isEmpty) ? null : feature,
      requirement: requirement,
      assignee: assignees.join(', '),
    );
  }
}
