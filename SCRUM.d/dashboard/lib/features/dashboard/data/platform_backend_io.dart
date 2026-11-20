// Holds: the desktop backend: a LocalBackend on the disk and `gh` (DSH-01.e). Depends on: LocalBackend, DiskFileAccess,
// ProcessCommandRunner. Used by: DashboardBackend (desktop builds only). Reads or writes: nothing itself; the backend
// reads files and runs programs at REPO_ROOT (dart-define, default `../..`) and the progress folder PROGRESS_DIR (default none).

import 'dashboard_backend.dart';
import 'disk_file_access.dart';
import 'local_backend.dart';
import 'process_command_runner.dart';

const _repoRoot = String.fromEnvironment('REPO_ROOT', defaultValue: '../..');
const _progressDir = String.fromEnvironment('PROGRESS_DIR');

DashboardBackend createPlatformBackend() => LocalBackend(
      files: const DiskFileAccess(),
      runner: const ProcessCommandRunner(workingDirectory: _repoRoot),
      repoRoot: _repoRoot,
      progressDir: _progressDir.isEmpty ? null : _progressDir,
    );
