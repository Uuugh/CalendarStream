// Holds: FileAccess through the server (DSH-01.e, DSH-10.b): the sprint path maps to GET/PUT /api/sprint and the
// requirements folder to GET /api/requirements. Depends on: HttpTransport, DashboardPaths, FileAccess, ServerUnreachableException.
// Used by: the web backend. Reads or writes: network, through the transport.

import 'dart:convert';

import 'dashboard_paths.dart';
import 'file_access.dart';
import 'http_transport.dart';

/// Web [FileAccess]. Paths are repository-relative (DashboardPaths). Listing the requirements folder reads them
/// again from the server; reads of files below it use that copy.
class HttpFileAccess implements FileAccess {
  HttpFileAccess(this.transport);

  final HttpTransport transport;

  Map<String, String> _requirements = {};

  @override
  Future<String?> read(String path) async {
    if (path == DashboardPaths.sprint) {
      final reply = await transport.send('GET', '/api/sprint');
      if (reply.status == 404) return null;
      if (!reply.ok) throw Exception('server answered ${reply.status}');
      return reply.body;
    }
    return _requirements[path];
  }

  @override
  Future<void> write(String path, String content) async {
    if (path != DashboardPaths.sprint) throw UnsupportedError('only the sprint file can be written');
    final reply = await transport.send('PUT', '/api/sprint', body: content);
    if (!reply.ok) throw Exception('server answered ${reply.status}');
  }

  @override
  Future<List<String>> listFiles(String dir) async {
    if (dir == DashboardPaths.requirements) await _refresh();
    return _below(dir).where((p) => !p.substring(dir.length + 1).contains('/')).toList();
  }

  @override
  Future<List<String>> listDirectories(String dir) async {
    final names = <String>{};
    for (final p in _below(dir)) {
      final rest = p.substring(dir.length + 1);
      final slash = rest.indexOf('/');
      if (slash > 0) names.add('$dir/${rest.substring(0, slash)}');
    }
    return names.toList()..sort();
  }

  Iterable<String> _below(String dir) => _requirements.keys.where((p) => p.startsWith('$dir/')).toList()..sort();

  Future<void> _refresh() async {
    final reply = await transport.send('GET', '/api/requirements');
    if (!reply.ok) throw Exception('server answered ${reply.status}');
    final data = jsonDecode(reply.body) as Map<String, dynamic>;
    _requirements = {for (final e in data.entries) '${DashboardPaths.requirements}/${e.key}': '${e.value}'};
  }
}
