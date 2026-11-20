// Holds: FileAccess on the local disk. Depends on: dart:io, FileAccess.
// Used by: main.dart. Reads or writes: files on disk (the web build cannot use it).

import 'dart:io';

import 'file_access.dart';

/// Disk-backed [FileAccess].
class DiskFileAccess implements FileAccess {
  const DiskFileAccess();

  @override
  Future<String?> read(String path) async {
    final file = File(path);
    if (!await file.exists()) return null;
    return file.readAsString();
  }

  @override
  Future<void> write(String path, String content) async {
    final file = File(path);
    await file.parent.create(recursive: true);
    await file.writeAsString(content);
  }

  @override
  Future<List<String>> listFiles(String dir) => _list<File>(dir);

  @override
  Future<List<String>> listDirectories(String dir) => _list<Directory>(dir);

  Future<List<String>> _list<T extends FileSystemEntity>(String dir) async {
    final directory = Directory(dir);
    if (!await directory.exists()) return [];
    final entries = await directory.list().where((e) => e is T).toList();
    return entries.map((e) => e.path.replaceAll('\\', '/')).toList()..sort();
  }
}
