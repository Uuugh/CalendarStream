// Tests DSH-03.a (read every requirement row, with ID, status, statement, feature) and
// the DSH-03 base fields. One run covers each ID named in the test name.
// DSH-03.b and DSH-03.c are tested in backlog_filter_test.dart and dashboard_page_test.dart.
import 'dart:io';

import 'package:dashboard/features/dashboard/data/requirement_repository.dart';
import 'package:flutter_test/flutter_test.dart';

import '../support/fixtures.dart';

void main() {
  late Directory repo;
  setUp(() => repo = makeRepo());
  tearDown(() => repo.deleteSync(recursive: true));

  Future<List<dynamic>> load() async =>
      RequirementRepository(files: disk, directory: makeRequirements(repo)).load();

  test('DSH-03.a: rows of a feature file are read', () async {
    final ids = (await load()).map((r) => r.id).toList();
    expect(ids, containsAll(['AAA-01', 'AAA-02']));
  });

  test('DSH-03.a: rows of connections.d and plugins.d files are read', () async {
    final ids = (await load()).map((r) => r.id).toList();
    expect(ids, containsAll(['BBB-01', 'GGG-01']));
  });

  test('DSH-03.a: README, oldkey.md and open-questions.md hold no requirements', () async {
    final ids = (await load()).map((r) => r.id).toList();
    expect(ids, isNot(contains('RDM-01')));
    expect(ids, isNot(contains('OLD-01')));
    expect(ids, isNot(contains('OQ-01')));
    expect(ids, isNot(contains('CRD-01')));
    expect(ids, hasLength(4));
  });

  test('DSH-03: each requirement has ID, status, statement and feature', () async {
    final r = (await load()).firstWhere((r) => r.id == 'BBB-01');
    expect(r.status, 'backlog');
    expect(r.statement, 'Beta one.');
    expect(r.feature, 'beta');
    final g = (await load()).firstWhere((r) => r.id == 'GGG-01');
    expect(g.status, 'done');
    expect(g.feature, 'gamma');
  });

  test('DSH-03: feature is the file name without .md', () async {
    final r = (await load()).firstWhere((r) => r.id == 'AAA-01');
    expect(r.feature, 'alpha');
    expect(r.status, 'proposed');
    expect(r.statement, 'Alpha one.');
  });

  test('DSH-03: a blank status counts as backlog', () async {
    final r = (await load()).firstWhere((r) => r.id == 'AAA-02');
    expect(r.status, 'backlog');
  });
}
