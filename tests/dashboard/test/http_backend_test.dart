// Tests the web app's data side: HttpBackend over a fake transport (DSH-01.e the requests it makes, DSH-13.c a refusal
// comes back as StatusRefused, DSH-13.g the server's reason, DSH-13.h an unreachable server) and, over a real server on
// 127.0.0.1, that it gives the same answers as LocalBackend (DSH-01.e). One run covers each ID named in the test name.
import 'dart:convert';
import 'dart:io';

import 'package:dashboard/features/dashboard/data/command_result.dart';
import 'package:dashboard/features/dashboard/data/http_backend.dart';
import 'package:dashboard/features/dashboard/data/http_reply.dart';
import 'package:dashboard/features/dashboard/data/issue_tracker_exception.dart';
import 'package:dashboard/features/dashboard/data/local_backend.dart';
import 'package:dashboard/features/dashboard/data/server_unreachable_exception.dart';
import 'package:dashboard/features/dashboard/data/sprint_repository.dart';
import 'package:dashboard/features/dashboard/domain/new_issue.dart';
import 'package:dashboard/features/dashboard/domain/requirement.dart';
import 'package:dashboard/features/dashboard/domain/sprint_edit.dart';
import 'package:dashboard/features/dashboard/domain/status.dart';
import 'package:dashboard/features/dashboard/domain/status_refused.dart';
import 'package:dashboard/features/dashboard/server/dashboard_server.dart';
import 'package:flutter_test/flutter_test.dart';

import '../support/fixtures.dart';
import '../support/http_client.dart';

HttpReply ok(String body) => HttpReply(200, body);

void main() {
  group('requests over a fake transport (DSH-01.e)', () {
    test('DSH-01.e: loadSprint is GET /api/sprint and parses the text', () async {
      final t = FakeTransport((m, p, b) async => ok(sampleSprintFile));
      final s = await HttpBackend(t).loadSprint();
      expect(t.calls, ['GET /api/sprint']);
      expect(s.blocks, hasLength(4));
    });

    test('DSH-01.e: saveSprint is PUT /api/sprint with the whole file text', () async {
      final t = FakeTransport((m, p, b) async => ok(''));
      final s = SprintRepository.parse(sampleSprintFile);
      await HttpBackend(t).saveSprint(s);
      expect(t.calls, ['PUT /api/sprint']);
      expect(t.bodies.single, SprintRepository.format(s));
    });

    test('DSH-01.e: loadRequirements, loadIssues and loadProgress are GETs that parse the lists', () async {
      final t = FakeTransport((m, p, b) async => switch (p) {
            '/api/requirements' => ok(jsonEncode([{'id': 'AAA-01', 'status': 'planned', 'statement': 's', 'feature': 'alpha'}])),
            '/api/issues' => ok(jsonEncode([{'number': 3, 'title': 'T', 'status': 'done', 'feature': null, 'requirement': null, 'assignee': ''}])),
            '/api/progress' => ok(jsonEncode([{'label': 'a', 'done': 1, 'total': 2}])),
            _ => const HttpReply(404, ''),
          });
      final b = HttpBackend(t);
      expect((await b.loadRequirements()).single.status, Status.planned);
      expect((await b.loadIssues()).single.status, Status.done);
      expect((await b.loadProgress()).single.text, '1/2');
      expect(t.calls, ['GET /api/requirements', 'GET /api/issues', 'GET /api/progress']);
    });

    test('DSH-01.e: the status changes and the issue creation are the routes of DSH-13.b with a JSON body', () async {
      final t = FakeTransport((m, p, b) async => ok(p == '/api/issues' ? '{"number": 31}' : '{}'));
      final b = HttpBackend(t);
      await b.setRequirementStatus('AAA-01.a', Status.planned);
      await b.setIssueStatus(4, Status.done);
      final n = await b.createIssue(const NewIssue(title: 'T', description: 'D', feature: 'f', requirement: 'AAA-01', status: Status.proposed));
      expect(n, 31);
      expect(t.calls, ['PUT /api/requirements/AAA-01.a/status', 'POST /api/issues/4/status', 'POST /api/issues']);
      expect(jsonDecode(t.bodies[0]!), {'status': 'planned'});
      expect(jsonDecode(t.bodies[1]!), {'status': 'done'});
      expect(jsonDecode(t.bodies[2]!), {'title': 'T', 'description': 'D', 'feature': 'f', 'requirement': 'AAA-01', 'status': 'proposed'});
    });

    test('DSH-01.e: the usage file is GET /api/usage, and a 404 is no file', () async {
      expect(await HttpBackend(FakeTransport((m, p, b) async => const HttpReply(404, ''))).loadUsage(), isNull);
      expect(await HttpBackend(FakeTransport((m, p, b) async => ok('text'))).loadUsage(), 'text');
    });
  });

  group('refusals and failures (DSH-13.c, DSH-13.g, DSH-13.h)', () {
    test('DSH-13.c and DSH-07.g: a 409 is a StatusRefused with the server reason', () async {
      final b = HttpBackend(FakeTransport((m, p, b) async => const HttpReply(409, '{"error":"a status cannot move from done to planned"}')));
      await expectLater(b.setRequirementStatus('AAA-01', Status.planned),
          throwsA(isA<StatusRefused>().having((e) => e.reason, 'reason', 'a status cannot move from done to planned')));
      await expectLater(b.setIssueStatus(1, Status.planned), throwsA(isA<StatusRefused>()));
    });

    test('DSH-13.g: another non-2xx answer is an IssueTrackerException with the error, else "server answered N"', () async {
      final bad = HttpBackend(FakeTransport((m, p, b) async => const HttpReply(502, '{"error":"not signed in"}')));
      await expectLater(bad.loadIssues(), throwsA(isA<IssueTrackerException>().having((e) => e.reason, 'reason', 'not signed in')));
      final plain = HttpBackend(FakeTransport((m, p, b) async => const HttpReply(500, 'oops')));
      await expectLater(plain.loadIssues(), throwsA(isA<IssueTrackerException>().having((e) => e.reason, 'reason', 'server answered 500')));
      await expectLater(plain.createIssue(const NewIssue(title: 'T')), throwsA(isA<IssueTrackerException>()));
      await expectLater(plain.loadSprint(), throwsA(isA<IssueTrackerException>()));
    });

    test('DSH-13.g: an answer that is not the expected JSON is an IssueTrackerException', () async {
      final b = HttpBackend(FakeTransport((m, p, b) async => ok('not json')));
      await expectLater(b.loadRequirements(), throwsA(isA<IssueTrackerException>()));
      await expectLater(b.createIssue(const NewIssue(title: 'T')), throwsA(isA<IssueTrackerException>()));
    });

    test('DSH-13.h: a transport that cannot reach the server throws ServerUnreachableException with the reason', () async {
      final b = HttpBackend(FakeTransport((m, p, b) async => throw const ServerUnreachableException('connection refused')));
      await expectLater(b.loadSprint(), throwsA(isA<ServerUnreachableException>().having((e) => e.reason, 'reason', 'connection refused')));
      await expectLater(b.loadIssues(), throwsA(isA<ServerUnreachableException>()));
    });

    test('DSH-13.h: ServerUnreachableException is an IssueTrackerException carrying the reason', () {
      const e = ServerUnreachableException('refused');
      expect(e, isA<IssueTrackerException>());
      expect(e.reason, 'refused');
    });

    test('DSH-13.h: nothing listens on the port, so the real transport reports the server unreachable', () async {
      final probe = await ServerSocket.bind('127.0.0.1', 0);
      final port = probe.port;
      await probe.close();
      await expectLater(ServerTransport(port).send('GET', '/api/sprint'), throwsA(isA<SocketException>()));
    });
  });

  group('the web app and the desktop app give the same answers (DSH-01.e)', () {
    late Directory repo;
    late Directory web;
    late Directory progress;
    late FakeRunner runner;
    late DashboardServer server;
    late LocalBackend local;
    late HttpBackend remote;

    setUp(() async {
      repo = makeRepo();
      web = Directory(join(repo, 'web'))..createSync();
      progress = Directory(join(repo, 'progress'))..createSync();
      File('${progress.path}/a.progress').writeAsStringSync('2/5');
      File('${progress.path}/bad.progress').writeAsStringSync('no');
      makeRequirements(repo);
      writeFile(repo, 'SCRUM.d/sprint.md', sampleSprintFile);
      writeFile(repo, 'SCRUM.d/usage.md', '## Usage\n\n| block |\n|---|\n| sprint-1 |\n');
      runner = FakeRunner(const CommandResult(exitCode: 0), handler: (a) {
        if (a[1] == 'list') return CommandResult(exitCode: 0, stdout: issuesJson([issueJson(1, 'One', feature: 'alpha', requirement: 'AAA-01', labels: ['planned'])]));
        if (a[1] == 'view') return viewResult(['planned']);
        if (a[1] == 'create' && a[0] == 'issue') return createdIssue12;
        return const CommandResult(exitCode: 0);
      });
      server = DashboardServer(repo: repo.path, runner: runner, webRoot: web.path, port: 0, progressDir: progress.path);
      await server.start();
      remote = HttpBackend(ServerTransport(server.port));
      local = LocalBackend(files: disk, runner: runner, repoRoot: repo.path, progressDir: progress.path);
    });
    tearDown(() async {
      await server.close();
      repo.deleteSync(recursive: true);
    });

    test('DSH-01.e: reading gives the same sprint, requirements, issues, progress and usage', () async {
      expect(SprintRepository.format(await remote.loadSprint()), SprintRepository.format(await local.loadSprint()));
      String req(Requirement r) => '${r.id}|${r.status.name}|${r.statement}|${r.feature}';
      expect((await remote.loadRequirements()).map(req).toList(), (await local.loadRequirements()).map(req).toList());
      expect((await remote.loadIssues()).map((i) => i.toJson()).toList(), (await local.loadIssues()).map((i) => i.toJson()).toList());
      expect((await remote.loadProgress()).map((p) => p.toJson()).toList(), (await local.loadProgress()).map((p) => p.toJson()).toList());
      expect(await remote.loadUsage(), await local.loadUsage());
      expect(await remote.loadUsage(), isNotNull);
    });

    test('DSH-01.e: writing through the web app changes the same files as through the desktop app', () async {
      await remote.saveSprint(SprintEdit.setUsage(await remote.loadSprint(), 'story-1', 2));
      expect((await local.loadSprint()).block('story-1')!.usage, 2);
      await remote.setRequirementStatus('AAA-01', Status.planned);
      expect((await local.loadRequirements()).firstWhere((r) => r.id == 'AAA-01').status, Status.planned);
      expect(await remote.createIssue(const NewIssue(title: 'T')), await local.createIssue(const NewIssue(title: 'T')));
    });

    test('DSH-01.e and DSH-13.c: a refused move is a StatusRefused through both, with the same reason', () async {
      await local.setRequirementStatus('AAA-04', Status.done);
      Object? viaLocal;
      Object? viaRemote;
      try {
        await local.setRequirementStatus('AAA-04', Status.planned);
      } on StatusRefused catch (e) {
        viaLocal = e.reason;
      }
      try {
        await remote.setRequirementStatus('AAA-04', Status.planned);
      } on StatusRefused catch (e) {
        viaRemote = e.reason;
      }
      expect(viaLocal, isNotNull);
      expect(viaRemote, viaLocal);
    });

    test('DSH-01.e and DSH-13.g: a tracker failure is an IssueTrackerException with the same reason through both', () async {
      runner = FakeRunner(const CommandResult(exitCode: 1, stderr: 'not signed in'));
      await server.close();
      server = DashboardServer(repo: repo.path, runner: runner, webRoot: web.path, port: 0);
      await server.start();
      remote = HttpBackend(ServerTransport(server.port));
      local = LocalBackend(files: disk, runner: runner, repoRoot: repo.path);
      await expectLater(local.loadIssues(), throwsA(isA<IssueTrackerException>().having((e) => e.reason, 'reason', 'not signed in')));
      await expectLater(remote.loadIssues(), throwsA(isA<IssueTrackerException>().having((e) => e.reason, 'reason', 'not signed in')));
      expect((await remote.loadRequirements()), isNotEmpty);
    });
  });
}
