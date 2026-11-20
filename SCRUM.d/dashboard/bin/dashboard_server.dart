// Holds: the command that starts the dashboard server (DSH-10). Depends on: DashboardServer, ProcessCommandRunner,
// DashboardServerConfig. Used by: the user. Reads or writes: nothing itself (see DashboardServer).
//
// Start (from SCRUM.d/dashboard, after `flutter build web`, the only other step):
//
//     dart run bin/dashboard_server.dart [--repo <path>]
//
// then open http://127.0.0.1:8765/. `--repo` is the repository folder, default `../..`; the server serves
// `build/web` and runs `gh` inside the repository folder.

import 'dart:io';

import 'package:dashboard/features/dashboard/data/process_command_runner.dart';
import 'package:dashboard/features/dashboard/server/dashboard_server.dart';
import 'package:dashboard/features/dashboard/server/dashboard_server_config.dart';

Future<void> main(List<String> arguments) async {
  var repo = '../..';
  for (var i = 0; i < arguments.length; i++) {
    if (arguments[i] == '--repo' && i + 1 < arguments.length) {
      repo = arguments[++i];
    } else {
      stderr.writeln('usage: dart run bin/dashboard_server.dart [--repo <path>]');
      exit(64);
    }
  }
  final server = DashboardServer(repo: repo, runner: ProcessCommandRunner(workingDirectory: repo), webRoot: 'build/web');
  await server.start();
  stdout.writeln('Dashboard at http://${DashboardServerConfig.host}:${server.port}/ (repo: $repo)');
}
