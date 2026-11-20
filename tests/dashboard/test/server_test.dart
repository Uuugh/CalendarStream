// Tests the server (DSH-10) over real HTTP on 127.0.0.1 port 0, with a fake command runner and a temp repository:
// DSH-10.a (local only), DSH-10.b (only these requests), DSH-10.c (separate arguments, no token), DSH-10.d (failure
// reason, other answers keep working), DSH-01.a (no token, only sprint and requirement files), DSH-02.d (first write
// creates the file). One run covers each ID named in the test name.
import 'dart:convert';
import 'dart:io';

import 'package:dashboard/features/dashboard/data/command_result.dart';
import 'package:dashboard/features/dashboard/data/command_runner.dart';
import 'package:dashboard/features/dashboard/data/issue_service.dart';
import 'package:dashboard/features/dashboard/server/dashboard_server.dart';
import 'package:flutter_test/flutter_test.dart';

import '../support/fixtures.dart';
import '../support/http_client.dart';
import '../support/mutable_runner.dart';

class ThrowingRunner implements CommandRunner {
  @override
  Future<CommandResult> run(String executable, List<String> arguments) => throw Exception('no such program');
}

const created = CommandResult(exitCode: 0, stdout: 'https://example.test/o/r/issues/12\n');

void main() {
  late Directory repo;
  late Directory web;
  late MutableRunner runner;
  late DashboardServer server;
  late int port;

  Future<void> boot(CommandRunner r) async {
    server = DashboardServer(repo: repo.path, runner: r, webRoot: web.path, port: 0);
    await server.start();
    port = server.port;
  }

  setUp(() async {
    repo = makeRepo();
    web = Directory(join(repo, 'web'))..createSync();
    File(join(web, 'index.html')).writeAsStringSync('<html>home</html>');
    File(join(web, 'app.js')).writeAsStringSync('var a=1;');
    File(join(repo, 'secret.txt')).writeAsStringSync('SECRET');
    runner = MutableRunner(const CommandResult(exitCode: 0, stdout: '[]'));
    await boot(runner);
  });
  tearDown(() async {
    await server.close();
    repo.deleteSync(recursive: true);
  });

  group('DSH-10.a: local only', () {
    test('DSH-10.a: the server answers on 127.0.0.1', () async {
      expect((await ask(port, 'GET', '/')).status, 200);
    });
    test('DSH-10.a: an API request whose Host is not 127.0.0.1 or localhost is answered 404', () async {
      expect((await raw(port, 'GET', '/api/sprint', ['Host: evil.example:$port'])).status, 404);
      expect((await raw(port, 'GET', '/api/issues', ['Host: evil.example'])).status, 404);
      expect(runner.calls, isEmpty);
    });
    test('DSH-10.a: a static request whose Host is not 127.0.0.1 or localhost is answered 404', () async {
      expect((await raw(port, 'GET', '/', ['Host: evil.example'])).status, 404);
    });
    test('DSH-10.a: Host localhost is accepted', () async {
      expect((await ask(port, 'GET', '/', host: 'localhost:$port')).status, 200);
    });
    test('DSH-10.a: an API request whose Origin does not match the Host is answered 404 and runs nothing', () async {
      expect((await raw(port, 'POST', '/api/issues/1/close', ['Host: 127.0.0.1:$port', 'Origin: http://evil.example'])).status, 404);
      expect((await raw(port, 'GET', '/api/issues', ['Host: 127.0.0.1:$port', 'Origin: http://evil.example'])).status, 404);
      expect(runner.calls, isEmpty);
    });
    test('DSH-10.a: a static request whose Origin does not match the Host is answered 404; a matching Origin is accepted', () async {
      expect((await raw(port, 'GET', '/', ['Host: 127.0.0.1:$port', 'Origin: http://evil.example'])).status, 404);
      expect((await raw(port, 'GET', '/', ['Host: 127.0.0.1:$port', 'Origin: http://127.0.0.1:$port'])).status, 200);
    });
    test('DSH-10.a: the listening socket is not reachable on a non-loopback address', () async {
      final others = (await NetworkInterface.list())
          .expand((i) => i.addresses)
          .where((a) => a.type == InternetAddressType.IPv4 && !a.isLoopback)
          .toList();
      if (others.isEmpty) {
        markTestSkipped('no non-loopback IPv4 address on this machine');
        return;
      }
      final client = HttpClient()..connectionTimeout = const Duration(seconds: 2);
      await expectLater(client.getUrl(Uri.parse('http://${others.first.address}:$port/')).then((r) => r.close()),
          throwsA(isA<SocketException>()));
      client.close(force: true);
    });
  });

  group('DSH-10.b: only these requests', () {
    test('DSH-10.b: GET /api/sprint returns the file text; a missing file is 404 with an empty body', () async {
      expect((await ask(port, 'GET', '/api/sprint')).status, 404);
      expect((await ask(port, 'GET', '/api/sprint')).body, '');
      writeFile(repo, 'SCRUM.d/sprint.md', sampleSprintFile);
      final a = await ask(port, 'GET', '/api/sprint');
      expect(a.status, 200);
      expect(a.body, sampleSprintFile);
    });
    test('DSH-10.b and DSH-02.d: PUT /api/sprint writes the whole text and creates the file', () async {
      expect(File(join(repo, 'SCRUM.d/sprint.md')).existsSync(), isFalse);
      expect((await ask(port, 'PUT', '/api/sprint', body: 'first')).status, 200);
      expect(File(join(repo, 'SCRUM.d/sprint.md')).readAsStringSync(), 'first');
      expect((await ask(port, 'PUT', '/api/sprint', body: 'second')).status, 200);
      expect(File(join(repo, 'SCRUM.d/sprint.md')).readAsStringSync(), 'second');
    });
    test('DSH-10.b and DSH-01.a: GET /api/requirements lists feature files and .d parts, skipping README, oldkey, open-questions', () async {
      makeRequirements(repo);
      final a = await ask(port, 'GET', '/api/requirements');
      expect(a.status, 200);
      final m = Map<String, dynamic>.from(a.json as Map);
      final keys = m.keys.map((k) => k.replaceAll("\\", "/")).toList();
      for (final want in ["alpha.md", "connections.d/beta.md", "plugins.d/gamma.md"]) {
        expect(keys.where((k) => k.endsWith(want)), hasLength(1), reason: want);
      }
      expect(m.keys.where((k) => k.contains('README') || k.contains('oldkey') || k.contains('open-questions')), isEmpty);
      expect(m.values.any((v) => (v as String).contains('AAA-01')), isTrue);
    });
    test('DSH-10.b: GET /api/issues runs the tracker list command and returns its output', () async {
      runner.result = const CommandResult(exitCode: 0, stdout: '[{"number":1}]');
      final a = await ask(port, 'GET', '/api/issues');
      expect(a.status, 200);
      expect(a.body, '[{"number":1}]');
      expect(runner.calls.single, [IssueService.executable, ...IssueService.listArguments]);
    });
    test('DSH-10.b: POST /api/issues runs gh issue create with title, body and labels; answers the number', () async {
      runner.result = created;
      final a = await ask(port, 'POST', '/api/issues',
          body: jsonEncode({'title': 'T', 'body': 'B', 'labels': ['issue', 'feature:alpha']}));
      expect(a.status, 200);
      expect(a.json, {'number': 12});
      expect(runner.calls.single,
          ['gh', 'issue', 'create', '--title', 'T', '--body', 'B', '--label', 'issue', '--label', 'feature:alpha']);
    });
    test('DSH-10.b: POST /api/issues with a bad body is 400 and runs nothing', () async {
      expect((await ask(port, 'POST', '/api/issues', body: 'not json')).status, 400);
      expect((await ask(port, 'POST', '/api/issues', body: '{"body":"x"}')).status, 400);
      expect(runner.calls, isEmpty);
    });
    test('DSH-10.b: POST /api/issues/<n>/close runs gh issue close n and answers the number', () async {
      final a = await ask(port, 'POST', '/api/issues/42/close');
      expect(a.status, 200);
      expect(a.json, {'number': 42});
      expect(runner.calls.single, ['gh', 'issue', 'close', '42']);
    });
    test('DSH-10.b: any other request is answered 404 and runs nothing', () async {
      final cases = <List<String>>[
        ['DELETE', '/api/sprint'], ['POST', '/api/sprint'], ['PUT', '/api/issues'], ['DELETE', '/api/issues'],
        ['GET', '/api/issues/42/close'], ['POST', '/api/issues/abc/close'], ['POST', '/api/issues/42'],
        ['POST', '/api/requirements'], ['PUT', '/api/requirements'], ['GET', '/api/nothing'], ['POST', '/'],
        ['PUT', '/index.html'], ['PATCH', '/api/sprint'],
      ];
      for (final c in cases) {
        expect((await ask(port, c[0], c[1], body: '{}')).status, 404, reason: '${c[0]} ${c[1]}');
      }
      expect(runner.calls, isEmpty);
    });
    test('DSH-10.b: static files are served from the web root; / is index.html; only GET and HEAD', () async {
      final root = await ask(port, 'GET', '/');
      expect(root.status, 200);
      expect(root.body, '<html>home</html>');
      expect((await ask(port, 'GET', '/app.js')).body, 'var a=1;');
      expect((await ask(port, 'HEAD', '/app.js')).status, 200);
      expect((await ask(port, 'GET', '/missing.js')).status, 404);
    });
    for (final p in ['/../secret.txt', '/%2e%2e/secret.txt', '/..%2fsecret.txt', '/%2e%2e%2fsecret.txt',
      '/..\\secret.txt', '/..%5csecret.txt', '/C:/Windows/win.ini', '/a:b']) {
      test('DSH-10.b: the static path $p is answered 404 and never serves a file outside the web root', () async {
        final a = await raw(port, 'GET', p, ['Host: 127.0.0.1:$port']);
        expect(a.body, isNot(contains('SECRET')), reason: 'served the file outside the web root');
        expect(a.status, 404, reason: 'body: ${a.body}');
      });
    }
  });

  group('DSH-10.c: arguments are passed separately, no shell, no token', () {
    test('DSH-10.c: request text with shell characters stays one argument each', () async {
      runner.result = created;
      await ask(port, 'POST', '/api/issues',
          body: jsonEncode({'title': 'x; rm -rf', 'body': r'$(id) `id` | a && b', 'labels': ['l1; l2']}));
      expect(runner.calls.single, [
        'gh', 'issue', 'create', '--title', 'x; rm -rf', '--body', r'$(id) `id` | a && b', '--label', 'l1; l2',
      ]);
    });
    test('DSH-10.c and DSH-01.a: no command argument or response header carries a token or authorization', () async {
      runner.result = created;
      await ask(port, 'POST', '/api/issues', body: jsonEncode({'title': 'T', 'body': '', 'labels': []}));
      await ask(port, 'POST', '/api/issues/3/close');
      await ask(port, 'GET', '/api/issues');
      final text = runner.calls.expand((c) => c).join(' ').toLowerCase();
      for (final w in ['token', 'authorization', 'secret']) {
        expect(text, isNot(contains(w)));
      }
    });
  });

  group('DSH-10.d: tracker failure', () {
    test('DSH-10.d: a non-zero exit on list answers 502 with the trimmed stderr as the reason', () async {
      runner.result = const CommandResult(exitCode: 1, stderr: ' not signed in \n');
      final a = await ask(port, 'GET', '/api/issues');
      expect(a.status, 502);
      expect(a.json, {'error': 'not signed in'});
    });
    test('DSH-10.d: a non-zero exit without stderr answers the reason exit code N', () async {
      runner.result = const CommandResult(exitCode: 4);
      final a = await ask(port, 'GET', '/api/issues');
      expect(a.status, 502);
      expect(a.json, {'error': 'exit code 4'});
    });
    test('DSH-10.d: a failing create or close answers 502 with an error', () async {
      runner.result = const CommandResult(exitCode: 1, stderr: 'denied');
      final c = await ask(port, 'POST', '/api/issues', body: jsonEncode({'title': 'T', 'body': '', 'labels': []}));
      expect(c.status, 502);
      expect(c.json, {'error': 'denied'});
      final x = await ask(port, 'POST', '/api/issues/5/close');
      expect(x.status, 502);
      expect(x.json, {'error': 'denied'});
    });
    test('DSH-10.d: a create whose output has no issue URL answers 502', () async {
      runner.result = const CommandResult(exitCode: 0, stdout: 'done');
      final c = await ask(port, 'POST', '/api/issues', body: jsonEncode({'title': 'T', 'body': '', 'labels': []}));
      expect(c.status, 502);
    });
    test('DSH-10.d: a throwing runner answers 502 and the sprint and requirement answers keep working', () async {
      await server.close();
      await boot(ThrowingRunner());
      final a = await ask(port, 'GET', '/api/issues');
      expect(a.status, 502);
      expect((a.json as Map)['error'], isNotEmpty);
      writeFile(repo, 'SCRUM.d/sprint.md', 'S');
      makeRequirements(repo);
      expect((await ask(port, 'GET', '/api/sprint')).body, 'S');
      expect((await ask(port, 'GET', '/api/requirements')).status, 200);
      expect((await ask(port, 'PUT', '/api/sprint', body: 'T')).status, 200);
    });
  });
}
