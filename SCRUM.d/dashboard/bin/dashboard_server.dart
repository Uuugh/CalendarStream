// Holds: the command that starts the dashboard server (DSH-13). Depends on: DashboardServer, ProcessCommandRunner,
// DashboardServerConfig. Used by: the user. Reads or writes: nothing itself (see DashboardServer).
//
// Start (from SCRUM.d/dashboard, after `flutter build web`, the only other step):
//
//     dart run bin/dashboard_server.dart [--repo <path>] [--progress <dir>] [--port <n>]
//
// then open http://127.0.0.1:8765/. `--repo` is the repository folder, default `../..`; `--progress` the folder of the
// `*.progress` files, default none; `--port` the port, default DashboardServerConfig.port. The server serves
// `build/web` and runs `gh` inside the repository folder.

import 'dart:io';

import 'package:dashboard/features/dashboard/data/process_command_runner.dart';
import 'package:dashboard/features/dashboard/server/dashboard_server.dart';
import 'package:dashboard/features/dashboard/server/dashboard_server_config.dart';

Future<void> main(List<String> arguments) async {
  const usage = 'usage: dart run bin/dashboard_server.dart [--repo <path>] [--progress <dir>] [--port <n>]';
  var repo = '../..';
  String? progress;
  var port = DashboardServerConfig.port;
  for (var i = 0; i < arguments.length; i++) {
    final hasValue = i + 1 < arguments.length;
    if (arguments[i] == '--repo' && hasValue) {
      repo = arguments[++i];
    } else if (arguments[i] == '--progress' && hasValue) {
      progress = arguments[++i];
    } else if (arguments[i] == '--port' && hasValue && int.tryParse(arguments[i + 1]) != null) {
      port = int.parse(arguments[++i]);
    } else {
      stderr.writeln(usage);
      exit(64);
    }
  }
  final server = DashboardServer(
    repo: repo,
    runner: ProcessCommandRunner(workingDirectory: repo),
    webRoot: 'build/web',
    port: port,
    progressDir: progress,
  );
  await server.start();
  stdout.writeln('Dashboard at http://${DashboardServerConfig.host}:${server.port}/ (repo: $repo)');
}
