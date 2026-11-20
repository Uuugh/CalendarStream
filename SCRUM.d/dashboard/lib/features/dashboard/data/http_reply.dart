// Holds: the answer of one HTTP request. Depends on: nothing. Used by: HttpTransport, HttpFileAccess, HttpIssueTracker.
// Reads or writes: nothing.

/// Status code and text body of a finished request.
class HttpReply {
  const HttpReply(this.status, this.body);

  final int status;
  final String body;

  bool get ok => status >= 200 && status < 300;
}
