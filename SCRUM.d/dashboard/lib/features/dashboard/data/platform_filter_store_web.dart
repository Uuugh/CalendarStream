// Holds: the web filter store (local storage). Depends on: WebFilterStore. Used by: filter_store_factory.dart (web builds;
// no dart:io). Reads or writes: nothing itself.

import '../domain/filter_store.dart';
import 'web_filter_store.dart';

FilterStore createPlatformFilterStore() => const WebFilterStore();
