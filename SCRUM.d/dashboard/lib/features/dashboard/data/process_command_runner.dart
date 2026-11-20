// Holds: CommandRunner on dart:io Process. Depends on: dart:io, CommandRunner. Used by: main (desktop), the server.
// Reads or writes: starts programs, in [workingDirectory] when given (the web build cannot; it never imports this).

import 'dart:io';

import 'command_result.dart';
import 'command_runner.dart';

/// Process-backed [CommandRunner]; never uses a shell (DSH-10.c).
class ProcessCommandRunner implements CommandRunner {
  const ProcessCommandRunner({this.workingDirectory});

  final String? workingDirectory;

  @override
  Future<CommandResult> run(String executable, List<String> arguments) async {
    final r = await Process.run(executable, arguments, workingDirectory: workingDirectory);
    return CommandResult(exitCode: r.exitCode, stdout: '${r.stdout}', stderr: '${r.stderr}');
  }
}
