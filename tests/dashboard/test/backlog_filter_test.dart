// Tests DSH-03.b, DSH-05.c (backlog drops what the sprint names), DSH-04 (filter logic, a-d).
// One run covers each ID named in the test name.
import 'package:dashboard/features/dashboard/domain/backlog.dart';
import 'package:dashboard/features/dashboard/domain/issue.dart';
import 'package:dashboard/features/dashboard/domain/list_filter.dart';
import 'package:dashboard/features/dashboard/domain/requirement.dart';
import 'package:dashboard/features/dashboard/domain/sprint.dart';
import 'package:dashboard/features/dashboard/domain/story.dart';
import 'package:flutter_test/flutter_test.dart';

Requirement req(String id, String status, String feature) =>
    Requirement(id: id, status: status, statement: 's $id', feature: feature);
Issue iss(int n, IssueStatus s, {String? feature, String? requirement}) =>
    Issue(number: n, title: 't$n', status: s, feature: feature, requirement: requirement);

void main() {
  final reqs = [req('AAA-01', 'proposed', 'alpha'), req('AAA-02', 'backlog', 'alpha'), req('BBB-01', 'backlog', 'beta')];

  test('DSH-03.b: a requirement named in a story items is not in the backlog', () {
    const sprint = Sprint(stories: [Story(id: 'S-1', title: 'x', items: ['AAA-01'])]);
    expect(Backlog.requirements(reqs, sprint).map((r) => r.id), ['AAA-02', 'BBB-01']);
  });

  test('DSH-03.b: a requirement that is a story id is not in the backlog', () {
    const sprint = Sprint(stories: [Story(id: 'BBB-01', title: 'x')]);
    expect(Backlog.requirements(reqs, sprint).map((r) => r.id), ['AAA-01', 'AAA-02']);
  });

  test('DSH-03.b: an empty sprint leaves every requirement in the backlog', () {
    expect(Backlog.requirements(reqs, const Sprint()), hasLength(3));
  });

  test('DSH-05.c: an issue written #N in story items is not in the backlog; others stay', () {
    const sprint = Sprint(stories: [Story(id: 'S-1', title: 'x', items: ['AAA-01', '#7'])]);
    final issues = [iss(7, IssueStatus.open), iss(8, IssueStatus.open), iss(70, IssueStatus.open)];
    expect(Backlog.issues(issues, sprint).map((i) => i.number), [8, 70]);
  });

  final base = [
    (f: 'alpha', id: 'AAA-01', s: 'proposed'),
    (f: 'alpha', id: 'AAA-02', s: 'backlog'),
    (f: 'beta', id: 'BBB-01', s: 'backlog'),
    (f: null, id: null, s: 'backlog'),
  ];
  List<String?> run(ListFilter f) =>
      f.apply(base, feature: (e) => e.f, requirementId: (e) => e.id, status: (e) => e.s).map((e) => e.id).toList();

  test('DSH-04: the start filter (All, empty text, All) keeps everything', () {
    expect(run(const ListFilter()), hasLength(4));
  });

  test('DSH-04.a: the feature filter keeps only the chosen feature', () {
    expect(run(const ListFilter(feature: 'beta')), ['BBB-01']);
  });

  test('DSH-04.b: the requirement text matches an ID substring, ignoring case', () {
    expect(run(const ListFilter(requirement: 'aaa-0')), ['AAA-01', 'AAA-02']);
    expect(run(const ListFilter(requirement: 'B-01')), ['BBB-01']);
  });

  test('DSH-04.c: the status filter keeps only the chosen status', () {
    expect(run(const ListFilter(status: 'proposed')), ['AAA-01']);
  });

  test('DSH-04.c: choices are the sorted distinct non-null values', () {
    expect(ListFilter.choices(['b', null, 'a', 'b']), ['a', 'b']);
  });

  test('DSH-04.d: the three filters combine; an entry must meet all', () {
    expect(run(const ListFilter(feature: 'alpha', requirement: 'aaa', status: 'backlog')), ['AAA-02']);
    expect(run(const ListFilter(feature: 'beta', requirement: 'aaa')), isEmpty);
  });

  test('DSH-04.d: matches agrees with apply', () {
    const f = ListFilter(feature: 'alpha', status: 'backlog');
    expect(f.matches(feature: 'alpha', requirementId: 'X', status: 'backlog'), isTrue);
    expect(f.matches(feature: 'beta', requirementId: 'X', status: 'backlog'), isFalse);
    expect(f.matches(feature: 'alpha', requirementId: 'X', status: 'done'), isFalse);
  });
}
