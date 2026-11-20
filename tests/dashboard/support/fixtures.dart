// Shared made-up data and helpers for the dashboard tests: a temp repository on disk, sample sprint, requirement
// and issue data, and the fake command runner.
// Depends on the dashboard package; used by every test here; writes only to a temp dir.
import 'dart:convert';
import 'dart:io';

import 'package:dashboard/features/dashboard/data/command_result.dart';
import 'package:dashboard/features/dashboard/data/command_runner.dart';
import 'package:dashboard/features/dashboard/data/disk_file_access.dart';

/// A throwaway directory standing in for the repository.
Directory makeRepo() => Directory.systemTemp.createTempSync('dsh_test_');

final disk = DiskFileAccess();

String join(Directory d, String rel) => '${d.path}/$rel';

void writeFile(Directory repo, String rel, String content) {
  final f = File(join(repo, rel));
  f.parent.createSync(recursive: true);
  f.writeAsStringSync(content);
}

/// A sprint file in the layout of DSH-02: an epic in a sprint, two stories, members and review text.
const sampleSprintFile = '''# Sprint

## Blocks

| id | kind | name | parent | assignee | estimate | usage |
|---|---|---|---|---|---|---|
| sprint-1 | sprint | First sprint |  |  | 0 | 0 |
| epic-1 | epic | Demo epic | sprint-1 |  | 0 | 0 |
| story-1 | story | First story | epic-1 | Ann | 3 | 1.5 |
| story-2 | story | Second story | sprint-1 |  | 2 | 0 |

## Members

| story | item |
|---|---|
| story-1 | AAA-01 |
| story-1 | AAA-03 |
| story-2 | #7 |

## Review

Looked fine.

## Retrospective

Do more of X.
''';

String reqFile(List<String> rows, {String eol = '\n'}) =>
    '# Requirements: demo\n\nIntro.\n\n| ID | status | statement | test | evidence |\n|---|---|---|---|---|\n${rows.join('\n')}\n'
        .replaceAll('\n', eol);

/// The requirement files of the made-up repository (feature files, `.d` parts, a CRLF file and the excluded
/// files), by path relative to the repository root.
Map<String, String> requirementFiles() => {
      'requirements/alpha.md': reqFile([
        '| AAA-01 | proposed | Alpha one. | — | — |',
        '| AAA-02 |  | Alpha two blank. | — | — |',
        '| AAA-03 | planned | Alpha three. | — | — |',
        '| AAA-04 | done (see AAA-03) | Alpha four. | — | — |',
        '| AAA-05.a | backlog | Alpha five a. | — | — |',
      ]),
      'requirements/connections.d/beta.md': reqFile(['| BBB-01 | backlog | Beta one. | — | — |']),
      'requirements/plugins.d/gamma.md': reqFile(['| GGG-01 | proposed | Gamma one. | — | — |']),
      'requirements/delta.md': reqFile(['| DDD-01 | backlog | Delta one. | — | — |', '| DDD-02 | proposed | Delta two. | — | — |'], eol: '\r\n'),
      'requirements/README.md': reqFile(['| RDM-01 | backlog | Readme row. | — | — |']),
      'requirements/oldkey.md': reqFile(['| OLD-01 | backlog | Old row. | — | — |']),
      'requirements/open-questions.md': reqFile(['| OQ-01 | backlog | Question row. | — | — |']),
      'requirements/connections.d/README.md': reqFile(['| CRD-01 | backlog | Folder readme. | — | — |']),
    };

/// Writes [requirementFiles] into [repo]. Returns the requirements directory.
String makeRequirements(Directory repo) {
  requirementFiles().forEach((rel, content) => writeFile(repo, rel, content));
  return join(repo, 'requirements');
}

/// The made-up repository in memory, under the root `/r`: the sprint file (when [sprint] is given) and the
/// requirement files, plus [extra].
Map<String, String> memoryFiles({String? sprint = sampleSprintFile, Map<String, String> extra = const {}}) => {
      if (sprint != null) memSprintPath: sprint,
      for (final e in requirementFiles().entries) '/r/${e.key}': e.value,
      ...extra,
    };

const memRoot = '/r';
const memSprintPath = '/r/SCRUM.d/sprint.md';
const memRequirementsDir = '/r/requirements';
const memUsagePath = '/r/SCRUM.d/usage.md';

/// A command runner that returns a fixed result (or what [handler] returns for the arguments) and records every call.
class FakeRunner implements CommandRunner {
  FakeRunner(this.result, {this.handler});
  CommandResult result;
  final CommandResult Function(List<String> arguments)? handler;
  final calls = <List<String>>[];

  @override
  Future<CommandResult> run(String executable, List<String> arguments) async {
    calls.add([executable, ...arguments]);
    return handler?.call(arguments) ?? result;
  }
}

/// Tracker JSON for made-up issues.
String issuesJson(List<Map<String, Object?>> issues) => jsonEncode(issues);

/// One made-up tracker issue; [labels] are added to the `feature:` label and an unrelated one.
Map<String, Object?> issueJson(int n, String title,
        {String? feature, String? requirement, String? assignee, List<String> labels = const []}) =>
    {
      'number': n,
      'title': title,
      'labels': [
        if (feature != null) {'name': 'feature:$feature'},
        {'name': 'other'},
        for (final l in labels) {'name': l},
      ],
      'assignees': [if (assignee != null) {'login': assignee}],
      'body': 'Some text.\n${requirement == null ? '' : 'Requirement: $requirement'}\nMore.',
    };

/// The answer of `gh issue view N --json labels` for the given label names.
CommandResult viewResult(List<String> labels) =>
    CommandResult(exitCode: 0, stdout: jsonEncode({'labels': [for (final l in labels) {'name': l}]}));

const createdIssue12 = CommandResult(exitCode: 0, stdout: 'https://example.test/o/r/issues/12\n');
