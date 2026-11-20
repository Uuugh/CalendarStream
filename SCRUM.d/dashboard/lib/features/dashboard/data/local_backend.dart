// Holds: the backend that does the work in its own process (DSH-01.e): the sprint and requirement files, the issue
// tracker through `gh`, the progress files. The desktop app uses it and so does the server. It is the one place that
// checks StatusRule (DSH-13.c). Depends on: FileAccess, CommandRunner, SprintRepository, RequirementRepository,
// IssueService, ProgressFile, StatusRule, DashboardPaths. Used by: platform_backend_io.dart, DashboardServer.
// Reads or writes: files under [repoRoot] and [progressDir]; the issue tracker through the runner.

import '../domain/issue.dart';
import '../domain/new_issue.dart';
import '../domain/progress_entry.dart';
import '../domain/progress_file.dart';
import '../domain/requirement.dart';
import '../domain/sprint.dart';
import '../domain/status.dart';
import '../domain/status_refused.dart';
import '../domain/status_rule.dart';
import 'command_runner.dart';
import 'dashboard_backend.dart';
import 'dashboard_paths.dart';
import 'file_access.dart';
import 'issue_service.dart';
import 'requirement_repository.dart';
import 'sprint_repository.dart';

/// [DashboardBackend] on files and programs.
class LocalBackend implements DashboardBackend {
  LocalBackend({required this.files, required this.runner, required this.repoRoot, this.progressDir})
      : _sprints = SprintRepository(files: files, path: '$repoRoot/${DashboardPaths.sprint}'),
        _requirements = RequirementRepository(files: files, directory: '$repoRoot/${DashboardPaths.requirements}'),
        _issues = IssueService(runner: runner);

  final FileAccess files;
  final CommandRunner runner;

  /// The repository folder.
  final String repoRoot;

  /// The folder of the `*.progress` files, or null for none (DSH-12.b).
  final String? progressDir;

  final SprintRepository _sprints;
  final RequirementRepository _requirements;
  final IssueService _issues;

  @override
  Future<Sprint> loadSprint() => _sprints.load();

  @override
  Future<void> saveSprint(Sprint sprint) => _sprints.save(sprint);

  @override
  Future<List<Requirement>> loadRequirements() => _requirements.load();

  @override
  Future<void> setRequirementStatus(String id, Status status) async {
    final current = (await _requirements.load()).where((r) => r.id == id).firstOrNull;
    if (current == null) throw StatusRefused('no requirement $id');
    final reason = StatusRule.refusal(current.status, status);
    if (reason != null) throw StatusRefused(reason);
    if (current.status == status) return;
    if (!await _requirements.setStatus(id, status)) throw StatusRefused('no requirement $id');
  }

  @override
  Future<List<Issue>> loadIssues() => _issues.load();

  @override
  Future<int> createIssue(NewIssue issue) => _issues.create(issue);

  @override
  Future<void> setIssueStatus(int number, Status status) async {
    final labels = await _issues.statusLabelsOf(number);
    final current = labels.isEmpty ? Status.backlog : labels.reduce((a, b) => a.index >= b.index ? a : b);
    final reason = StatusRule.refusal(current, status);
    if (reason != null) throw StatusRefused(reason);
    await _issues.relabel(number, labels, status);
  }

  @override
  Future<List<ProgressEntry>> loadProgress() async {
    final dir = progressDir;
    if (dir == null) return const [];
    final result = <ProgressEntry>[];
    for (final path in await files.listFiles(dir)) {
      final name = path.split('/').last;
      if (!name.endsWith(ProgressFile.extension)) continue;
      final text = await files.read(path);
      final entry = text == null ? null : ProgressFile.parse(name, text);
      if (entry != null) result.add(entry);
    }
    return result;
  }

  @override
  Future<String?> loadUsage() => files.read('$repoRoot/${DashboardPaths.usage}');
}
