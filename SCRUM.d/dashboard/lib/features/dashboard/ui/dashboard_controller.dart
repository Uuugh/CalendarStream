// Holds: the state of the dashboard page and every change it makes through the backend (DSH-01.c, DSH-07, DSH-08,
// DSH-09, DSH-10, DSH-12.c, DSH-14). Depends on: DashboardBackend, FilterStore, MultiFilter, SprintEdit, DropRule,
// UsageTable and the domain. Used by: DashboardPage and the widgets it builds. Reads or writes: through the backend.

import 'package:flutter/foundation.dart';

import '../data/dashboard_backend.dart';
import '../domain/block_kind.dart';
import '../domain/drop_rule.dart';
import '../domain/filter_store.dart';
import '../domain/issue.dart';
import '../domain/member.dart';
import '../domain/multi_filter.dart';
import '../domain/new_issue.dart';
import '../domain/progress_entry.dart';
import '../domain/requirement.dart';
import '../domain/sprint.dart';
import '../domain/sprint_edit.dart';
import '../domain/status.dart';
import '../domain/status_refused.dart';
import '../domain/usage_row.dart';
import '../domain/usage_table.dart';

/// Loads and changes the dashboard's data. Each of the five reads keeps its own error, so a failure shows in the
/// place that needs that data and the others keep working (DSH-01.b, DSH-01.f). Every change method returns the
/// reason it was refused (shown as {reason} of msg:dshMoveRefused) or null when it succeeded or changed nothing.
class DashboardController extends ChangeNotifier {
  DashboardController({required this.backend, required this.filterStore});

  final DashboardBackend backend;
  final FilterStore filterStore;

  Sprint? sprint;
  Object? sprintError;
  List<Requirement>? requirements;
  Object? requirementsError;
  List<Issue>? issues;
  Object? issuesError;
  List<ProgressEntry>? progress;
  Object? progressError;

  /// The rows of the usage table; null when there is no usage file or no table (DSH-14.g).
  List<UsageRow>? usage;
  Object? usageError;

  bool _disposed = false;
  final Map<String, MultiFilter> _filters = {};

  @override
  void dispose() {
    _disposed = true;
    super.dispose();
  }

  @override
  void notifyListeners() {
    if (!_disposed) super.notifyListeners();
  }

  /// Reads the sprint, the requirements, the issues, the progress and the usage again (DSH-01.c).
  Future<void> reload() async {
    await Future.wait([_loadSprint(), _loadRequirements(), _loadIssues(), reloadLive()]);
    notifyListeners();
  }

  /// Reads the progress and the usage again (DSH-12.c).
  Future<void> reloadLive() async {
    await Future.wait([_loadProgress(), _loadUsage()]);
    notifyListeners();
  }

  Future<void> _loadSprint() async {
    try {
      sprint = await backend.loadSprint();
      sprintError = null;
    } catch (e) {
      sprintError = e;
    }
  }

  Future<void> _loadRequirements() async {
    try {
      requirements = await backend.loadRequirements();
      requirementsError = null;
    } catch (e) {
      requirementsError = e;
    }
  }

  Future<void> _loadIssues() async {
    try {
      issues = await backend.loadIssues();
      issuesError = null;
    } catch (e) {
      issuesError = e;
    }
  }

  Future<void> _loadProgress() async {
    try {
      progress = await backend.loadProgress();
      progressError = null;
    } catch (e) {
      progressError = e;
    }
  }

  Future<void> _loadUsage() async {
    try {
      final text = await backend.loadUsage();
      usage = text == null ? null : UsageTable.parse(text);
      usageError = null;
    } catch (e) {
      usageError = e;
    }
  }

  /// The filter kept under [key] over [choices]: restored from the store the first time, then kept in step with the
  /// choices (UIC-21).
  MultiFilter filter(String key, List<String> choices) {
    final known = _filters[key];
    if (known == null) {
      if (choices.isEmpty) return MultiFilter(choices);
      final made = MultiFilter.restore(choices, filterStore.get(key));
      _filters[key] = made;
      return made;
    }
    if (!listEquals(known.choices, choices)) {
      final next = known.withChoices(choices);
      _filters[key] = next;
      return next;
    }
    return known;
  }

  /// Keeps [value] as the filter [key] and saves its selection; the lists update at once (UIC-21).
  void setFilter(String key, MultiFilter value) {
    _filters[key] = value;
    try {
      filterStore.set(key, value.selectedList);
    } catch (_) {
      // A store that cannot write leaves the filter working for this run (FilterStore).
    }
    notifyListeners();
  }

  /// The title of [item] (a requirement ID or `#N`): its statement or issue title, or null when it is not loaded.
  String? titleOf(String item) {
    if (item.startsWith('#')) {
      final n = int.tryParse(item.substring(1));
      for (final i in issues ?? const <Issue>[]) {
        if (i.number == n) return i.title;
      }
      return null;
    }
    for (final r in requirements ?? const <Requirement>[]) {
      if (r.id == item) return r.statement;
    }
    return null;
  }

  Status? _statusOf(String item) {
    if (item.startsWith('#')) {
      final n = int.tryParse(item.substring(1));
      for (final i in issues ?? const <Issue>[]) {
        if (i.number == n) return i.status;
      }
      return null;
    }
    for (final r in requirements ?? const <Requirement>[]) {
      if (r.id == item) return r.status;
    }
    return null;
  }

  Future<void> _setStatus(String item, Status status) {
    if (item.startsWith('#')) return backend.setIssueStatus(int.parse(item.substring(1)), status);
    return backend.setRequirementStatus(item, status);
  }

  Future<String?> _guarded(Future<void> Function() change) async {
    try {
      await change();
      return null;
    } on StatusRefused catch (e) {
      return e.reason;
    } catch (e) {
      return '$e';
    } finally {
      await reload();
    }
  }

  /// Drops block [id] on block [parent] (null is the top of the board) (DSH-07.a, DSH-07.b).
  Future<String?> dropBlock(String id, String? parent) async {
    final current = sprint;
    if (current == null) return null;
    final refusal = SprintEdit.moveRefusal(current, id, parent);
    if (refusal != null) return refusal;
    final next = SprintEdit.moveBlock(current, id, parent);
    if (identical(next, current)) return null;
    return _guarded(() => backend.saveSprint(next));
  }

  /// Why a requirement or an issue dropped on the board background is refused (DSH-07.c).
  String dropItemOnBoard() => DropRule.itemTargets;

  /// Drops a block on the Backlog block, which holds none (DSH-07.g).
  String dropBlockOnBacklog() => DropRule.blockOnBacklog;

  /// Drops [item] (a requirement ID or `#N`) on story [storyId], or on the Backlog block when it is null
  /// (DSH-07.c to DSH-07.h).
  Future<String?> dropItem(String item, String? storyId) async {
    final current = sprint;
    final status = _statusOf(item);
    if (current == null || status == null) return null;
    final refusal = DropRule.itemRefusal(current, storyId);
    if (refusal != null) return refusal;
    final from = current.storyOf(item);
    if (storyId == null) {
      if (status == Status.backlog && from == null) return null;
      return _guarded(() async {
        if (status != Status.backlog) await _setStatus(item, Status.backlog);
        if (from != null) await backend.saveSprint(SprintEdit.removeMember(current, item));
      });
    }
    if (status == Status.planned && from == storyId) return null;
    return _guarded(() async {
      if (status != Status.planned) await _setStatus(item, Status.planned);
      final next = SprintEdit.addMember(current, storyId, item);
      if (!identical(next, current)) await backend.saveSprint(next);
    });
  }

  /// Accept: sets every requirement and issue of story [storyId] to done (DSH-08.a).
  Future<String?> accept(String storyId) async {
    final current = sprint;
    if (current == null) return null;
    return _guarded(() async {
      for (final item in current.itemsOf(storyId)) {
        final status = _statusOf(item);
        if (status != null && status != Status.done) await _setStatus(item, Status.done);
      }
    });
  }

  /// Adds a block at the top of the board (DSH-06.b).
  Future<String?> addBlock(BlockKind kind, String name) async {
    final current = sprint;
    if (current == null) return null;
    final next = SprintEdit.addBlock(current, kind, name);
    if (identical(next, current)) return null;
    return _guarded(() => backend.saveSprint(next));
  }

  /// Sets a story's estimate or usage (DSH-10.a).
  Future<String?> setPoints(String storyId, {double? estimate, double? usage}) async {
    final current = sprint;
    if (current == null) return null;
    var next = current;
    if (estimate != null) next = SprintEdit.setEstimate(next, storyId, estimate);
    if (usage != null) next = SprintEdit.setUsage(next, storyId, usage);
    if (identical(next, current)) return null;
    return _guarded(() => backend.saveSprint(next));
  }

  /// Creates an issue (DSH-09.d) and reloads the lists (DSH-09.g). Throws what the backend throws, so the form can say why
  /// (DSH-09.e).
  Future<void> createIssue(NewIssue issue) async {
    await backend.createIssue(issue);
    await reload();
  }

  /// The `#N` form of an issue number.
  static String issueItem(int number) => Member.issue(number);
}
