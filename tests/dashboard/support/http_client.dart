// A tiny dart:io HTTP client for the server tests, and a fake HttpTransport that records calls.
// Depends on the dashboard package; used by server_test.dart and http_data_test.dart; touches only 127.0.0.1 and memory.
import 'dart:convert';
import 'dart:io';

import 'package:dashboard/features/dashboard/data/http_reply.dart';
import 'package:dashboard/features/dashboard/data/http_transport.dart';

class Answer {
  Answer(this.status, this.body);
  final int status;
  final String body;
  dynamic get json => jsonDecode(body);
}

/// Sends [method] [path] to 127.0.0.1:[port]; [host] and [origin] override the Host and Origin headers.
Future<Answer> ask(int port, String method, String path,
    {String? body, String? host, String? origin, Map<String, String> headers = const {}}) async {
  final client = HttpClient();
  try {
    final req = await client.openUrl(method, Uri.parse('http://127.0.0.1:$port$path'));
    if (host != null) req.headers.host = host;
    if (origin != null) req.headers.set('origin', origin);
    headers.forEach(req.headers.set);
    if (body != null) {
      req.headers.contentType = ContentType.json;
      final bytes = utf8.encode(body);
      req.contentLength = bytes.length;
      req.add(bytes);
    }
    final res = await req.close();
    return Answer(res.statusCode, await utf8.decodeStream(res));
  } finally {
    client.close(force: true);
  }
}

/// A transport answering from [handler]; records "METHOD path" and the body of every call.
class FakeTransport implements HttpTransport {
  FakeTransport(this.handler);
  final Future<HttpReply> Function(String method, String path, String? body) handler;
  final calls = <String>[];
  final bodies = <String?>[];

  @override
  Future<HttpReply> send(String method, String path, {String? body}) {
    calls.add('$method $path');
    bodies.add(body);
    return handler(method, path, body);
  }
}

/// Sends [method] [target] over a raw socket, exactly as written, with the given header lines (no Host unless given).
/// Used where dart:io's client would rewrite the Host header or normalize the path.
Future<Answer> raw(int port, String method, String target, List<String> headerLines) async {
  final socket = await Socket.connect('127.0.0.1', port);
  socket.write('$method $target HTTP/1.1\r\n${headerLines.join('\r\n')}\r\nConnection: close\r\n\r\n');
  await socket.flush();
  final text = await utf8.decodeStream(socket);
  socket.destroy();
  final status = int.parse(text.split(' ')[1]);
  final at = text.indexOf('\r\n\r\n');
  return Answer(status, at < 0 ? '' : text.substring(at + 4));
}

/// An HttpTransport that really sends each request to the server on 127.0.0.1:[port] (so HttpBackend can be run
/// against a real DashboardServer).
class ServerTransport implements HttpTransport {
  ServerTransport(this.port);
  final int port;

  @override
  Future<HttpReply> send(String method, String path, {String? body}) async {
    final a = await ask(port, method, path, body: body);
    return HttpReply(a.status, a.body);
  }
}
