/// A rule that cannot be saved; the message says why.
///
/// Holds: [RuleError].
/// Depends on: nothing.
/// Used by: rule validation.
/// Reads/writes: nothing.
/// Ported from: app/rule_engine/rule_error.py. Requirements: RUL-19..RUL-21.
library;

class RuleError implements Exception {
  const RuleError(this.message);

  final String message;

  @override
  String toString() => message;
}
