// An in-memory FileAccess for fast tests: files live in a map keyed by '/' paths; every plain and atomic write is recorded.
// Depends on the dashboard package; used by tests that need no disk; reads and writes only its map.
import 'package:dashboard/features/dashboard/data/file_access.dart';

class MemoryFileAccess implements FileAccess {
  MemoryFileAccess([Map<String, String>? files]) : files = {...?files};
  final Map<String, String> files;

  /// The paths written with [write], and with [writeAtomic], in order.
  final writes = <String>[];
  final atomicWrites = <String>[];
  final reads = <String>[];

  @override
  Future<String?> read(String path) async {
    reads.add(path);
    return files[path];
  }

  @override
  Future<void> write(String path, String content) async {
    writes.add(path);
    files[path] = content;
  }

  @override
  Future<void> writeAtomic(String path, String content) async {
    atomicWrites.add(path);
    files[path] = content;
  }

  @override
  Future<List<String>> listFiles(String dir) async =>
      files.keys.where((p) => p.startsWith('$dir/') && !p.substring(dir.length + 1).contains('/')).toList()..sort();

  @override
  Future<List<String>> listDirectories(String dir) async => files.keys
      .where((p) => p.startsWith('$dir/') && p.substring(dir.length + 1).contains('/'))
      .map((p) => '$dir/${p.substring(dir.length + 1).split('/').first}')
      .toSet()
      .toList()
    ..sort();
}
