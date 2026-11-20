// Holds: the choice of FilterStore for the platform this build runs on, by conditional import (DSH-04).
// Depends on: the platform filter stores. Used by: main.dart. Reads or writes: nothing itself.

import '../domain/filter_store.dart';
import 'platform_filter_store_io.dart' if (dart.library.js_interop) 'platform_filter_store_web.dart';

/// Makes the [FilterStore] of the platform.
class FilterStoreFactory {
  const FilterStoreFactory._();

  static FilterStore create() => createPlatformFilterStore();
}
