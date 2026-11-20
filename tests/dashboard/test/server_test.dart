// Tests the server (DSH-13) over real HTTP on 127.0.0.1 port 0, with a fake command runner and a temp repository:
// DSH-13.a (local only, Host and Origin), DSH-13.b (only these requests), DSH-13.c (status rule, 409), DSH-13.d (one row),
// DSH-13.e (issue labels), DSH-13.f (separate arguments, no token), DSH-13.g (failure reason, other answers keep working),
// DSH-01.a (what it changes), DSH-02.e (first write creates the file), DSH-12 and DSH-14.g (progress, usage).
// One run covers each ID named in the test name.
import 'dart:convert';
import 'dart:io';

import 'package:dashboard/features/dashboard/data/command_result.dart';
import 'package:dashboard/features/dashboard/data/command_runner.dart';
import 'package:dashboard/features/dashboard/data/sprint_repository.dart';
import 'package:dashboard/features/dashboard/domain/status.dart';
import 'package:dashboard/features/dashboard/server/dashboard_server.dart';
import 'package:flutter_test/flutter_test.dart';

import '../support/fixtures.dart';
import '../support/http_client.dart';

class ThrowingRunner implements CommandRunner {
  @override
  Future<CommandResult> run(String executable, List<String> arguments) => throw Exception('no such program');
}

void main() {
  late Directory repo;
  late Directory web;
  late Directory progress;
  late FakeRunner runner;
  late DashboardServer server;
  late int port;
  var tracker = <int, List<String>>{};

  Future<void> boot(CommandRunner r) async {
    server = DashboardServer(repo: repo.path, runner: r, webRoot: web.path, port: 0, progressDir: progress.path);
    await server.start();
    port = server.port;
  }

  String reqText(String rel) => File(join(repo, 'requirements/$rel')).readAsStringSync();

  setUp(() async {
    repo = makeRepo();
    web = Directory(join(repo, 'web'))..createSync();
    progress = Directory(join(repo, 'progress'))..createSync();
    File(join(web, 'index.html')).writeAsStringSync('<html>home</html>');
    File(join(web, 'app.js')).writeAsStringSync('var a=1;');
    File(join(repo, 'secret.txt')).writeAsStringSync('SECRET');
    makeRequirements(repo);
    tracker = {5: ['issue', 'backlog'], 8: ['issue', 'done']};
    runner = FakeRunner(const CommandResult(exitCode: 0, stdout: '[]'), handler: (a) {
      if (a[0] == 'issue' && a[1] == 'view') return viewResult(tracker[int.parse(a[2])] ?? []);
      if (a[0] == 'issue' && a[1] == 'create') return createdIssue12;
      if (a[0] == 'label') return const CommandResult(exitCode: 0);
      if (a[0] == 'issue' && a[1] == 'edit') return const CommandResult(exitCode: 0);
      return runner.result;
    });
    await boot(runner);
  });
  tearDown(() async {
    await server.close();
    repo.deleteSync(recursive: true);
  });

  group('DSH-13.a: local only', () {
    test('DSH-13.a: the server answers on 127.0.0.1, and is on the port it was given (port 0 is any free port)', () async {
      expect((await ask(port, 'GET', '/')).status, 200);
      expect(port, greaterThan(0));
    });

    test('DSH-13.a: an API request whose Host is not 127.0.0.1 or localhost is answered 404 and runs nothing', () async {
      expect((await raw(port, 'GET', '/api/sprint', ['Host: evil.example:$port'])).status, 404);
      expect((await raw(port, 'GET', '/api/issues', ['Host: evil.example'])).status, 404);
      expect(runner.calls, isEmpty);
    });

    test('DSH-13.a: a static request whose Host is not 127.0.0.1 or localhost is answered 404', () async {
      expect((await raw(port, 'GET', '/', ['Host: evil.example'])).status, 404);
    });

    test('DSH-13.a: Host localhost is accepted', () async {
      expect((await ask(port, 'GET', '/', host: 'localhost:$port')).status, 200);
    });

    test('DSH-13.a: a request whose Origin does not match the Host is answered 404 and runs nothing', () async {
      expect((await raw(port, 'POST', '/api/issues/5/status', ['Host: 127.0.0.1:$port', 'Origin: http://evil.example'])).status, 404);
      expect((await raw(port, 'GET', '/api/issues', ['Host: 127.0.0.1:$port', 'Origin: http://evil.example'])).status, 404);
      expect((await raw(port, 'PUT', '/api/requirements/AAA-01/status', ['Host: 127.0.0.1:$port', 'Origin: http://127.0.0.1:1'])).status, 404);
      expect(runner.calls, isEmpty);
      expect(reqText('alpha.md'), contains('| AAA-01 | proposed |'));
    });

    test('DSH-13.a: a static request whose Origin does not match the Host is answered 404; a matching Origin is accepted', () async {
      expect((await raw(port, 'GET', '/', ['Host: 127.0.0.1:$port', 'Origin: http://evil.example'])).status, 404);
      expect((await raw(port, 'GET', '/', ['Host: 127.0.0.1:$port', 'Origin: http://127.0.0.1:$port'])).status, 200);
      expect((await raw(port, 'GET', '/api/usage', ['Host: 127.0.0.1:$port', 'Origin: http://127.0.0.1:$port'])).status, 404, reason: 'matching origin passes the check; the usage file is missing');
    });

    test('DSH-13.a: the listening socket is not reachable on a non-loopback address', () async {
      final others = (await NetworkInterface.list())
          .expand((i) => i.addresses)
          .where((a) => a.type == InternetAddressType.IPv4 && !a.isLoopback)
          .toList();
      if (others.isEmpty) {
        markTestSkipped('no non-loopback IPv4 address on this machine');
        return;
      }
      final client = HttpClient()..connectionTimeout = const Duration(seconds: 2);
      await expectLater(client.getUrl(Uri.parse('http://${others.first.address}:$port/')).then((r) => r.close()), throwsA(isA<SocketException>()));
      client.close(force: true);
    });
  });

  group('DSH-13.b: only these requests', () {
    test('DSH-13.b: GET /api/sprint returns the sprint file text; with no file it is an empty sprint (DSH-02.e)', () async {
      final empty = await ask(port, 'GET', '/api/sprint');
      expect(empty.status, 200);
      expect(SprintRepository.parse(empty.body).blocks, isEmpty);
      writeFile(repo, 'SCRUM.d/sprint.md', sampleSprintFile);
      final a = await ask(port, 'GET', '/api/sprint');
      expect(a.status, 200);
      expect(SprintRepository.parse(a.body).blocks.map((b) => b.id), ['sprint-1', 'epic-1', 'story-1', 'story-2']);
      expect(SprintRepository.parse(a.body).review, 'Looked fine.');
    });

    test('DSH-13.b and DSH-02.e: PUT /api/sprint writes the sprint and creates the file with its folder', () async {
      final path = join(repo, 'SCRUM.d/sprint.md');
      expect(File(path).existsSync(), isFalse);
      expect((await ask(port, 'PUT', '/api/sprint', body: sampleSprintFile)).status, 200);
      expect(File(path).existsSync(), isTrue);
      expect(SprintRepository.parse(File(path).readAsStringSync()).members.map((m) => m.item), ['AAA-01', 'AAA-03', '#7']);
      expect(SprintRepository.parse(File(path).readAsStringSync()).retrospective, 'Do more of X.');
    });

    test('DSH-13.b: GET /api/requirements lists the requirements of the feature files and .d parts, not the README, oldkey or open-questions', () async {
      final a = await ask(port, 'GET', '/api/requirements');
      expect(a.status, 200);
      final list = (a.json as List).cast<Map<String, dynamic>>();
      final ids = list.map((r) => r['id']).toList();
      expect(ids, containsAll(['AAA-01', 'BBB-01', 'GGG-01', 'DDD-01']));
      expect(ids, isNot(anyOf(contains('RDM-01'), contains('OLD-01'), contains('OQ-01'), contains('CRD-01'))));
      final b = list.firstWhere((r) => r['id'] == 'BBB-01');
      expect(b, {'id': 'BBB-01', 'status': 'backlog', 'statement': 'Beta one.', 'feature': 'beta'});
    });

    test('DSH-13.b: PUT /api/requirements/<ID>/status sets the status, also for a sub-requirement ID', () async {
      final a = await ask(port, 'PUT', '/api/requirements/AAA-01/status', body: jsonEncode({'status': 'planned'}));
      expect(a.status, 200);
      expect(reqText('alpha.md'), contains('| AAA-01 | planned | Alpha one. | — | — |'));
      expect((await ask(port, 'PUT', '/api/requirements/AAA-05.a/status', body: jsonEncode({'status': 'planned'}))).status, 200);
      expect(reqText('alpha.md'), contains('| AAA-05.a | planned |'));
    });

    test('DSH-13.b: GET /api/issues runs the list command and answers the issues as JSON', () async {
      runner.result = CommandResult(exitCode: 0, stdout: issuesJson([issueJson(1, 'One', feature: 'alpha', requirement: 'AAA-01', labels: ['planned'])]));
      final a = await ask(port, 'GET', '/api/issues');
      expect(a.status, 200);
      expect(a.json, [
        {'number': 1, 'title': 'One', 'status': 'planned', 'feature': 'alpha', 'requirement': 'AAA-01', 'assignee': ''},
      ]);
      expect(runner.calls.single.sublist(0, 6), ['gh', 'issue', 'list', '--state', 'open', '--limit']);
    });

    test('DSH-13.b and DSH-09.d: POST /api/issues creates one issue and answers its number', () async {
      final a = await ask(port, 'POST', '/api/issues',
          body: jsonEncode({'title': 'T', 'description': 'D', 'feature': 'alpha', 'requirement': 'AAA-01', 'status': 'proposed'}));
      expect(a.status, 200);
      expect(a.json, {'number': 12});
      expect(runner.calls, [
        ['gh', 'label', 'create', 'proposed', '--force'],
        ['gh', 'issue', 'create', '--title', 'T', '--body', 'D\n\nRequirement: AAA-01', '--label', 'issue', '--label', 'feature:alpha', '--label', 'proposed'],
      ]);
    });

    test('DSH-13.b: POST /api/issues with no status makes a backlog issue; a bad body or status is 400 and runs nothing', () async {
      expect((await ask(port, 'POST', '/api/issues', body: jsonEncode({'title': 'T'}))).status, 200);
      expect(runner.calls.last.sublist(runner.calls.last.length - 2), ['--label', 'backlog']);
      runner.calls.clear();
      expect((await ask(port, 'POST', '/api/issues', body: 'not json')).status, 400);
      expect((await ask(port, 'POST', '/api/issues', body: '{"description":"x"}')).status, 400);
      expect((await ask(port, 'POST', '/api/issues', body: '{"title":" "}')).status, 400);
      expect((await ask(port, 'POST', '/api/issues', body: '{"title":"T","status":"closed"}')).status, 400);
      expect((await ask(port, 'POST', '/api/issues/5/status', body: '{"status":"nope"}')).status, 400);
      expect((await ask(port, 'PUT', '/api/requirements/AAA-01/status', body: '{}')).status, 400);
      expect(runner.calls, isEmpty);
    });

    test('DSH-13.b: POST /api/issues/<digits>/status changes the status labels and answers the number and status', () async {
      final a = await ask(port, 'POST', '/api/issues/5/status', body: jsonEncode({'status': 'planned'}));
      expect(a.status, 200);
      expect(a.json, {'number': 5, 'status': 'planned'});
      expect(runner.calls.last, ['gh', 'issue', 'edit', '5', '--add-label', 'planned', '--remove-label', 'backlog']);
    });

    test('DSH-13.b: GET /api/progress lists the progress files that hold done/total', () async {
      File('${progress.path}/agent-a.progress').writeAsStringSync('3/10');
      File('${progress.path}/bad.progress').writeAsStringSync('x');
      File('${progress.path}/notes.txt').writeAsStringSync('1/2');
      final a = await ask(port, 'GET', '/api/progress');
      expect(a.status, 200);
      expect(a.json, [{'label': 'agent-a', 'done': 3, 'total': 10}]);
    });

    test('DSH-13.b and DSH-14.g: GET /api/usage answers the file text, and 404 with an empty body when it is missing', () async {
      final none = await ask(port, 'GET', '/api/usage');
      expect([none.status, none.body], [404, '']);
      writeFile(repo, 'SCRUM.d/usage.md', '## Usage\n');
      final a = await ask(port, 'GET', '/api/usage');
      expect([a.status, a.body], [200, '## Usage\n']);
    });

    test('DSH-13.b: any other request is answered 404 and runs nothing', () async {
      final cases = <List<String>>[
        ['DELETE', '/api/sprint'], ['POST', '/api/sprint'], ['PATCH', '/api/sprint'], ['PUT', '/api/issues'], ['DELETE', '/api/issues'],
        ['GET', '/api/issues/42/status'], ['PUT', '/api/issues/42/status'], ['POST', '/api/issues/abc/status'], ['POST', '/api/issues/42'],
        ['POST', '/api/issues/42/close'], ['POST', '/api/requirements'], ['PUT', '/api/requirements'], ['GET', '/api/requirements/AAA-01/status'],
        ['POST', '/api/requirements/AAA-01/status'], ['PUT', '/api/requirements/aaa-01/status'], ['PUT', '/api/requirements/AAA-01/other'],
        ['PUT', '/api/requirements/../status'], ['POST', '/api/progress'], ['PUT', '/api/usage'], ['GET', '/api/nothing'], ['POST', '/'], ['PUT', '/index.html'],
      ];
      for (final c in cases) {
        expect((await ask(port, c[0], c[1], body: '{"status":"done","title":"x"}')).status, 404, reason: '${c[0]} ${c[1]}');
      }
      expect(runner.calls, isEmpty);
      expect(reqText('alpha.md'), contains('| AAA-01 | proposed |'));
    });

    test('DSH-13.b: static files are served from the web root; / is index.html; only GET and HEAD', () async {
      final root = await ask(port, 'GET', '/');
      expect(root.status, 200);
      expect(root.body, '<html>home</html>');
      expect((await ask(port, 'GET', '/app.js')).body, 'var a=1;');
      expect((await ask(port, 'HEAD', '/app.js')).status, 200);
      expect((await ask(port, 'GET', '/missing.js')).status, 404);
    });

    for (final p in ['/../secret.txt', '/%2e%2e/secret.txt', '/..%2fsecret.txt', '/%2e%2e%2fsecret.txt', '/..\\secret.txt', '/..%5csecret.txt', '/C:/Windows/win.ini', '/a:b']) {
      test('DSH-13.b: the static path $p is answered 404 and never serves a file outside the web root', () async {
        final a = await raw(port, 'GET', p, ['Host: 127.0.0.1:$port']);
        expect(a.body, isNot(contains('SECRET')), reason: 'served the file outside the web root');
        expect(a.status, 404, reason: 'body: ${a.body}');
      });
    }

    test('DSH-13.b: a symbolic link inside the web root that points outside it is not served', () async {
      try {
        Link(join(web, 'link.txt')).createSync(join(repo, 'secret.txt'));
      } on FileSystemException {
        markTestSkipped('this machine cannot create a symbolic link');
        return;
      }
      final a = await ask(port, 'GET', '/link.txt');
      expect(a.status, 404);
      expect(a.body, isNot(contains('SECRET')));
    });
  });

  group('DSH-13.c: every status change is checked', () {
    test('DSH-13.c: a requirement move down other than planned to backlog is 409 with the reason, and the file is as it was', () async {
      final before = reqText('alpha.md');
      for (final c in [['AAA-04', 'planned'], ['AAA-04', 'proposed'], ['AAA-03', 'proposed']]) {
        final a = await ask(port, 'PUT', '/api/requirements/${c[0]}/status', body: jsonEncode({'status': c[1]}));
        expect(a.status, 409, reason: '${c[0]} to ${c[1]}');
        expect((a.json as Map)['error'], isNotEmpty);
      }
      expect(reqText('alpha.md'), before);
    });

    test('DSH-13.c: planned to backlog is allowed, and every move up', () async {
      expect((await ask(port, 'PUT', '/api/requirements/AAA-03/status', body: jsonEncode({'status': 'backlog'}))).status, 200);
      expect((await ask(port, 'PUT', '/api/requirements/AAA-01/status', body: jsonEncode({'status': 'done'}))).status, 200);
      expect(reqText('alpha.md'), contains('| AAA-03 | backlog |'));
      expect(reqText('alpha.md'), contains('| AAA-01 | done |'));
    });

    test('DSH-13.c: a requirement that does not exist is 409', () async {
      expect((await ask(port, 'PUT', '/api/requirements/ZZZ-99/status', body: jsonEncode({'status': 'planned'}))).status, 409);
    });

    test('DSH-13.c: an issue move down other than planned to backlog is 409 with the reason and nothing is edited', () async {
      final a = await ask(port, 'POST', '/api/issues/8/status', body: jsonEncode({'status': 'planned'}));
      expect(a.status, 409);
      expect((a.json as Map)['error'], isNotEmpty);
      expect(runner.calls.where((c) => c[1] == 'edit' || c[0] == 'label'), isEmpty);
    });
  });

  group('DSH-13.d: one row is edited', () {
    test('DSH-13.d: a status change changes only that cell: every other file and line is as it was', () async {
      final others = {for (final e in requirementFiles().entries) e.key: e.value}..remove('requirements/alpha.md');
      final before = reqText('alpha.md');
      await ask(port, 'PUT', '/api/requirements/AAA-02/status', body: jsonEncode({'status': 'planned'}));
      expect(reqText('alpha.md'), before.replaceFirst('| AAA-02 |  | Alpha two blank. |', '| AAA-02 | planned | Alpha two blank. |'));
      for (final e in others.entries) {
        expect(File(join(repo, e.key)).readAsStringSync(), e.value, reason: e.key);
      }
    });

    test('DSH-13.d: a file with CRLF line endings keeps them', () async {
      await ask(port, 'PUT', '/api/requirements/DDD-01/status', body: jsonEncode({'status': 'planned'}));
      final text = File(join(repo, 'requirements/delta.md')).readAsStringSync();
      expect(text, contains('| DDD-01 | planned | Delta one. | — | — |\r\n'));
      expect(RegExp(r'(?<!\r)\n').hasMatch(text), isFalse);
    });

    test('DSH-13.d: no temporary file stays behind', () async {
      await ask(port, 'PUT', '/api/requirements/AAA-01/status', body: jsonEncode({'status': 'planned'}));
      expect(Directory(join(repo, 'requirements')).listSync(recursive: true).where((e) => e.path.endsWith('.tmp')), isEmpty);
    });
  });

  group('DSH-13.e: issue labels', () {
    test('DSH-13.e: the other status labels are removed, the new one is added and created, and the state is left alone', () async {
      tracker[5] = ['issue', 'proposed', 'backlog'];
      await ask(port, 'POST', '/api/issues/5/status', body: jsonEncode({'status': 'planned'}));
      expect(runner.calls, [
        ['gh', 'issue', 'view', '5', '--json', 'labels'],
        ['gh', 'label', 'create', 'planned', '--force'],
        ['gh', 'issue', 'edit', '5', '--add-label', 'planned', '--remove-label', 'proposed', '--remove-label', 'backlog'],
      ]);
      final text = runner.calls.expand((c) => c).join(' ');
      for (final w in ['close', 'reopen', '--state']) {
        expect(text, isNot(contains(w)));
      }
    });
  });

  group('DSH-13.f: arguments are passed separately, no shell, no token', () {
    test('DSH-13.f: request text with shell characters stays one argument each', () async {
      await ask(port, 'POST', '/api/issues',
          body: jsonEncode({'title': 'x; rm -rf', 'description': r'$(id) `id` | a && b', 'feature': 'l1; l2', 'status': 'backlog'}));
      expect(runner.calls.last, [
        'gh', 'issue', 'create', '--title', 'x; rm -rf', '--body', r'$(id) `id` | a && b', '--label', 'issue', '--label', 'feature:l1; l2', '--label', 'backlog',
      ]);
    });

    test('DSH-13.f and DSH-01.a: no command argument carries a token, secret or authorization', () async {
      await ask(port, 'POST', '/api/issues', body: jsonEncode({'title': 'T'}));
      await ask(port, 'POST', '/api/issues/5/status', body: jsonEncode({'status': 'done'}));
      await ask(port, 'GET', '/api/issues');
      final text = runner.calls.expand((c) => c).join(' ').toLowerCase();
      for (final w in ['token', 'authorization', 'secret']) {
        expect(text, isNot(contains(w)));
      }
      for (final c in runner.calls) {
        expect(c.first, 'gh');
      }
    });
  });

  group('DSH-13.g: tracker failure', () {
    test('DSH-13.g: a non-zero exit on list answers 502 with the trimmed stderr as the reason', () async {
      runner.result = const CommandResult(exitCode: 1, stderr: ' not signed in \n');
      await server.close();
      await boot(FakeRunner(runner.result));
      final a = await ask(port, 'GET', '/api/issues');
      expect(a.status, 502);
      expect(a.json, {'error': 'not signed in'});
    });

    test('DSH-13.g: a failing create or status change answers 502 with the error', () async {
      await server.close();
      await boot(FakeRunner(const CommandResult(exitCode: 1, stderr: 'denied')));
      final c = await ask(port, 'POST', '/api/issues', body: jsonEncode({'title': 'T'}));
      expect([c.status, c.json], [502, {'error': 'denied'}]);
      final x = await ask(port, 'POST', '/api/issues/5/status', body: jsonEncode({'status': 'done'}));
      expect([x.status, x.json], [502, {'error': 'denied'}]);
    });

    test('DSH-13.g: a throwing runner answers 502 and the sprint, requirement, progress and usage answers keep working', () async {
      await server.close();
      await boot(ThrowingRunner());
      final a = await ask(port, 'GET', '/api/issues');
      expect(a.status, 502);
      expect((a.json as Map)['error'], isNotEmpty);
      writeFile(repo, 'SCRUM.d/sprint.md', sampleSprintFile);
      expect((await ask(port, 'GET', '/api/sprint')).status, 200);
      expect((await ask(port, 'GET', '/api/requirements')).status, 200);
      expect((await ask(port, 'GET', '/api/progress')).status, 200);
      expect((await ask(port, 'GET', '/api/usage')).status, 404);
      expect((await ask(port, 'PUT', '/api/sprint', body: sampleSprintFile)).status, 200);
      expect((await ask(port, 'PUT', '/api/requirements/AAA-01/status', body: jsonEncode({'status': 'planned'}))).status, 200);
    });
  });

  group('DSH-01.a: what the dashboard changes', () {
    test('DSH-01.a: a session of changes touches only the sprint file and one requirement file', () async {
      final tree = () => {
            for (final e in repo.listSync(recursive: true).whereType<File>()) e.path.replaceAll('\\', '/'): e.readAsStringSync(),
          };
      final before = tree();
      await ask(port, 'PUT', '/api/sprint', body: sampleSprintFile);
      await ask(port, 'PUT', '/api/requirements/BBB-01/status', body: jsonEncode({'status': 'planned'}));
      await ask(port, 'GET', '/api/progress');
      final after = tree();
      final changed = {
        for (final k in {...before.keys, ...after.keys})
          if (before[k] != after[k]) k.substring(repo.path.replaceAll('\\', '/').length + 1),
      };
      expect(changed, {'SCRUM.d/sprint.md', 'requirements/connections.d/beta.md'});
    });
  });

  test('DSH-13.c: the status order the server enforces is proposed, backlog, planned, done', () {
    expect(Status.values.map((s) => s.name), ['proposed', 'backlog', 'planned', 'done']);
  });
}
