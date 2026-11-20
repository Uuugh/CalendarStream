// Holds: the web app's backend (DSH-01.e): every call is a request to the server (DSH-13.b), and an error answer becomes
// the exception LocalBackend would throw. Depends on: HttpTransport, SprintRepository (the file format), the domain,
// IssueTrackerException, StatusRefused. Used by: platform_backend_web.dart. Reads or writes: network, through the transport.

import 'dart:convert';

import '../domain/issue.dart';
import '../domain/new_issue.dart';
import '../domain/progress_entry.dart';
import '../domain/requirement.dart';
import '../domain/sprint.dart';
import '../domain/status.dart';
import '../domain/status_refused.dart';
import 'dashboard_backend.dart';
import 'http_reply.dart';
import 'http_transport.dart';
import 'issue_tracker_exception.dart';
import 'sprint_repository.dart';

/// [DashboardBackend] on the server's routes.
class HttpBackend implements DashboardBackend {
  const HttpBackend(this.transport);

  final HttpTransport transport;

  @override
  Future<Sprint> loadSprint() async {
    final reply = await transport.send('GET', '/api/sprint');
    return SprintRepository.parse(_ok(reply));
  }

  @override
  Future<void> saveSprint(Sprint sprint) async {
    _ok(await transport.send('PUT', '/api/sprint', body: SprintRepository.format(sprint)));
  }

  @override
  Future<List<Requirement>> loadRequirements() async =>
      [for (final m in await _list('/api/requirements')) Requirement.fromJson(m)];

  @override
  Future<void> setRequirementStatus(String id, Status status) async {
    _ok(await transport.send('PUT', '/api/requirements/$id/status', body: jsonEncode({'status': status.name})));
  }

  @override
  Future<List<Issue>> loadIssues() async => [for (final m in await _list('/api/issues')) Issue.fromJson(m)];

  @override
  Future<int> createIssue(NewIssue issue) async {
    final reply = await transport.send('POST', '/api/issues', body: jsonEncode(issue.toJson()));
    final number = _decode(_ok(reply));
    if (number is! Map || number['number'] is! int) throw const IssueTrackerException('no issue number');
    return number['number'] as int;
  }

  @override
  Future<void> setIssueStatus(int number, Status status) async {
    _ok(await transport.send('POST', '/api/issues/$number/status', body: jsonEncode({'status': status.name})));
  }

  @override
  Future<List<ProgressEntry>> loadProgress() async =>
      [for (final m in await _list('/api/progress')) ProgressEntry.fromJson(m)];

  @override
  Future<String?> loadUsage() async {
    final reply = await transport.send('GET', '/api/usage');
    return reply.status == 404 ? null : _ok(reply);
  }

  Future<List<Map<String, dynamic>>> _list(String path) async {
    final data = _decode(_ok(await transport.send('GET', path)));
    if (data is! List) throw const IssueTrackerException('unexpected answer');
    return [for (final m in data) m as Map<String, dynamic>];
  }

  Object? _decode(String text) {
    try {
      return jsonDecode(text);
    } on FormatException {
      throw const IssueTrackerException('unexpected answer');
    }
  }

  /// The body of a good answer; a 409 is a refused status change, any other error is an [IssueTrackerException].
  String _ok(HttpReply reply) {
    if (reply.ok) return reply.body;
    var reason = 'server answered ${reply.status}';
    try {
      final data = jsonDecode(reply.body);
      if (data is Map && data['error'] != null) reason = '${data['error']}';
    } on FormatException {
      // keep the status reason
    }
    if (reply.status == 409) throw StatusRefused(reason);
    throw IssueTrackerException(reason);
  }
}
