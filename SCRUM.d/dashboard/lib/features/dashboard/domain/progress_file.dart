// Holds: reading one `*.progress` file (DSH-12, DSH-12.d). Depends on: ProgressEntry.
// Used by: LocalBackend. Reads or writes: nothing.

import 'progress_entry.dart';

/// A progress file: its name is the agent's label and its content is `done/total`.
class ProgressFile {
  const ProgressFile._();

  static const extension = '.progress';
  static final _content = RegExp(r'^\s*(\d+)\s*/\s*(\d+)\s*$');

  /// The entry of file [name] with content [text], or null when the content is not `done/total` (DSH-12.d).
  static ProgressEntry? parse(String name, String text) {
    final m = _content.firstMatch(text);
    if (m == null) return null;
    final done = int.tryParse(m.group(1)!);
    final total = int.tryParse(m.group(2)!);
    if (done == null || total == null) return null;
    final label = name.endsWith(extension) ? name.substring(0, name.length - extension.length) : name;
    return ProgressEntry(label, done, total);
  }
}
