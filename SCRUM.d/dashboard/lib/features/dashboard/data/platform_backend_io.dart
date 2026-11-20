// Holds: the desktop backend: DiskFileAccess and IssueService on ProcessCommandRunner (DSH-01.e). Depends on:
// DiskFileAccess, ProcessCommandRunner, IssueService, DashboardPaths. Used by: DashboardBackend (desktop builds only).
// Reads or writes: files and programs, at REPO_ROOT (dart-define, default `../..`).

import 'dashboard_backend.dart';
import 'dashboard_paths.dart';
import 'disk_file_access.dart';
import 'issue_service.dart';
import 'process_command_runner.dart';

const _repoRoot = String.fromEnvironment('REPO_ROOT', defaultValue: '../..');

DashboardBackend createPlatformBackend() => const DashboardBackend(
      files: DiskFileAccess(),
      issues: IssueService(runner: ProcessCommandRunner()),
      sprintPath: '$_repoRoot/${DashboardPaths.sprint}',
      requirementsDirectory: '$_repoRoot/${DashboardPaths.requirements}',
    );
