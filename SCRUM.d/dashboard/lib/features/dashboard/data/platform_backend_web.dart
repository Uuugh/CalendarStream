// Holds: the web backend: HttpFileAccess and HttpIssueTracker through the server at the page's origin (DSH-01.e).
// Depends on: JsHttpTransport, HttpFileAccess, HttpIssueTracker, DashboardPaths. Used by: DashboardBackend (web builds
// only; no dart:io). Reads or writes: network.

import 'dashboard_backend.dart';
import 'dashboard_paths.dart';
import 'http_file_access.dart';
import 'http_issue_tracker.dart';
import 'js_http_transport.dart';

DashboardBackend createPlatformBackend() {
  const transport = JsHttpTransport();
  return DashboardBackend(
    files: HttpFileAccess(transport),
    issues: const HttpIssueTracker(transport),
    sprintPath: DashboardPaths.sprint,
    requirementsDirectory: DashboardPaths.requirements,
  );
}
