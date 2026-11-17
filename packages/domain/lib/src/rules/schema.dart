/// Rule limits, types and constants.
///
/// Holds: rule limits, action types, shadowing kinds.
/// Depends on: nothing.
/// Used by: the rule validation, matching, conflict and migration code.
/// Reads/writes: nothing.
/// Ported from: app/rule_engine/schema.py (the oracle until step 5).
/// Requirements: RUL-11, RUL-21.
library;

final RegExp colorPattern = RegExp(r'^#[0-9a-fA-F]{6}$');
final RegExp idPattern = RegExp(r'^[a-z0-9]{1,16}$');
final RegExp sourceIdPattern = RegExp(r'^(ccs|[fl][0-9a-f]{6})$');

const int maxRules = 60;
const int maxConditions = 12;
const int maxActions = 6;
const int maxBrackets = 3;

const int maxText = 200;
const int maxRegex = 100;
const int maxTitle = 80;
const int maxEmoji = 16;

/// Minutes.
const int maxOffset = 7 * 24 * 60;
const int maxLength = 52 * 7 * 24 * 60;

/// Seconds a typed regex may take on one event before it counts as no match.
const double regexTimeoutSeconds = 0.05;

/// CCS+ writes whole days as 00:01-23:59:59.
const Duration allDayTolerance = Duration(minutes: 5);

const Map<String, String> actionTypes = {
  'color': 'Color',
  'emoji': 'Add emoji to title',
  'event': 'Create event',
  'change': 'Change',
  'add': 'Add',
  'move': 'Move this event',
  'delete': 'Delete this event',
  'changes': 'Record changes in the event notes section',
};

/// The only Thens of a link rule.
const List<String> linkActions = ['delete', 'move'];

/// A Change / Add to Notes.
const int maxNotes = 1000;

/// Move this event: up to a week either way (minutes).
const int maxMove = 7 * 24 * 60;

const List<String> shadowed = [
  'color',
  'emoji',
  'change',
  'change:title',
  'change:notes',
  'change:location',
  'add:title',
  'add:notes',
  'add:location',
  'move',
];

const Map<String, String> modeToOp = {
  'word': 'word',
  'contains': 'contains',
  'starts': 'begins',
  'exact': 'is',
};
