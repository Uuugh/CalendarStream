// Tests DSH-04.e: a filter shows the value that is applied, even when no entry has it, and it can be changed.
// One run covers each ID named in the test name.
import 'package:dashboard/features/dashboard/domain/list_filter.dart';
import 'package:dashboard/features/dashboard/ui/list_filter_bar.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import '../support/page_harness.dart';

void main() {
  late List<ListFilter> changes;

  Future<void> pump(WidgetTester t, ListFilter filter) async {
    changes = [];
    bigView(t, size: const Size(1600, 600));
    await t.pumpWidget(testApp(Scaffold(
      body: ListFilterBar(
        filter: filter,
        onChanged: changes.add,
        features: const ['alpha', 'beta'],
        statuses: const ['backlog', 'proposed'],
        statusLabel: (s) => s,
        shown: 0,
        total: 2,
      ),
    )));
    await t.pumpAndSettle();
  }

  testWidgets('DSH-04.e: an applied feature that no entry has is shown and offered', (t) async {
    await pump(t, const ListFilter(feature: 'zeta'));
    expect(find.text('zeta'), findsOneWidget);
    await t.tap(find.text('zeta'));
    await t.pumpAndSettle();
    expect(find.text('zeta'), findsWidgets);
    expect(find.text('alpha'), findsOneWidget);
  });

  testWidgets('DSH-04.e: an applied status that no entry has is shown, and can be changed', (t) async {
    await pump(t, const ListFilter(status: 'done'));
    expect(find.text('done'), findsOneWidget);
    await t.tap(find.text('done'));
    await t.pumpAndSettle();
    await t.tap(find.text('proposed').last);
    await t.pumpAndSettle();
    expect(changes.single.status, 'proposed');
  });

  testWidgets('DSH-04.e: an applied feature that an entry has is shown too, and All is shown at the start', (t) async {
    await pump(t, const ListFilter(feature: 'beta'));
    expect(find.text('beta'), findsOneWidget);
    await pump(t, const ListFilter());
    expect(find.text('All'), findsNWidgets(2));
  });
}
