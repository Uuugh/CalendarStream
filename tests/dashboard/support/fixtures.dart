// Shared made-up data and helpers for the dashboard tests: a temp
// repository on disk, and sample sprint and requirement files.
// Depends on the dashboard package; used by every test here; writes only to a temp dir.
import 'dart:convert';
import 'dart:io';

import 'package:dashboard/features/dashboard/data/command_result.dart';
import 'package:dashboard/features/dashboard/data/command_runner.dart';
import 'package:dashboard/features/dashboard/data/disk_file_access.dart';
import 'package:dashboard/features/dashboard/data/file_access.dart';

/// A throwaway directory standing in for the repository.
Directory makeRepo() => Directory.systemTemp.createTempSync('dsh_test_');

final disk = DiskFileAccess();

String join(Directory d, String rel) => '${d.path}/$rel';

void writeFile(Directory repo, String rel, String content) {
  final f = File(join(repo, rel));
  f.parent.createSync(recursive: true);
  f.writeAsStringSync(content);
}

const sampleSprintFile = '''# Sprint

Goal: Ship the demo board

## Stories

| story | title | items | stage | assignee | estimate | usage |
|---|---|---|---|---|---|---|
| S-1 | First story | AAA-01, AAA-02 | Build | Ann | 3 | 1.5 |
| S-2 | Second story | #7 | Backlog |  | 2 | 0 |

## Review

Looked fine.

## Retrospective

Do more of X.
''';

String reqFile(List<String> rows) =>
    '# Requirements: demo\n\nIntro.\n\n| ID | status | statement | test | evidence |\n|---|---|---|---|---|\n${rows.join('\n')}\n';

/// Builds a requirements directory with feature files, `.d` parts and the
/// excluded files, all with made-up rows. Returns its path.
String makeRequirements(Directory repo) {
  writeFile(repo, 'requirements/alpha.md',
      reqFile(['| AAA-01 | proposed | Alpha one. | — | — |', '| AAA-02 |  | Alpha two blank. | — | — |']));
  writeFile(repo, 'requirements/connections.d/beta.md',
      reqFile(['| BBB-01 | backlog | Beta one. | — | — |']));
  writeFile(repo, 'requirements/plugins.d/gamma.md',
      reqFile(['| GGG-01 | done | Gamma one. | — | — |']));
  writeFile(repo, 'requirements/README.md', reqFile(['| RDM-01 | backlog | Readme row. | — | — |']));
  writeFile(repo, 'requirements/oldkey.md', reqFile(['| OLD-01 | backlog | Old row. | — | — |']));
  writeFile(repo, 'requirements/open-questions.md', reqFile(['| OQ-01 | backlog | Question row. | — | — |']));
  writeFile(repo, 'requirements/connections.d/README.md', reqFile(['| CRD-01 | backlog | Folder readme. | — | — |']));
  return join(repo, 'requirements');
}

/// Wraps a FileAccess and records every path read or written (DSH-01.a).
class RecordingFileAccess implements FileAccess {
  RecordingFileAccess(this.inner);
  final FileAccess inner;
  final reads = <String>[];
  final writes = <String>[];

  @override
  Future<String?> read(String path) {
    reads.add(path);
    return inner.read(path);
  }

  @override
  Future<void> write(String path, String content) {
    writes.add(path);
    return inner.write(path, content);
  }

  @override
  Future<List<String>> listFiles(String dir) => inner.listFiles(dir);

  @override
  Future<List<String>> listDirectories(String dir) => inner.listDirectories(dir);
}

/// A command runner that returns a fixed result and records every call.
class FakeRunner implements CommandRunner {
  FakeRunner(this.result);
  final CommandResult result;
  final calls = <List<String>>[];

  @override
  Future<CommandResult> run(String executable, List<String> arguments) async {
    calls.add([executable, ...arguments]);
    return result;
  }
}

/// Tracker JSON for made-up issues.
String issuesJson(List<Map<String, Object?>> issues) => jsonEncode(issues);

Map<String, Object?> issueJson(int n, String title,
        {String state = 'OPEN', String? feature, String? requirement, String? assignee}) =>
    {
      'number': n,
      'title': title,
      'state': state,
      'labels': [if (feature != null) {'name': 'feature:$feature'}, {'name': 'other'}],
      'assignees': [if (assignee != null) {'login': assignee}],
      'body': 'Some text.\n${requirement == null ? '' : 'Requirement: $requirement'}\nMore.',
    };

/// Sprint file whose first story names BBB-01 and issue #7.
const pageSprintFile = '''# Sprint

Goal: Page goal

## Stories

| story | title | items | stage | assignee | estimate | usage |
|---|---|---|---|---|---|---|
| S-1 | Named story | BBB-01, #7 | Build | Ann | 3 | 1 |

## Review

## Retrospective
''';

/// Writes the page fixtures into [repo]; returns the requirements directory.
String makePageRepo(Directory repo) {
  writeFile(repo, 'SCRUM.d/sprint.md', pageSprintFile);
  return makeRequirements(repo);
}
