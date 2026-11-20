// Holds: the dashboard server (DSH-10): serves the web build and gives it the sprint file, the requirement files and
// the issues over HTTP. Pure Dart. Depends on: dart:io, dart:convert, FileAccess, DiskFileAccess, CommandRunner,
// RequirementRepository, IssueService (its `gh` arguments), DashboardPaths, DashboardServerConfig, ContentTypes.
// Used by: bin/dashboard_server.dart, tests. Reads or writes: files under [repo] and [webRoot]; the issue tracker
// through the runner; a socket on 127.0.0.1. It holds no token and reads no secret; it never takes a path from a request.

import 'dart:convert';
import 'dart:io';

import '../data/command_runner.dart';
import '../data/dashboard_paths.dart';
import '../data/disk_file_access.dart';
import '../data/file_access.dart';
import '../data/issue_service.dart';
import '../data/requirement_repository.dart';
import 'content_types.dart';
import 'dashboard_server_config.dart';

/// The server. Answers only the requests of DSH-10.b; anything else is 404.
class DashboardServer {
  DashboardServer({
    required this.repo,
    required this.runner,
    required this.webRoot,
    int port = DashboardServerConfig.port,
    this.files = const DiskFileAccess(),
  }) : _requestedPort = port;

  /// The repository folder: the sprint file and the requirements are read from here.
  final String repo;

  /// Runs the issue tracker's commands (DSH-10.c); the arguments are passed separately, never through a shell.
  final CommandRunner runner;

  /// The folder holding the built web app.
  final String webRoot;

  final FileAccess files;
  final int _requestedPort;
  HttpServer? _server;

  /// The port in use once started (the OS's choice when 0 was asked).
  int get port => _server?.port ?? _requestedPort;

  static final _closeRoute = RegExp(r'^/api/issues/(\d+)/close$');

  Future<void> start() async {
    final server = await HttpServer.bind(InternetAddress(DashboardServerConfig.host), _requestedPort);
    _server = server;
    server.listen(_handle);
  }

  Future<void> close() async {
    await _server?.close(force: true);
    _server = null;
  }

  Future<void> _handle(HttpRequest request) async {
    try {
      await _route(request);
    } catch (e) {
      await _json(request, HttpStatus.internalServerError, {'error': '$e'});
    }
  }

  Future<void> _route(HttpRequest request) async {
    final path = request.uri.path;
    final method = request.method;
    if (!_sameOrigin(request)) return _notFound(request);
    if (!path.startsWith('/api/')) return _static(request);
    if (path == '/api/sprint' && method == 'GET') return _readSprint(request);
    if (path == '/api/sprint' && method == 'PUT') return _writeSprint(request);
    if (path == '/api/requirements' && method == 'GET') return _requirements(request);
    if (path == '/api/issues' && method == 'GET') return _listIssues(request);
    if (path == '/api/issues' && method == 'POST') return _createIssue(request);
    final close = _closeRoute.firstMatch(path);
    if (close != null && method == 'POST') return _closeIssue(request, close.group(1)!);
    return _notFound(request);
  }

  /// A page of another site must not drive the server: the Host is this machine and any Origin is the server itself.
  bool _sameOrigin(HttpRequest request) {
    final host = (request.headers.value('host') ?? '').split(':').first;
    if (host != DashboardServerConfig.host && host != 'localhost') return false;
    final origin = request.headers.value('origin');
    if (origin == null) return true;
    final uri = Uri.tryParse(origin);
    return uri != null && uri.host == host && uri.port == (request.headers.port ?? 80);
  }

  String get _sprintPath => '$repo/${DashboardPaths.sprint}';

  Future<void> _readSprint(HttpRequest request) async {
    final text = await files.read(_sprintPath);
    if (text == null) return _send(request, HttpStatus.notFound, 'text/plain; charset=utf-8', '');
    await _send(request, HttpStatus.ok, 'text/plain; charset=utf-8', text);
  }

  Future<void> _writeSprint(HttpRequest request) async {
    await files.write(_sprintPath, await utf8.decoder.bind(request).join());
    await _send(request, HttpStatus.ok, 'text/plain; charset=utf-8', '');
  }

  Future<void> _requirements(HttpRequest request) async {
    final texts = await RequirementRepository(files: files, directory: '$repo/${DashboardPaths.requirements}').readTexts();
    await _json(request, HttpStatus.ok, texts);
  }

  Future<void> _listIssues(HttpRequest request) async {
    final out = await _gh(IssueService.listArguments);
    if (out.error != null) return _json(request, HttpStatus.badGateway, {'error': out.error});
    await _send(request, HttpStatus.ok, 'application/json; charset=utf-8', out.stdout);
  }

  Future<void> _createIssue(HttpRequest request) async {
    final Object? data;
    try {
      data = jsonDecode(await utf8.decoder.bind(request).join());
    } on FormatException {
      return _json(request, HttpStatus.badRequest, {'error': 'body is not JSON'});
    }
    if (data is! Map || data['title'] is! String || data['body'] is! String || data['labels'] is! List) {
      return _json(request, HttpStatus.badRequest, {'error': 'expected title, body and labels'});
    }
    final labels = [for (final l in data['labels'] as List) '$l'];
    final out = await _gh(IssueService.createArguments(data['title'] as String, data['body'] as String, labels));
    if (out.error != null) return _json(request, HttpStatus.badGateway, {'error': out.error});
    final number = IssueService.numberFrom(out.stdout);
    if (number == null) return _json(request, HttpStatus.badGateway, {'error': 'no issue number'});
    await _json(request, HttpStatus.ok, {'number': number});
  }

  Future<void> _closeIssue(HttpRequest request, String number) async {
    final out = await _gh(['issue', 'close', number]);
    if (out.error != null) return _json(request, HttpStatus.badGateway, {'error': out.error});
    await _json(request, HttpStatus.ok, {'number': int.parse(number)});
  }

  /// Runs the tracker command; [error] is its reason when it failed (DSH-10.d).
  Future<({String stdout, String? error})> _gh(List<String> arguments) async {
    try {
      final r = await runner.run(IssueService.executable, arguments);
      if (r.exitCode == 0) return (stdout: r.stdout, error: null);
      final reason = r.stderr.trim();
      return (stdout: '', error: reason.isEmpty ? 'exit code ${r.exitCode}' : reason);
    } catch (e) {
      return (stdout: '', error: '$e');
    }
  }

  Future<void> _static(HttpRequest request) async {
    if (request.method != 'GET' && request.method != 'HEAD') return _notFound(request);
    final segments = request.uri.pathSegments.where((s) => s.isNotEmpty).toList();
    if (segments.any((s) => s == '..' || s == '.' || s.contains('/') || s.contains('\\') || s.contains(':') || s.contains('\u0000'))) {
      return _notFound(request);
    }
    final file = File([webRoot, ...(segments.isEmpty ? ['index.html'] : segments)].join('/'));
    if (!await file.exists()) return _notFound(request);
    final root = await Directory(webRoot).resolveSymbolicLinks();
    final resolved = await file.resolveSymbolicLinks();
    if (!resolved.startsWith(root.endsWith(Platform.pathSeparator) ? root : '$root${Platform.pathSeparator}')) {
      return _notFound(request);
    }
    final response = request.response;
    response.statusCode = HttpStatus.ok;
    response.headers.contentType = ContentType.parse(ContentTypes.of(file.path));
    if (request.method == 'GET') await response.addStream(file.openRead());
    await response.close();
  }

  Future<void> _notFound(HttpRequest request) => _send(request, HttpStatus.notFound, 'text/plain; charset=utf-8', 'not found');

  Future<void> _json(HttpRequest request, int status, Object body) =>
      _send(request, status, 'application/json; charset=utf-8', jsonEncode(body));

  Future<void> _send(HttpRequest request, int status, String contentType, String body) async {
    final response = request.response;
    response.statusCode = status;
    response.headers.contentType = ContentType.parse(contentType);
    response.write(body);
    await response.close();
  }
}
