// Holds: the content type of each kind of file the web build has. Depends on: nothing.
// Used by: DashboardServer. Reads or writes: nothing.

/// Maps a file name to its content type.
class ContentTypes {
  const ContentTypes._();

  static const _byExtension = {
    'html': 'text/html; charset=utf-8',
    'js': 'text/javascript; charset=utf-8',
    'mjs': 'text/javascript; charset=utf-8',
    'css': 'text/css; charset=utf-8',
    'json': 'application/json; charset=utf-8',
    'map': 'application/json; charset=utf-8',
    'wasm': 'application/wasm',
    'png': 'image/png',
    'ico': 'image/x-icon',
    'svg': 'image/svg+xml',
    'otf': 'font/otf',
    'ttf': 'font/ttf',
    'woff2': 'font/woff2',
    'txt': 'text/plain; charset=utf-8',
  };

  static String of(String fileName) {
    final dot = fileName.lastIndexOf('.');
    final extension = dot < 0 ? '' : fileName.substring(dot + 1).toLowerCase();
    return _byExtension[extension] ?? 'application/octet-stream';
  }
}
