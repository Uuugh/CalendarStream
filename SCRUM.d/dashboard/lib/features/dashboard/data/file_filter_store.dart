// Holds: FilterStore in a JSON file `.dashboard-filters.json` in the working directory (desktop). Depends on: dart:io,
// dart:convert, FilterStore. Used by: platform_filter_store_io.dart. Reads or writes: that file.

import 'dart:convert';
import 'dart:io';

import '../domain/filter_store.dart';

/// Disk-backed [FilterStore].
class FileFilterStore implements FilterStore {
  FileFilterStore({this.path = fileName});

  static const fileName = '.dashboard-filters.json';

  final String path;

  Map<String, dynamic> _read() {
    try {
      final data = jsonDecode(File(path).readAsStringSync());
      return data is Map<String, dynamic> ? data : {};
    } catch (_) {
      return {};
    }
  }

  @override
  List<String>? get(String key) {
    final value = _read()[key];
    return value is List ? [for (final v in value) '$v'] : null;
  }

  @override
  void set(String key, List<String> values) {
    try {
      File(path).writeAsStringSync(jsonEncode({..._read(), key: values}));
    } catch (_) {
      // not kept: the filter starts with everything selected next time
    }
  }
}
