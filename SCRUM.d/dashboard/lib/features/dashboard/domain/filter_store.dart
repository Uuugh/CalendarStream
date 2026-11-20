// Holds: where the filters' selected choices are kept between runs (DSH-04). Depends on: nothing.
// Used by: the page. Reads or writes: nothing itself; implementations keep the values (web: local storage; desktop: a file).

/// Keeps string lists by key. A failure to read or write is silent: the filter then starts with everything selected.
abstract class FilterStore {
  /// The list kept under [key], or null when none is.
  List<String>? get(String key);

  void set(String key, List<String> values);
}
