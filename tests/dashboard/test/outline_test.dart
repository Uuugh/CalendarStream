// Tests the outline of the Requirements column as a pure function (RequirementOutline): DSH-11 (sub-requirements
// beneath their requirement), DSH-11.a (depth and the indent constant), DSH-11.b (which requirements have a triangle and
// its direction), DSH-11.c (expand all, collapse all), DSH-11.d (all collapsed at the start), DSH-11.e (built from the
// listed entries). Drawing the triangle and the switch is a page test and is not here. One run covers each ID named.
import 'package:dashboard/features/dashboard/domain/dashboard_limits.dart';
import 'package:dashboard/features/dashboard/domain/outline_row.dart';
import 'package:dashboard/features/dashboard/domain/requirement.dart';
import 'package:dashboard/features/dashboard/domain/requirement_outline.dart';
import 'package:dashboard/features/dashboard/domain/status.dart';
import 'package:flutter_test/flutter_test.dart';

Requirement r(String id) => Requirement(id: id, status: Status.backlog, statement: 's', feature: id.split('-').first.toLowerCase());

final all = [r('AAA-01'), r('AAA-01.a'), r('AAA-01.b'), r('AAA-01.b.x'), r('AAA-02'), r('BBB-01'), r('BBB-01.a')];

List<String> ids(List<OutlineRow> rows) => [for (final x in rows) x.requirement.id];
List<int> depths(List<OutlineRow> rows) => [for (final x in rows) x.depth];

void main() {
  test('DSH-11: the parent of an ID is the text before its last dot; an ID with no dot has none', () {
    expect(RequirementOutline.parentOf('ACC-06.a'), 'ACC-06');
    expect(RequirementOutline.parentOf('ACC-06.a.b'), 'ACC-06.a');
    expect(RequirementOutline.parentOf('ACC-06'), isNull);
  });

  test('DSH-11.d: with nothing expanded only the requirements show, each at depth 0 (everything collapsed when the page opens)', () {
    final rows = RequirementOutline.rows(all, const {});
    expect(ids(rows), ['AAA-01', 'AAA-02', 'BBB-01']);
    expect(depths(rows), [0, 0, 0]);
    expect(rows.every((x) => !x.expanded), isTrue);
  });

  test('DSH-11: an expanded requirement is followed by its sub-requirements, in listed order, one level deeper (DSH-11.a)', () {
    final rows = RequirementOutline.rows(all, {'AAA-01'});
    expect(ids(rows), ['AAA-01', 'AAA-01.a', 'AAA-01.b', 'AAA-02', 'BBB-01']);
    expect(depths(rows), [0, 1, 1, 0, 0]);
  });

  test('DSH-11.a: sub-sub-requirements are one level deeper again, once their parent is expanded too', () {
    final rows = RequirementOutline.rows(all, {'AAA-01', 'AAA-01.b'});
    expect(ids(rows), ['AAA-01', 'AAA-01.a', 'AAA-01.b', 'AAA-01.b.x', 'AAA-02', 'BBB-01']);
    expect(depths(rows), [0, 1, 1, 2, 0, 0]);
  });

  test('DSH-11.a: the indent is the sub-requirement indent of DEF-01, 3 characters of the body text', () {
    expect(DashboardLimits.subRequirementIndent, 3);
  });

  test('DSH-11.b: a requirement with listed sub-requirements has a triangle, one without has none', () {
    final rows = RequirementOutline.rows(all, const {});
    expect({for (final x in rows) x.requirement.id: x.hasChildren}, {'AAA-01': true, 'AAA-02': false, 'BBB-01': true});
    final open = RequirementOutline.rows(all, {'AAA-01'});
    expect({for (final x in open) x.requirement.id: x.hasChildren}['AAA-01.a'], isFalse);
    expect({for (final x in open) x.requirement.id: x.hasChildren}['AAA-01.b'], isTrue);
  });

  test('DSH-11.b: the triangle points down exactly when the requirement is expanded and right when it is collapsed', () {
    final rows = RequirementOutline.rows(all, {'AAA-01'});
    final byId = {for (final x in rows) x.requirement.id: x};
    expect(byId['AAA-01']!.expanded, isTrue);
    expect(byId['BBB-01']!.expanded, isFalse);
    expect(byId['AAA-02']!.expanded, isFalse, reason: 'no children: never expanded');
    expect(RequirementOutline.rows(all, {'AAA-02'}).firstWhere((x) => x.requirement.id == 'AAA-02').expanded, isFalse);
  });

  test('DSH-11.b: parents lists the listed requirements that have a listed sub-requirement, in listed order', () {
    expect(RequirementOutline.parents(all), ['AAA-01', 'AAA-01.b', 'BBB-01']);
    expect(RequirementOutline.parents([r('AAA-01'), r('AAA-02')]), isEmpty);
  });

  test('DSH-11.c: expanding all (every parent) shows every entry; collapsing all shows only the top level', () {
    expect(ids(RequirementOutline.rows(all, RequirementOutline.parents(all).toSet())).toSet(), all.map((x) => x.id).toSet());
    expect(RequirementOutline.rows(all, const {}).length, 3);
  });

  test('DSH-11.e: a sub-requirement whose requirement is not listed is listed on its own at depth 0', () {
    final listed = [r('AAA-01.a'), r('AAA-02'), r('BBB-01'), r('BBB-01.a')];
    final rows = RequirementOutline.rows(listed, {'BBB-01'});
    expect(ids(rows), ['AAA-01.a', 'AAA-02', 'BBB-01', 'BBB-01.a']);
    expect(depths(rows), [0, 0, 0, 1]);
    expect(rows.first.hasChildren, isFalse);
  });

  test('DSH-11.e: filtering the requirement out of the list turns its sub-requirements into top-level rows', () {
    final listed = [for (final x in all) if (x.id != 'AAA-01') x];
    final rows = RequirementOutline.rows(listed, RequirementOutline.parents(listed).toSet());
    expect(depths(rows.where((x) => x.requirement.id.startsWith('AAA-01')).toList()), [0, 0, 1], reason: 'AAA-01.a and AAA-01.b stand alone; AAA-01.b.x sits under AAA-01.b');
  });

  test('DSH-11: an empty list gives no rows; nothing is lost or repeated when everything is expanded', () {
    expect(RequirementOutline.rows(const [], const {}), isEmpty);
    final rows = RequirementOutline.rows(all, RequirementOutline.parents(all).toSet());
    expect(ids(rows).toSet(), hasLength(all.length));
    expect(rows, hasLength(all.length));
  });
}
