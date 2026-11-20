// Holds: the one request function the web implementations use, so tests can pass a fake.
// Depends on: HttpReply. Used by: HttpFileAccess, HttpIssueTracker. Reads or writes: nothing itself.

import 'http_reply.dart';

/// Sends a request to the server at the page's own origin.
abstract class HttpTransport {
  /// Throws [ServerUnreachableException] when the server cannot be contacted; any HTTP status is a normal [HttpReply].
  Future<HttpReply> send(String method, String path, {String? body});
}
