// Tests DSH-06 a-d (header counts, card content, column colors, assignee dot) and DSH-07 b-d at the widget level
// (drag between columns, onto its own column), with the board alone. One run covers each ID named in the test name.
import 'package:dashboard/features/dashboard/domain/sprint.dart';
import 'package:dashboard/features/dashboard/domain/stage.dart';
import 'package:dashboard/features/dashboard/domain/story.dart';
import 'package:dashboard/features/dashboard/ui/assignee_colors.dart';
import 'package:dashboard/features/dashboard/ui/assignee_dot.dart';
import 'package:dashboard/features/dashboard/ui/sprint_board.dart';
import 'package:dashboard/features/dashboard/ui/stage_colors.dart';
import 'package:dashboard/theme/app_theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import '../support/page_harness.dart';

const sprint = Sprint(goal: 'Board goal', stories: [
  Story(id: 'S-1', title: 'First story', stage: Stage.build, assignee: 'Ann', estimate: 3),
  Story(id: 'S-2', title: 'Second story', stage: Stage.build, assignee: 'Ann', estimate: 2),
  Story(id: 'S-3', title: 'Third story', stage: Stage.done, assignee: 'Bob', estimate: 1),
  Story(id: 'S-4', title: 'Fourth story', stage: Stage.ready),
]);

void main() {
  final changes = <Sprint>[];
  setUp(changes.clear);

  Future<void> pump(WidgetTester t, {ThemeData? theme}) async {
    bigView(t, size: const Size(2400, 1200));
    await t.pumpWidget(testApp(Scaffold(body: SprintBoard(sprint: sprint, onChanged: changes.add)), theme: theme));
    await t.pumpAndSettle();
  }

  // Every color a column or a card shows: text, fills and borders.
  Set<int> colorsIn(WidgetTester t, Finder root) {
    final out = <int>{};
    void add(Color? c) {
      if (c != null) out.add(c.toARGB32() & 0xFFFFFF);
    }
    for (final e in find.descendant(of: root, matching: find.byType(DecoratedBox)).evaluate()) {
      final d = (e.widget as DecoratedBox).decoration;
      if (d is BoxDecoration) {
        add(d.color);
        final b = d.border;
        if (b is Border) {
          for (final side in [b.top, b.left, b.right, b.bottom]) {
            add(side.color);
          }
        }
      }
    }
    for (final e in find.descendant(of: root, matching: find.byType(Text)).evaluate()) {
      add((e.widget as Text).style?.color);
    }
    for (final e in find.descendant(of: root, matching: find.byType(Container)).evaluate()) {
      add((e.widget as Container).color);
    }
    void addShape(ShapeBorder? shape) {
      if (shape is OutlinedBorder) add(shape.side.color);
    }
    for (final e in find.descendant(of: root, matching: find.byType(Card)).evaluate()) {
      final c = e.widget as Card;
      add(c.color);
      addShape(c.shape);
    }
    for (final e in find.descendant(of: root, matching: find.byType(Material)).evaluate()) {
      final m = e.widget as Material;
      add(m.color);
      addShape(m.shape);
    }
    for (final e in find.descendant(of: root, matching: find.byType(Icon)).evaluate()) {
      add((e.widget as Icon).color);
    }
    return out;
  }

  testWidgets('DSH-06: the goal and six columns in stage order', (t) async {
    await pump(t);
    expect(find.textContaining('Board goal'), findsOneWidget);
    final xs = [for (final s in Stage.values) t.getTopLeft(find.byKey(Key('column-${s.name}'))).dx];
    expect(xs, orderedEquals([...xs]..sort()));
    expect(xs.toSet(), hasLength(6));
  });

  testWidgets('DSH-06.a: headers show the stage name and n / total', (t) async {
    await pump(t);
    const expected = {
      Stage.backlog: 'Backlog 0 / 4',
      Stage.ready: 'Ready 1 / 4',
      Stage.build: 'Build 2 / 4',
      Stage.test: 'Test 0 / 4',
      Stage.review: 'Review 0 / 4',
      Stage.done: 'Done 1 / 4',
    };
    for (final e in expected.entries) {
      final texts = find
          .descendant(of: find.byKey(Key('column-${e.key.name}')), matching: find.byType(Text))
          .evaluate()
          .map((x) => (x.widget as Text).data ?? (x.widget as Text).textSpan?.toPlainText() ?? '')
          .map((s) => s.replaceAll(RegExp(r'\s+'), ' ').trim());
      expect(texts, contains(e.value), reason: '${e.key.name}: $texts');
    }
  });

  testWidgets('DSH-06.b: a card shows id, estimate, title and the assignee dot', (t) async {
    await pump(t);
    final card = find.byKey(const Key('card-S-1'));
    expect(find.descendant(of: card, matching: find.text('S-1')), findsOneWidget);
    expect(find.descendant(of: card, matching: find.textContaining('3')), findsWidgets);
    expect(find.descendant(of: card, matching: find.text('First story')), findsOneWidget);
    expect(find.descendant(of: card, matching: find.byKey(const Key('assignee-dot-S-1'))), findsOneWidget);
  });

  testWidgets('DSH-06.c: each column has its own color from the theme, in light and dark, and its cards carry it', (t) async {
    for (final theme in [AppTheme.light, AppTheme.dark]) {
      await pump(t, theme: theme);
      final colors = {for (final s in Stage.values) s: StageColors.of(theme, s)};
      expect(colors.values.toSet(), hasLength(6), reason: 'one color for each stage');
      for (final e in colors.entries) {
        expect(colorsIn(t, find.byKey(Key('column-${e.key.name}'))), contains(e.value.toARGB32() & 0xFFFFFF), reason: 'column ${e.key.name}');
      }
      for (final c in {'S-1': Stage.build, 'S-3': Stage.done, 'S-4': Stage.ready}.entries) {
        expect(colorsIn(t, find.byKey(Key('card-${c.key}'))), contains(colors[c.value]!.toARGB32() & 0xFFFFFF), reason: 'card ${c.key}');
      }
    }
    expect({for (final s in Stage.values) StageColors.of(AppTheme.light, s)}, isNot(equals({for (final s in Stage.values) StageColors.of(AppTheme.dark, s)})));
  });

  testWidgets('DSH-06.d: same assignee same dot color from the theme, tooltip is the name, empty dot has no fill and says no assignee', (t) async {
    await pump(t);
    final theme = AppTheme.light;
    expect(AssigneeColors.of(theme, 'Ann'), AssigneeColors.of(theme, 'Ann'));
    // Distinct names need not differ (a palette can collide), but the palette must not be a single color.
    expect({for (final n in ['Ann', 'Bob', 'Cy', 'Di', 'Ed', 'Flo']) AssigneeColors.of(theme, n)}.length, greaterThan(1));
    expect(AssigneeColors.palette(AppTheme.light), isNot(equals(AssigneeColors.palette(AppTheme.dark))));
    Color? fill(String id) {
      final dot = find.byKey(Key('assignee-dot-$id'));
      final d = find
          .descendant(of: dot, matching: find.byType(DecoratedBox))
          .evaluate()
          .followedBy(dot.evaluate().where((e) => e.widget is DecoratedBox))
          .map((e) => (e.widget as DecoratedBox).decoration)
          .whereType<BoxDecoration>();
      return d.isEmpty ? null : d.first.color;
    }
    expect(fill('S-1'), isNotNull);
    expect(fill('S-1'), fill('S-2'));
    expect(fill('S-3'), AssigneeColors.of(theme, 'Bob'));
    expect(fill('S-1'), AssigneeColors.of(theme, 'Ann'));
    expect(fill('S-4'), isNull);
    final tips = find.descendant(of: find.byType(AssigneeDot), matching: find.byType(Tooltip)).evaluate().map((e) => (e.widget as Tooltip).message);
    expect(tips, containsAll(['Ann', 'Bob', 'No assignee']));
  });

  testWidgets('DSH-07.b: dropping a card on another column sets its stage', (t) async {
    await pump(t);
    await t.drag(find.byKey(const Key('card-S-1')), t.getCenter(find.byKey(const Key('column-review'))) - t.getCenter(find.byKey(const Key('card-S-1'))));
    await t.pumpAndSettle();
    expect(changes, hasLength(1));
    expect(changes.single.stories.firstWhere((s) => s.id == 'S-1').stage, Stage.review);
    expect(changes.single.stories, hasLength(4));
  });

  testWidgets('DSH-07.d: dropping a card on its own column does not call onChanged', (t) async {
    await pump(t);
    final from = t.getCenter(find.byKey(const Key('card-S-1')));
    await t.drag(find.byKey(const Key('card-S-1')), t.getCenter(find.byKey(const Key('column-build'))) + const Offset(0, 200) - from);
    await t.pumpAndSettle();
    expect(changes, isEmpty);
  });
}
