// Holds: the dashboard server (DSH-13): serves the web build and gives it the sprint file, the requirements, the
// issues, the progress and the usage over HTTP. Pure Dart. Depends on: dart:io, dart:convert, LocalBackend, FileAccess,
// DiskFileAccess, CommandRunner, SprintRepository, Status, NewIssue, StatusRefused, IssueTrackerException,
// DashboardServerConfig, ContentTypes. Used by: bin/dashboard_server.dart, tests. Reads or writes: through the
// LocalBackend (files under [repo] and [progressDir], the issue tracker through the runner); files under [webRoot];
// a socket on 127.0.0.1. It holds no token and reads no secret; it never takes a path from a request.

import 'dart:convert';
import 'dart:io';

import '../data/command_runner.dart';
import '../data/disk_file_access.dart';
import '../data/file_access.dart';
import '../data/issue_tracker_exception.dart';
import '../data/local_backend.dart';
import '../data/sprint_repository.dart';
import '../domain/new_issue.dart';
import '../domain/status.dart';
import '../domain/status_refused.dart';
import 'content_types.dart';
import 'dashboard_server_config.dart';

/// The server. Answers only the requests of DSH-13.b; anything else is 404.
class DashboardServer {
  DashboardServer({
    required this.repo,
    required this.runner,
    required this.webRoot,
    int port = DashboardServerConfig.port,
    this.progressDir,
    this.files = const DiskFileAccess(),
  })  : _requestedPort = port,
        _backend = LocalBackend(files: files, runner: runner, repoRoot: repo, progressDir: progressDir);

  /// The repository folder: the sprint file, the requirements and the usage file are here.
  final String repo;

  /// Runs the issue tracker's commands (DSH-13.f); the arguments are passed separately, never through a shell.
  final CommandRunner runner;

  /// The folder holding the built web app.
  final String webRoot;

  /// The folder of the `*.progress` files, or null for none (DSH-12.b).
  final String? progressDir;

  final FileAccess files;
  final int _requestedPort;
  final LocalBackend _backend;
  HttpServer? _server;

  /// The port in use once started (the OS's choice when 0 was asked).
  int get port => _server?.port ?? _requestedPort;

  static final _requirementStatusRoute = RegExp(r'^/api/requirements/([A-Z]+-[0-9]+(?:\.[a-z]+)?)/status$');
  static final _issueStatusRoute = RegExp(r'^/api/issues/([0-9]+)/status$');

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
    } on StatusRefused catch (e) {
      await _json(request, HttpStatus.conflict, {'error': e.reason});
    } on IssueTrackerException catch (e) {
      await _json(request, HttpStatus.badGateway, {'error': e.reason});
    } catch (e) {
      await _json(request, HttpStatus.internalServerError, {'error': '$e'});
    }
  }

  /// The routes of DSH-13.b and nothing else.
  Future<void> _route(HttpRequest request) async {
    final path = request.uri.path;
    final method = request.method;
    if (!_sameOrigin(request)) return _notFound(request);
    if (!path.startsWith('/api/')) return _static(request);
    if (path == '/api/sprint' && method == 'GET') return _readSprint(request);
    if (path == '/api/sprint' && method == 'PUT') return _writeSprint(request);
    if (path == '/api/requirements' && method == 'GET') return _listRequirements(request);
    final requirement = _requirementStatusRoute.firstMatch(path);
    if (requirement != null && method == 'PUT') return _setRequirementStatus(request, requirement.group(1)!);
    if (path == '/api/issues' && method == 'GET') return _listIssues(request);
    if (path == '/api/issues' && method == 'POST') return _createIssue(request);
    final issue = _issueStatusRoute.firstMatch(path);
    if (issue != null && method == 'POST') return _setIssueStatus(request, int.parse(issue.group(1)!));
    if (path == '/api/progress' && method == 'GET') return _listProgress(request);
    if (path == '/api/usage' && method == 'GET') return _readUsage(request);
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

  Future<void> _readSprint(HttpRequest request) async =>
      _send(request, HttpStatus.ok, 'text/plain; charset=utf-8', SprintRepository.format(await _backend.loadSprint()));

  Future<void> _writeSprint(HttpRequest request) async {
    await _backend.saveSprint(SprintRepository.parse(await utf8.decoder.bind(request).join()));
    await _send(request, HttpStatus.ok, 'text/plain; charset=utf-8', '');
  }

  Future<void> _listRequirements(HttpRequest request) async =>
      _json(request, HttpStatus.ok, [for (final r in await _backend.loadRequirements()) r.toJson()]);

  Future<void> _setRequirementStatus(HttpRequest request, String id) async {
    final status = await _statusFrom(request);
    if (status == null) return;
    await _backend.setRequirementStatus(id, status);
    await _json(request, HttpStatus.ok, {'id': id, 'status': status.name});
  }

  Future<void> _listIssues(HttpRequest request) async =>
      _json(request, HttpStatus.ok, [for (final i in await _backend.loadIssues()) i.toJson()]);

  Future<void> _createIssue(HttpRequest request) async {
    final data = await _body(request);
    if (data == null) return;
    final status = data['status'] == null ? Status.backlog : Status.tryName('${data['status']}');
    if (data['title'] is! String || (data['title'] as String).trim().isEmpty || status == null) {
      return _json(request, HttpStatus.badRequest, {'error': 'expected a title and a status'});
    }
    final number = await _backend.createIssue(NewIssue.fromJson({...data, 'status': status.name}));
    await _json(request, HttpStatus.ok, {'number': number});
  }

  Future<void> _setIssueStatus(HttpRequest request, int number) async {
    final status = await _statusFrom(request);
    if (status == null) return;
    await _backend.setIssueStatus(number, status);
    await _json(request, HttpStatus.ok, {'number': number, 'status': status.name});
  }

  Future<void> _listProgress(HttpRequest request) async =>
      _json(request, HttpStatus.ok, [for (final p in await _backend.loadProgress()) p.toJson()]);

  Future<void> _readUsage(HttpRequest request) async {
    final text = await _backend.loadUsage();
    if (text == null) return _send(request, HttpStatus.notFound, 'text/plain; charset=utf-8', '');
    await _send(request, HttpStatus.ok, 'text/plain; charset=utf-8', text);
  }

  /// The JSON object of the request body, or null after answering 400.
  Future<Map<String, dynamic>?> _body(HttpRequest request) async {
    try {
      final data = jsonDecode(await utf8.decoder.bind(request).join());
      if (data is Map<String, dynamic>) return data;
    } on FormatException {
      // answered below
    }
    await _json(request, HttpStatus.badRequest, {'error': 'body is not a JSON object'});
    return null;
  }

  /// The status in a body `{"status": s}`, or null after answering 400.
  Future<Status?> _statusFrom(HttpRequest request) async {
    final data = await _body(request);
    if (data == null) return null;
    final status = Status.tryName(data['status'] as String?);
    if (status == null) await _json(request, HttpStatus.badRequest, {'error': 'expected a status'});
    return status;
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
    response.add(utf8.encode(body)); // bytes, so the declared utf-8 is what is sent (DSH-13.i)
    await response.close();
  }
}
