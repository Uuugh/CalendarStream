// Holds: the desktop filter store (a file). Depends on: FileFilterStore. Used by: filter_store_factory.dart (desktop builds).
// Reads or writes: nothing itself.

import '../domain/filter_store.dart';
import 'file_filter_store.dart';

FilterStore createPlatformFilterStore() => FileFilterStore();
