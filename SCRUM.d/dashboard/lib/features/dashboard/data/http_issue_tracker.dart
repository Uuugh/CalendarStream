// Holds: IssueTracker through the server (DSH-01.e, DSH-10.b, DSH-10.d). Depends on: HttpTransport, IssueService
// (its parsing and labels), IssueTracker, IssueTrackerException. Used by: the web backend. Reads or writes: network, through the transport.

import 'dart:convert';

import '../domain/issue.dart';
import '../domain/new_issue.dart';
import 'http_transport.dart';
import 'issue_service.dart';
import 'issue_tracker.dart';
import 'issue_tracker_exception.dart';

/// Web [IssueTracker]; a server answer that carries `error` becomes an [IssueTrackerException] with that reason.
class HttpIssueTracker extends IssueTracker {
  const HttpIssueTracker(this.transport);

  final HttpTransport transport;

  @override
  Future<List<Issue>> load() async {
    final text = await _send('GET', '/api/issues');
    try {
      return IssueService.parse(text);
    } on FormatException catch (e) {
      throw IssueTrackerException(e.message);
    }
  }

  @override
  Future<int> createOpen(NewIssue issue) async {
    final text = await _send('POST', '/api/issues',
        body: jsonEncode({'title': issue.title, 'body': issue.body, 'labels': IssueService.labelsFor(issue)}));
    final number = (jsonDecode(text) as Map<String, dynamic>)['number'];
    if (number is! int) throw const IssueTrackerException('no issue number');
    return number;
  }

  @override
  Future<void> close(int number) async {
    await _send('POST', '/api/issues/$number/close');
  }

  Future<String> _send(String method, String path, {String? body}) async {
    final reply = await transport.send(method, path, body: body);
    if (reply.ok) return reply.body;
    var reason = 'server answered ${reply.status}';
    try {
      final data = jsonDecode(reply.body);
      if (data is Map && data['error'] != null) reason = '${data['error']}';
    } on FormatException {
      // keep the status reason
    }
    throw IssueTrackerException(reason);
  }
}
