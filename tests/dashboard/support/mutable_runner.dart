// A command runner whose result a test can change between calls, and that records every call.
// Depends on the dashboard package; used by the usage and reload tests; touches nothing outside memory.
import 'package:dashboard/features/dashboard/data/command_result.dart';
import 'package:dashboard/features/dashboard/data/command_runner.dart';

class MutableRunner implements CommandRunner {
  MutableRunner(this.result);
  CommandResult result;
  final calls = <List<String>>[];

  @override
  Future<CommandResult> run(String executable, List<String> arguments) async {
    calls.add([executable, ...arguments]);
    return result;
  }
}
