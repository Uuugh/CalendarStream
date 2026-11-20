// Holds: CommandRunner on dart:io Process. Depends on: dart:io, CommandRunner. Used by: main.dart.
// Reads or writes: starts programs (the web build cannot; it throws UnsupportedError).

import 'dart:io';

import 'command_result.dart';
import 'command_runner.dart';

/// Process-backed [CommandRunner].
class ProcessCommandRunner implements CommandRunner {
  const ProcessCommandRunner();

  @override
  Future<CommandResult> run(String executable, List<String> arguments) async {
    final r = await Process.run(executable, arguments);
    return CommandResult(exitCode: r.exitCode, stdout: '${r.stdout}', stderr: '${r.stderr}');
  }
}
