// A FileAccess that fails for the paths a test names and passes everything else on.
// Depends on the dashboard package; used by tests for unreadable and unwritable files; touches nothing outside its inner access.
import 'package:dashboard/features/dashboard/data/file_access.dart';

class FailingFileAccess implements FileAccess {
  FailingFileAccess(this.inner, {required this.failsOn, this.reason = 'disk gone'});
  final FileAccess inner;
  final bool Function(String path) failsOn;
  final String reason;

  void _check(String path) {
    if (failsOn(path)) throw Exception(reason);
  }

  @override
  Future<String?> read(String path) async {
    _check(path);
    return inner.read(path);
  }

  @override
  Future<void> write(String path, String content) async {
    _check(path);
    return inner.write(path, content);
  }

  @override
  Future<void> writeAtomic(String path, String content) async {
    _check(path);
    return inner.writeAtomic(path, content);
  }

  @override
  Future<List<String>> listFiles(String dir) async {
    _check(dir);
    return inner.listFiles(dir);
  }

  @override
  Future<List<String>> listDirectories(String dir) async {
    _check(dir);
    return inner.listDirectories(dir);
  }
}
