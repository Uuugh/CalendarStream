// Tests LocalBackend, which does what the server does in its own process: the status rule (DSH-13.c), the moves of
// DSH-07 (d, e, f, g, h) and DSH-08.a (Accept) as status changes of requirements and issues, DSH-12 (progress files),
// DSH-14.g (usage text), DSH-01.a (what is changed), DSH-01.b (the tracker's failure does not stop the rest).
// Fakes only: in-memory files and a fake runner that records every call. One run covers each ID named in the test name.
import 'package:dashboard/features/dashboard/data/command_result.dart';
import 'package:dashboard/features/dashboard/data/local_backend.dart';
import 'package:dashboard/features/dashboard/domain/new_issue.dart';
import 'package:dashboard/features/dashboard/domain/sprint_edit.dart';
import 'package:dashboard/features/dashboard/domain/status.dart';
import 'package:dashboard/features/dashboard/domain/status_refused.dart';
import 'package:flutter_test/flutter_test.dart';

import '../support/fixtures.dart';
import '../support/memory_file_access.dart';
import '../support/mutable_runner.dart';

void main() {
  late MemoryFileAccess files;
  late FakeRunner runner;
  late LocalBackend backend;

  /// The tracker holds one issue per number with the labels in [tracker]; view answers them, everything else succeeds.
  late Map<int, List<String>> tracker;

  setUp(() {
    tracker = {5: ['issue', 'backlog'], 6: ['issue', 'proposed'], 7: ['issue', 'planned', 'feature:alpha'], 8: ['issue', 'done'], 9: ['issue']};
    files = MemoryFileAccess(memoryFiles(extra: {
      '/prog/a.progress': '3/10',
      '/prog/b.progress': ' 10 / 10\n',
      '/prog/bad.progress': 'three of ten',
      '/prog/notes.txt': '1/2',
    }));
    runner = FakeRunner(const CommandResult(exitCode: 0), handler: (a) {
      if (a[0] == 'issue' && a[1] == 'view') return viewResult(tracker[int.parse(a[2])] ?? []);
      if (a[0] == 'issue' && a[1] == 'create') return createdIssue12;
      if (a[0] == 'issue' && a[1] == 'list') return CommandResult(exitCode: 0, stdout: issuesJson([issueJson(5, 'Five', labels: ['backlog'])]));
      return const CommandResult(exitCode: 0);
    });
    backend = LocalBackend(files: files, runner: runner, repoRoot: memRoot, progressDir: '/prog');
  });

  Future<Status> statusOf(String id) async => (await backend.loadRequirements()).firstWhere((r) => r.id == id).status;

  group('requirement status moves (DSH-07, DSH-13.c)', () {
    test('DSH-07.d: dropping a proposed requirement on the Backlog block sets it to backlog', () async {
      await backend.setRequirementStatus('AAA-01', Status.backlog);
      expect(await statusOf('AAA-01'), Status.backlog);
    });

    test('DSH-07.e: dropping a requirement on a story sets it to planned and the story records it', () async {
      await backend.setRequirementStatus('AAA-02', Status.planned);
      await backend.saveSprint(SprintEdit.addMember(await backend.loadSprint(), 'story-2', 'AAA-02'));
      expect(await statusOf('AAA-02'), Status.planned);
      expect((await backend.loadSprint()).itemsOf('story-2'), contains('AAA-02'));
    });

    test('DSH-07.f: a planned requirement taken out of its story goes back to backlog and out of the Members rows', () async {
      await backend.setRequirementStatus('AAA-03', Status.backlog);
      await backend.saveSprint(SprintEdit.removeMember(await backend.loadSprint(), 'AAA-03'));
      expect(await statusOf('AAA-03'), Status.backlog);
      expect((await backend.loadSprint()).storyOf('AAA-03'), isNull);
    });

    test('DSH-07.g and DSH-13.c: any other move down is refused with its reason and the file is not touched', () async {
      for (final c in [
        ['AAA-04', Status.planned], ['AAA-04', Status.backlog], ['AAA-04', Status.proposed],
        ['AAA-03', Status.proposed], ['BBB-01', Status.proposed],
      ]) {
        final id = c[0] as String;
        await expectLater(backend.setRequirementStatus(id, c[1] as Status),
            throwsA(isA<StatusRefused>().having((e) => e.reason, 'reason', isNotEmpty)), reason: '$id to ${(c[1] as Status).name}');
      }
      expect(files.atomicWrites, isEmpty);
      expect(files.writes, isEmpty);
    });

    test('DSH-07.g: a requirement that does not exist is refused', () async {
      await expectLater(backend.setRequirementStatus('ZZZ-99', Status.planned), throwsA(isA<StatusRefused>()));
    });

    test('DSH-07.h: setting the status a requirement already has changes nothing', () async {
      await backend.setRequirementStatus('AAA-03', Status.planned);
      await backend.setRequirementStatus('BBB-01', Status.backlog);
      expect(files.atomicWrites, isEmpty);
    });

    test('DSH-13.c: every move up the order is accepted, from a blank status too', () async {
      await backend.setRequirementStatus('AAA-02', Status.done);
      await backend.setRequirementStatus('AAA-01', Status.done);
      expect(await statusOf('AAA-02'), Status.done);
      expect(await statusOf('AAA-01'), Status.done);
    });

    test('DSH-13.d: a status change writes only that requirement file, by an atomic write', () async {
      await backend.setRequirementStatus('AAA-01', Status.planned);
      expect(files.atomicWrites, ['$memRequirementsDir/alpha.md']);
      expect(files.writes, isEmpty);
    });
  });

  group('Accept (DSH-08, DSH-08.a)', () {
    test('DSH-08.a: Accept sets every requirement and issue of the story to done', () async {
      final sprint = await backend.loadSprint();
      final story = sprint.itemsOf('story-1');
      expect(story, ['AAA-01', 'AAA-03']);
      tracker[7] = ['issue', 'planned'];
      for (final item in [...story, '#7']) {
        if (item.startsWith('#')) {
          await backend.setIssueStatus(int.parse(item.substring(1)), Status.done);
        } else {
          await backend.setRequirementStatus(item, Status.done);
        }
      }
      expect(await statusOf('AAA-01'), Status.done);
      expect(await statusOf('AAA-03'), Status.done);
      expect(runner.calls.last, ['gh', 'issue', 'edit', '7', '--add-label', 'done', '--remove-label', 'planned']);
    });

    test('DSH-08.a: accepting an item that is already done changes nothing', () async {
      await backend.setRequirementStatus('AAA-04', Status.done);
      await backend.setIssueStatus(8, Status.done);
      expect(files.atomicWrites, isEmpty);
      expect(runner.calls.where((c) => c.contains('edit')), isEmpty);
    });
  });

  group('issue status moves (DSH-07, DSH-13.c, DSH-13.e)', () {
    test('DSH-07.e: an issue dropped on a story gets planned: the label is created, planned added, the old one removed', () async {
      await backend.setIssueStatus(5, Status.planned);
      expect(runner.calls, [
        ['gh', 'issue', 'view', '5', '--json', 'labels'],
        ['gh', 'label', 'create', 'planned', '--force'],
        ['gh', 'issue', 'edit', '5', '--add-label', 'planned', '--remove-label', 'backlog'],
      ]);
    });

    test('DSH-07.d: a proposed issue dropped on the Backlog block gets backlog', () async {
      await backend.setIssueStatus(6, Status.backlog);
      expect(runner.calls.last, ['gh', 'issue', 'edit', '6', '--add-label', 'backlog', '--remove-label', 'proposed']);
    });

    test('DSH-07.f: a planned issue taken out of its story gets backlog', () async {
      await backend.setIssueStatus(7, Status.backlog);
      expect(runner.calls.last, ['gh', 'issue', 'edit', '7', '--add-label', 'backlog', '--remove-label', 'planned']);
    });

    test('DSH-07.g and DSH-13.c: a move down in any other way is refused with its reason and nothing is edited', () async {
      await expectLater(backend.setIssueStatus(8, Status.planned), throwsA(isA<StatusRefused>().having((e) => e.reason, 'reason', isNotEmpty)));
      await expectLater(backend.setIssueStatus(7, Status.proposed), throwsA(isA<StatusRefused>()));
      await expectLater(backend.setIssueStatus(5, Status.proposed), throwsA(isA<StatusRefused>()));
      expect(runner.calls.where((c) => c[1] == 'issue' && c[2] == 'edit' || c[1] == 'label'), isEmpty);
    });

    test('DSH-07.h: setting the status an issue already has changes nothing', () async {
      await backend.setIssueStatus(7, Status.planned);
      expect(runner.calls, [['gh', 'issue', 'view', '7', '--json', 'labels']]);
    });

    test('DSH-05.a and DSH-13.c: an issue with no status label counts as backlog: planned is allowed and proposed is refused', () async {
      await backend.setIssueStatus(9, Status.planned);
      expect(runner.calls.last, ['gh', 'issue', 'edit', '9', '--add-label', 'planned']);
      await expectLater(backend.setIssueStatus(9, Status.proposed), throwsA(isA<StatusRefused>()));
    });

    test('DSH-13.e: when an issue has two status labels all the other ones are removed', () async {
      tracker[5] = ['backlog', 'proposed'];
      await backend.setIssueStatus(5, Status.planned);
      expect(runner.calls.last, ['gh', 'issue', 'edit', '5', '--add-label', 'planned', '--remove-label', 'backlog', '--remove-label', 'proposed']);
    });

    test('DSH-13.e: the open or closed state of the issue is never changed', () async {
      await backend.setIssueStatus(5, Status.done);
      final text = runner.calls.expand((c) => c).join(' ');
      for (final w in ['close', 'reopen', '--state']) {
        expect(text, isNot(contains(w)));
      }
    });

    test('DSH-13.g: when the tracker fails the reason comes back and the files still load', () async {
      runner.result = const CommandResult(exitCode: 1, stderr: 'not signed in');
      final failing = FakeRunner(const CommandResult(exitCode: 1, stderr: 'not signed in'));
      final b = LocalBackend(files: files, runner: failing, repoRoot: memRoot);
      await expectLater(b.setIssueStatus(5, Status.planned), throwsA(predicate((e) => '$e' == 'not signed in')));
      await expectLater(b.loadIssues(), throwsA(predicate((e) => '$e' == 'not signed in')));
      expect(await b.loadRequirements(), isNotEmpty);
      expect((await b.loadSprint()).blocks, isNotEmpty);
    });
  });

  group('creating and listing issues (DSH-09.d, DSH-09.g, DSH-01.b)', () {
    test('DSH-09.d: createIssue returns the number and runs one gh issue create with the labels', () async {
      final n = await backend.createIssue(const NewIssue(title: 'T', feature: 'alpha', requirement: 'AAA-01', status: Status.planned));
      expect(n, 12);
      expect(runner.calls, [
        ['gh', 'label', 'create', 'planned', '--force'],
        ['gh', 'issue', 'create', '--title', 'T', '--body', 'Requirement: AAA-01', '--label', 'issue', '--label', 'feature:alpha', '--label', 'planned'],
      ]);
    });

    test('DSH-09.g: the issue list is read from the tracker with the open-issue command', () async {
      final list = await backend.loadIssues();
      expect(list.single.number, 5);
      expect(runner.calls.single.sublist(0, 6), ['gh', 'issue', 'list', '--state', 'open', '--limit']);
    });
  });

  group('progress files (DSH-12, DSH-12.a, DSH-12.b, DSH-12.c, DSH-12.d)', () {
    test('DSH-12 and DSH-12.a: each .progress file gives a bar: the file name as label, done and total, and the text done/total', () async {
      final p = await backend.loadProgress();
      expect(p.map((e) => [e.label, e.done, e.total, e.text]), [['a', 3, 10, '3/10'], ['b', 10, 10, '10/10']]);
      expect(p.first.fraction, closeTo(0.3, 1e-9));
      expect(p.last.fraction, 1);
    });

    test('DSH-12.d: a file whose content is not done/total shows no bar, and a file without the .progress ending is not read', () async {
      expect((await backend.loadProgress()).map((e) => e.label), isNot(anyOf(contains('bad'), contains('notes'))));
      expect(files.reads, isNot(contains('/prog/notes.txt')));
    });

    test('DSH-12.b: with no progress folder, a missing one, or one without a progress file the list is empty', () async {
      expect(await LocalBackend(files: files, runner: runner, repoRoot: memRoot).loadProgress(), isEmpty);
      expect(await LocalBackend(files: files, runner: runner, repoRoot: memRoot, progressDir: '/nowhere').loadProgress(), isEmpty);
      expect(await LocalBackend(files: MemoryFileAccess({'/prog/notes.txt': 'x'}), runner: runner, repoRoot: memRoot, progressDir: '/prog').loadProgress(), isEmpty);
    });

    test('DSH-12.c: every call reads the files again (the page calls it at the interval and on Reload)', () async {
      expect((await backend.loadProgress()).first.done, 3);
      files.files['/prog/a.progress'] = '7/10';
      files.files['/prog/c.progress'] = '1/1';
      final again = await backend.loadProgress();
      expect(again.map((e) => e.label), ['a', 'b', 'c']);
      expect(again.first.done, 7);
      files.files.remove('/prog/b.progress');
      expect((await backend.loadProgress()).map((e) => e.label), ['a', 'c']);
    });
  });

  group('usage text and reload (DSH-14.g, DSH-01.c)', () {
    test('DSH-14.g: a missing usage file is null', () async {
      expect(await backend.loadUsage(), isNull);
    });

    test('DSH-14.g: the usage file is read from SCRUM.d/usage.md', () async {
      files.files[memUsagePath] = 'text';
      expect(await backend.loadUsage(), 'text');
    });

    test('DSH-01.c: loading again reads the sprint file, the requirement files, the issues and the progress again', () async {
      final r = MutableRunner(CommandResult(exitCode: 0, stdout: issuesJson([issueJson(1, 'One')])));
      final b = LocalBackend(files: files, runner: r, repoRoot: memRoot, progressDir: '/prog');
      expect((await b.loadIssues()).map((i) => i.title), ['One']);
      r.result = CommandResult(exitCode: 0, stdout: issuesJson([issueJson(1, 'One'), issueJson(2, 'Two')]));
      files.files[memSprintPath] = SprintFileWithOneBlock.text;
      files.files['$memRequirementsDir/alpha.md'] = reqFile(['| AAA-01 | done | Changed. | — | — |']);
      files.files['/prog/a.progress'] = '9/10';
      expect((await b.loadIssues()).map((i) => i.title), ['One', 'Two']);
      expect((await b.loadSprint()).blocks.map((x) => x.id), ['story-9']);
      expect((await b.loadRequirements()).firstWhere((x) => x.id == 'AAA-01').statement, 'Changed.');
      expect((await b.loadProgress()).first.done, 9);
    });
  });

  group('what the dashboard changes (DSH-01.a)', () {
    test('DSH-01.a: a whole session of changes writes only the sprint file and requirement files, and runs only the tracker commands', () async {
      await backend.saveSprint(SprintEdit.addMember(await backend.loadSprint(), 'story-2', 'AAA-02'));
      await backend.setRequirementStatus('AAA-02', Status.planned);
      await backend.setIssueStatus(5, Status.planned);
      await backend.createIssue(const NewIssue(title: 'T'));
      await backend.loadIssues();
      await backend.loadProgress();
      await backend.loadUsage();
      expect(files.writes, [memSprintPath]);
      expect(files.atomicWrites, hasLength(1));
      expect(files.atomicWrites.single, startsWith('$memRequirementsDir/'));
      for (final c in runner.calls) {
        expect(c.first, 'gh');
        expect(['label', 'issue'], contains(c[1]));
      }
      expect(files.files.keys.where((k) => k.startsWith('/prog/')).length, 4, reason: 'the progress folder gains and loses nothing');
    });
  });
}

class SprintFileWithOneBlock {
  static const text = '## Blocks\n\n| id | kind | name | parent | assignee | estimate | usage |\n|---|---|---|---|---|---|---|\n| story-9 | story | Nine |  |  | 1 | 0 |\n';
}
