// Holds: what the dashboard needs from its platform, the same for the web app and the desktop app (DSH-01.e).
// Depends on: the domain, the platform backend (chosen by conditional import: desktop is a LocalBackend, web an
// HttpBackend). Used by: main.dart, the page. Reads or writes: nothing itself.

import '../domain/issue.dart';
import '../domain/new_issue.dart';
import '../domain/progress_entry.dart';
import '../domain/requirement.dart';
import '../domain/sprint.dart';
import '../domain/status.dart';
import 'platform_backend_io.dart' if (dart.library.js_interop) 'platform_backend_web.dart';

/// The data interface of the dashboard. Failures: [StatusRefused] when a status change breaks StatusRule,
/// [IssueTrackerException] when the issue tracker or the server answers badly, [ServerUnreachableException] when the
/// web app cannot reach the server.
abstract class DashboardBackend {
  /// The backend of the platform this build runs on.
  factory DashboardBackend.create() => createPlatformBackend();

  /// The sprint; empty when the file does not exist (DSH-02.e).
  Future<Sprint> loadSprint();

  /// Writes the sprint at once (DSH-02.d).
  Future<void> saveSprint(Sprint sprint);

  Future<List<Requirement>> loadRequirements();

  /// Sets the status of requirement [id]; throws StatusRefused when StatusRule refuses (DSH-13.c).
  Future<void> setRequirementStatus(String id, Status status);

  /// The open issues (DSH-05).
  Future<List<Issue>> loadIssues();

  /// Creates an issue; returns its number (DSH-09.d).
  Future<int> createIssue(NewIssue issue);

  /// Sets the status of issue [number]; throws StatusRefused when StatusRule refuses (DSH-13.c, DSH-13.e).
  Future<void> setIssueStatus(int number, Status status);

  /// The progress files (DSH-12); empty without a progress folder.
  Future<List<ProgressEntry>> loadProgress();

  /// The text of `SCRUM.d/usage.md`, or null when it does not exist (DSH-14.g).
  Future<String?> loadUsage();
}
