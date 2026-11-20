// Tests the web app's data side over a fake transport: DSH-01.e (same data interface, same rows as the desktop files),
// DSH-02.d (first save creates the file), DSH-10.e (unreachable server is said, with the reason), DSH-10.d (the
// server's reason reaches the caller), DSH-01.a (no token or secret in the server and web sources).
// One run covers each ID named in the test name.
import 'dart:convert';
import 'dart:io';

import 'package:dashboard/features/dashboard/data/http_file_access.dart';
import 'package:dashboard/features/dashboard/data/http_issue_tracker.dart';
import 'package:dashboard/features/dashboard/data/http_reply.dart';
import 'package:dashboard/features/dashboard/data/issue_partial_failure.dart';
import 'package:dashboard/features/dashboard/data/issue_service.dart';
import 'package:dashboard/features/dashboard/data/issue_tracker_exception.dart';
import 'package:dashboard/features/dashboard/data/requirement_repository.dart';
import 'package:dashboard/features/dashboard/data/server_unreachable_exception.dart';
import 'package:dashboard/features/dashboard/data/sprint_repository.dart';
import 'package:dashboard/features/dashboard/domain/issue.dart';
import 'package:dashboard/features/dashboard/domain/new_issue.dart';
import 'package:dashboard/features/dashboard/domain/sprint.dart';
import 'package:dashboard/features/dashboard/ui/dashboard_page.dart';
import 'package:flutter_test/flutter_test.dart';

import '../support/fixtures.dart';
import '../support/http_client.dart';
import '../support/page_harness.dart';

HttpReply ok(String body) => HttpReply(200, body);

/// A fake server holding a sprint file and the requirement files (relative to requirements/), like DSH-10.b.
FakeTransport fakeServer({String? sprint, Map<String, String>? reqs}) {
  var sprintText = sprint;
  final r = reqs ??
      {
        for (final e in requirementFiles().entries)
          if (!{'README.md', 'oldkey.md', 'open-questions.md'}.contains(e.key.substring('requirements/'.length)) &&
              !e.key.endsWith('/README.md'))
            e.key.substring('requirements/'.length): e.value,
      };
  return FakeTransport((method, path, body) async {
    if (path == '/api/sprint' && method == 'GET') return sprintText == null ? const HttpReply(404, '') : ok(sprintText!);
    if (path == '/api/sprint' && method == 'PUT') {
      sprintText = body;
      return ok('');
    }
    if (path == '/api/requirements') return ok(jsonEncode(r));
    return const HttpReply(404, '');
  });
}

void main() {
  group('HttpFileAccess (DSH-01.e)', () {
    test('DSH-01.e: read of the sprint file is GET /api/sprint; a 404 is null', () async {
      final t = fakeServer();
      expect(await HttpFileAccess(t).read('SCRUM.d/sprint.md'), isNull);
      expect(t.calls, ['GET /api/sprint']);
    });
    test('DSH-01.e: write is PUT /api/sprint with the whole text', () async {
      final t = fakeServer();
      await HttpFileAccess(t).write('SCRUM.d/sprint.md', 'text');
      expect(t.calls, ['PUT /api/sprint']);
      expect(t.bodies.single, 'text');
    });
    test('DSH-01.e: requirement listing and reads come from one cached GET /api/requirements', () async {
      final t = fakeServer();
      final f = HttpFileAccess(t);
      expect(await f.listFiles('requirements'), contains('requirements/alpha.md'));
      expect(await f.listDirectories('requirements'), containsAll(['requirements/connections.d', 'requirements/plugins.d']));
      expect(await f.read('requirements/alpha.md'), contains('AAA-01'));
      expect(await f.read('requirements/connections.d/beta.md'), contains('BBB-01'));
      expect(t.calls.where((c) => c == 'GET /api/requirements'), hasLength(1));
    });
    test('DSH-01.e and DSH-10.d: a non-2xx answer throws', () async {
      final t = FakeTransport((m, p, b) async => const HttpReply(500, 'x'));
      await expectLater(HttpFileAccess(t).read('SCRUM.d/sprint.md'), throwsA(anything));
      await expectLater(HttpFileAccess(t).write('SCRUM.d/sprint.md', 'a'), throwsA(anything));
      await expectLater(HttpFileAccess(t).listFiles('requirements'), throwsA(anything));
    });
  });

  group('same rows over files and over the server (DSH-01.e)', () {
    test('DSH-01.e: RequirementRepository over HttpFileAccess loads the same rows as over a temp directory', () async {
      final repo = makeRepo();
      addTearDown(() => repo.deleteSync(recursive: true));
      final fromDisk = await RequirementRepository(files: disk, directory: makeRequirements(repo)).load();
      final fromHttp = await RequirementRepository(files: HttpFileAccess(fakeServer()), directory: 'requirements').load();
      String key(r) => '${r.id}|${r.status}|${r.statement}|${r.feature}';
      expect(fromHttp.map(key).toList()..sort(), fromDisk.map(key).toList()..sort());
      expect(fromHttp, isNotEmpty);
    });
    test('DSH-01.e: SprintRepository over HttpFileAccess loads the same sprint as over a temp directory', () async {
      final repo = makeRepo();
      addTearDown(() => repo.deleteSync(recursive: true));
      writeFile(repo, 'SCRUM.d/sprint.md', sampleSprintFile);
      final a = await SprintRepository(files: disk, path: join(repo, 'SCRUM.d/sprint.md')).load();
      final b = await SprintRepository(files: HttpFileAccess(fakeServer(sprint: sampleSprintFile)), path: 'SCRUM.d/sprint.md').load();
      expect(b.goal, a.goal);
      expect(b.stories.map((s) => s.id), a.stories.map((s) => s.id));
      expect(b.review, a.review);
      expect(b.retrospective, a.retrospective);
    });
    test('DSH-02.d: over the server a missing sprint file is empty and the first save creates it', () async {
      final t = fakeServer();
      final r = SprintRepository(files: HttpFileAccess(t), path: 'SCRUM.d/sprint.md');
      expect((await r.load()).stories, isEmpty);
      await r.save(const Sprint(goal: 'G'));
      expect(t.calls, contains('PUT /api/sprint'));
      expect((await r.load()).goal, 'G');
    });
  });

  group('HttpIssueTracker (DSH-01.e, DSH-10.d)', () {
    final listJson = issuesJson([issueJson(1, 'One', assignee: 'ann'), issueJson(2, 'Two', state: 'CLOSED')]);

    test('DSH-01.e: load is GET /api/issues and parses like IssueService.parse', () async {
      final t = FakeTransport((m, p, b) async => ok(listJson));
      final got = await HttpIssueTracker(t).load();
      expect(t.calls, ['GET /api/issues']);
      final want = IssueService.parse(listJson);
      expect(got.map((i) => '${i.number}|${i.title}|${i.status}|${i.assignee}'),
          want.map((i) => '${i.number}|${i.title}|${i.status}|${i.assignee}'));
      expect(got[1].status, IssueStatus.closed);
    });
    test('DSH-01.e: create posts title, body and labels and returns the number; an open issue is not closed', () async {
      final t = FakeTransport((m, p, b) async => ok('{"number": 31}'));
      final n = await HttpIssueTracker(t).create(NewIssue(title: 'T; x', description: 'D', feature: 'alpha', requirement: 'AAA-01'));
      expect(n, 31);
      expect(t.calls, ['POST /api/issues']);
      final sent = jsonDecode(t.bodies.single!) as Map;
      expect(sent['title'], 'T; x');
      expect(sent['body'], 'D\n\nRequirement: AAA-01');
      expect(sent['labels'], contains('feature:alpha'));
    });
    test('DSH-01.e: a closed issue is created, then closed with POST /api/issues/N/close', () async {
      final t = FakeTransport((m, p, b) async => ok('{"number": 31}'));
      await HttpIssueTracker(t).create(NewIssue(title: 'T', closed: true));
      expect(t.calls, ['POST /api/issues', 'POST /api/issues/31/close']);
    });
    test('DSH-10.d: a failing close after create throws IssuePartialFailure with the number and the reason', () async {
      final t = FakeTransport((m, p, b) async =>
          p.endsWith('/close') ? const HttpReply(502, '{"error":"denied"}') : ok('{"number": 31}'));
      await expectLater(
          HttpIssueTracker(t).create(NewIssue(title: 'T', closed: true)),
          throwsA(isA<IssuePartialFailure>().having((e) => e.number, 'number', 31).having((e) => e.reason, 'reason', 'denied')));
      expect(t.calls.where((c) => c == 'POST /api/issues'), hasLength(1));
    });
    test('DSH-10.d: a non-2xx answer throws IssueTrackerException with the server error, else "server answered N"', () async {
      final bad = HttpIssueTracker(FakeTransport((m, p, b) async => const HttpReply(502, '{"error":"not signed in"}')));
      await expectLater(bad.load(), throwsA(isA<IssueTrackerException>().having((e) => e.reason, 'reason', 'not signed in')));
      final plain = HttpIssueTracker(FakeTransport((m, p, b) async => const HttpReply(500, 'oops')));
      await expectLater(plain.load(), throwsA(isA<IssueTrackerException>().having((e) => e.reason, 'reason', 'server answered 500')));
      await expectLater(plain.close(3), throwsA(isA<IssueTrackerException>()));
    });
    test('DSH-10.e: ServerUnreachableException is an IssueTrackerException carrying the reason', () {
      const e = ServerUnreachableException('refused');
      expect(e, isA<IssueTrackerException>());
      expect(e.reason, 'refused');
    });
  });

  group('DSH-10.e: the page says the server cannot be reached', () {
    testWidgets('DSH-10.e: every list shows msg:dshServerUnreachable with the reason when the transport cannot reach the server', (t) async {
      final transport = FakeTransport((m, p, b) async => throw const ServerUnreachableException('connection refused'));
      bigView(t);
      await t.pumpWidget(testApp(DashboardPage(
        sprints: SprintRepository(files: HttpFileAccess(transport), path: 'SCRUM.d/sprint.md'),
        requirements: RequirementRepository(files: HttpFileAccess(transport), directory: 'requirements'),
        issues: HttpIssueTracker(transport),
      )));
      await t.pumpAndSettle();
      expect(find.textContaining('The dashboard server could not be reached: connection refused'), findsWidgets);
      expect(find.textContaining('The dashboard server could not be reached: connection refused').evaluate().length, greaterThanOrEqualTo(2));
    });
  });

  group('DSH-01.a: no token or secret in the server and web sources', () {
    final lib = Directory('../../SCRUM.d/dashboard/lib/features/dashboard');
    List<File> sources() => [
          ...Directory('${lib.path}/server').listSync().whereType<File>(),
          ...Directory('${lib.path}/data')
              .listSync()
              .whereType<File>()
              .where((f) => RegExp(r'[\\/](http_|js_http_|platform_backend|dashboard_backend)[^\\/]*$').hasMatch(f.path)),
        ];

    test('DSH-01.a: the scan finds the server and web sources', () {
      final names = sources().map((f) => f.path.replaceAll('\\', '/')).toList();
      expect(names.any((n) => n.endsWith('server/dashboard_server.dart')), isTrue);
      expect(names.any((n) => n.endsWith('data/http_issue_tracker.dart')), isTrue);
    });
    test('DSH-01.a and DSH-10.c: no server or web source names a token, secret, Authorization, GH_TOKEN or GITHUB_TOKEN', () {
      for (final f in sources()) {
        final text = f.readAsLinesSync().where((l) => !l.trimLeft().startsWith("//")).join(' '); // code only: a comment may say "no token"
        for (final w in ['token', 'secret', 'authorization', 'gh_token', 'github_token']) {
          expect(text.toLowerCase(), isNot(contains(w)), reason: '${f.path} names $w');
        }
      }
    });
    test('DSH-01.a: no source in lib names GH_TOKEN, GITHUB_TOKEN or an Authorization header', () {
      for (final f in lib.parent.parent.parent.listSync(recursive: true).whereType<File>().where((f) => f.path.endsWith('.dart'))) {
        final text = f.readAsStringSync();
        for (final w in ['GH_TOKEN', 'GITHUB_TOKEN', 'Authorization']) {
          expect(text, isNot(contains(w)), reason: '${f.path} names $w');
        }
      }
    });
  });
}
