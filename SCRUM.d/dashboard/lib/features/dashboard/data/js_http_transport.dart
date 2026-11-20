// Holds: HttpTransport on the browser's fetch (dart:js_interop, no package). Depends on: dart:js_interop,
// dart:js_interop_unsafe, HttpTransport. Used by: platform_backend_web.dart (the desktop build never imports it).
// Reads or writes: network, to the page's own origin.

import 'dart:js_interop';
import 'dart:js_interop_unsafe';

import 'http_reply.dart';
import 'http_transport.dart';
import 'server_unreachable_exception.dart';

/// Browser-backed [HttpTransport]; [path] is relative (`/api/...`), so the request goes to the page's own origin.
class JsHttpTransport implements HttpTransport {
  const JsHttpTransport();

  @override
  Future<HttpReply> send(String method, String path, {String? body}) async {
    try {
      final init = JSObject()..setProperty('method'.toJS, method.toJS);
      if (body != null) {
        init.setProperty('body'.toJS, body.toJS);
        init.setProperty('headers'.toJS, JSObject()..setProperty('content-type'.toJS, 'application/json'.toJS));
      }
      final response =
          await globalContext.callMethod<JSPromise<JSObject>>('fetch'.toJS, path.toJS, init).toDart;
      final status = response.getProperty<JSNumber>('status'.toJS).toDartInt;
      final text = await response.callMethod<JSPromise<JSString>>('text'.toJS).toDart;
      return HttpReply(status, text.toDart);
    } catch (e) {
      throw ServerUnreachableException('$e');
    }
  }
}
