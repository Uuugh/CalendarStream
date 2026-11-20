// Holds: the outcome of one command run. Depends on: nothing. Used by: CommandRunner, IssueService.
// Reads or writes: nothing.

/// Exit code and output of a finished command.
class CommandResult {
  const CommandResult({required this.exitCode, this.stdout = '', this.stderr = ''});

  final int exitCode;
  final String stdout;
  final String stderr;
}
