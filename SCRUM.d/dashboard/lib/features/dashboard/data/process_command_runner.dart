// Holds: CommandRunner on dart:io Process. Depends on: dart:io, CommandRunner. Used by: platform_backend_io.dart, bin/dashboard_server.dart.
// Reads or writes: starts programs, in [workingDirectory] when given (the web build cannot; it never imports this).

import 'dart:convert';
import 'dart:io';

import 'command_result.dart';
import 'command_runner.dart';

/// Process-backed [CommandRunner]; never uses a shell (DSH-13.f).
class ProcessCommandRunner implements CommandRunner {
  const ProcessCommandRunner({this.workingDirectory});

  final String? workingDirectory;

  @override
  Future<CommandResult> run(String executable, List<String> arguments) async {
    final r = await Process.run(executable, arguments,
        workingDirectory: workingDirectory, stdoutEncoding: utf8, stderrEncoding: utf8); // DSH-13.i
    return CommandResult(exitCode: r.exitCode, stdout: '${r.stdout}', stderr: '${r.stderr}');
  }
}
