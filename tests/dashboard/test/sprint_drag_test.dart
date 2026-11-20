// Tests DSH-07 a-d on the page: drag from the backlog to a column, between columns, back to the backlog area,
// onto its own column, and the saved sprint file. Uses an in-memory FileAccess. One run covers each ID named.
import 'package:dashboard/features/dashboard/data/command_result.dart';
import 'package:dashboard/features/dashboard/data/issue_service.dart';
import 'package:dashboard/features/dashboard/data/requirement_repository.dart';
import 'package:dashboard/features/dashboard/data/sprint_repository.dart';
import 'package:dashboard/features/dashboard/ui/dashboard_page.dart';
import 'package:dashboard/l10n/app_localizations.dart';
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_test/flutter_test.dart';

import '../support/fixtures.dart';
import '../support/memory_file_access.dart';

const sprintPath = '/r/SCRUM.d/sprint.md';

const startSprint = '''# Sprint

Goal: Drag goal

## Stories

| story | title | items | stage | assignee | estimate | usage |
|---|---|---|---|---|---|---|
| S-1 | Named story | BBB-01 | Build | Ann | 3 | 1 |

## Review

Keep this review.

## Retrospective

Keep this retro.
''';

void main() {
  late MemoryFileAccess files;

  Future<void> pump(WidgetTester t) async {
    files = MemoryFileAccess({
      sprintPath: startSprint,
      '/r/requirements/alpha.md': reqFile(['| AAA-01 | backlog | Alpha one. | — | — |']),
      '/r/requirements/beta.md': reqFile(['| BBB-01 | backlog | Beta one. | — | — |']),
    });
    t.view.physicalSize = const Size(2400, 1800);
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.reset);
    await t.pumpWidget(MaterialApp(
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: AppLocalizations.supportedLocales,
      home: DashboardPage(
        sprints: SprintRepository(files: files, path: sprintPath),
        requirements: RequirementRepository(files: files, directory: '/r/requirements'),
        issues: IssueService(runner: FakeRunner(CommandResult(exitCode: 0, stdout: issuesJson([issueJson(12, 'Issue twelve')])))),
      ),
    ));
    await t.pumpAndSettle();
  }

  Future<void> dragTo(WidgetTester t, Finder from, Finder to, {Offset shift = Offset.zero}) async {
    final g = await t.startGesture(t.getCenter(from));
    await g.moveBy(const Offset(0, 20));
    await t.pump();
    await g.moveTo(t.getCenter(to) + shift);
    await t.pump();
    await g.up();
    await t.pumpAndSettle();
  }

  testWidgets('DSH-07.a: dropping a requirement on a column adds a story there, saves it, and the item leaves the backlog', (t) async {
    await pump(t);
    expect(find.byKey(const Key('backlog-item-AAA-01')), findsOneWidget);
    await dragTo(t, find.byKey(const Key('backlog-item-AAA-01')), find.byKey(const Key('column-ready')));
    expect(find.byKey(const Key('card-AAA-01')), findsOneWidget);
    expect(find.byKey(const Key('backlog-item-AAA-01')), findsNothing);
    final saved = files.files[sprintPath]!;
    expect(RegExp(r'\| AAA-01 \| .* \| Ready \|').hasMatch(saved), isTrue, reason: saved);
    expect(saved, contains('Keep this review.'));
    expect(saved, contains('Keep this retro.'));
    expect(saved, contains('Goal: Drag goal'));
  });

  testWidgets('DSH-07.a: dropping an issue adds a story with id #12', (t) async {
    await pump(t);
    await dragTo(t, find.byKey(const Key('backlog-item-#12')), find.byKey(const Key('column-test')));
    expect(find.byKey(const Key('card-#12')), findsOneWidget);
    expect(find.byKey(const Key('backlog-item-#12')), findsNothing);
    expect(RegExp(r'\| #12 \| .* \| Test \|').hasMatch(files.files[sprintPath]!), isTrue, reason: files.files[sprintPath]);
  });

  testWidgets('DSH-07.b: dropping a card on another column changes its stage and saves', (t) async {
    await pump(t);
    await dragTo(t, find.byKey(const Key('card-S-1')), find.byKey(const Key('column-review')));
    expect(RegExp(r'\| S-1 \| Named story \| BBB-01 \| Review \|').hasMatch(files.files[sprintPath]!), isTrue, reason: files.files[sprintPath]);
  });

  testWidgets('DSH-07.c: dropping a card on the backlog area removes the story and the item returns', (t) async {
    await pump(t);
    expect(find.byKey(const Key('backlog-item-BBB-01')), findsNothing);
    await dragTo(t, find.byKey(const Key('card-S-1')), find.byKey(const Key('backlog-area')));
    expect(find.byKey(const Key('card-S-1')), findsNothing);
    expect(find.byKey(const Key('backlog-item-BBB-01')), findsOneWidget);
    expect(files.files[sprintPath]!, isNot(contains('S-1')));
    expect(files.files[sprintPath]!, contains('Keep this review.'));
  });

  testWidgets('DSH-07.d: dropping a card on its own column writes nothing', (t) async {
    await pump(t);
    final before = files.files[sprintPath];
    await dragTo(t, find.byKey(const Key('card-S-1')), find.byKey(const Key('column-build')), shift: const Offset(0, 200));
    expect(files.files[sprintPath], before);
    expect(find.byKey(const Key('card-S-1')), findsOneWidget);
  });
}
