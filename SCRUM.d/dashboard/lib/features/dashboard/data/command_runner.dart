// Holds: the command running the services use, so tests can pass a fake. Depends on: CommandResult.
// Used by: IssueService. Reads or writes: nothing itself; implementations run programs.

import 'command_result.dart';

/// Runs a program and returns its result; throws when the program cannot be started.
abstract class CommandRunner {
  Future<CommandResult> run(String executable, List<String> arguments);
}
