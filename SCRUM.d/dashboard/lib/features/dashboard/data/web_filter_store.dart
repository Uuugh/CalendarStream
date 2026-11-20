// Holds: FilterStore in the browser's local storage (dart:js_interop_unsafe, no package). Depends on: dart:js_interop,
// dart:js_interop_unsafe, dart:convert, FilterStore. Used by: platform_filter_store_web.dart. Reads or writes: local storage.

import 'dart:convert';
import 'dart:js_interop';
import 'dart:js_interop_unsafe';

import '../domain/filter_store.dart';

/// Local-storage-backed [FilterStore]; each key is stored as `dashboard.filter.<key>`.
class WebFilterStore implements FilterStore {
  const WebFilterStore();

  static const _prefix = 'dashboard.filter.';

  JSObject? get _storage {
    try {
      return globalContext.getProperty<JSObject?>('localStorage'.toJS);
    } catch (_) {
      return null;
    }
  }

  @override
  List<String>? get(String key) {
    try {
      final text = _storage?.callMethod<JSString?>('getItem'.toJS, '$_prefix$key'.toJS)?.toDart;
      if (text == null) return null;
      final data = jsonDecode(text);
      return data is List ? [for (final v in data) '$v'] : null;
    } catch (_) {
      return null;
    }
  }

  @override
  void set(String key, List<String> values) {
    try {
      _storage?.callMethod<JSAny?>('setItem'.toJS, '$_prefix$key'.toJS, jsonEncode(values).toJS);
    } catch (_) {
      // not kept: the filter starts with everything selected next time
    }
  }
}
