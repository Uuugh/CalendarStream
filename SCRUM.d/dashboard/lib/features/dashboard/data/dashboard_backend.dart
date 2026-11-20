// Holds: what the dashboard needs from its platform: file access, the issue tracker and the paths (DSH-01.e).
// Depends on: FileAccess, IssueTracker, the platform backend (chosen by conditional import: desktop reads the files and
// runs `gh` itself, web asks the server). Used by: main.dart. Reads or writes: nothing itself.

import 'file_access.dart';
import 'issue_tracker.dart';
import 'platform_backend_io.dart' if (dart.library.js_interop) 'platform_backend_web.dart';

/// The data interface the dashboard page is built on, the same for the web app and the desktop app (DSH-01.e).
class DashboardBackend {
  const DashboardBackend({
    required this.files,
    required this.issues,
    required this.sprintPath,
    required this.requirementsDirectory,
  });

  /// The backend of the platform this build runs on.
  factory DashboardBackend.create() => createPlatformBackend();

  final FileAccess files;
  final IssueTracker issues;

  /// Path of the sprint file as [files] takes it.
  final String sprintPath;

  /// Path of the requirements folder as [files] takes it.
  final String requirementsDirectory;
}
