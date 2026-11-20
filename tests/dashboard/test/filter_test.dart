// Tests the filter logic of DSH-04 (MultiFilter, the choices of each filter, the stored selection) and the form's
// dropdown logic of DSH-09.a. One run covers each ID named in the test name.
import 'dart:io';

import 'package:dashboard/features/dashboard/data/file_filter_store.dart';
import 'package:dashboard/features/dashboard/domain/multi_filter.dart';
import 'package:dashboard/features/dashboard/domain/requirement.dart';
import 'package:dashboard/features/dashboard/domain/requirement_choices.dart';
import 'package:dashboard/features/dashboard/domain/status.dart';
import 'package:flutter_test/flutter_test.dart';

class _Item {
  const _Item(this.feature, this.requirement, this.status);
  final String? feature;
  final String? requirement;
  final String status;
}

const items = [
  _Item('alpha', 'AAA-01', 'proposed'),
  _Item('alpha', 'AAA-02', 'backlog'),
  _Item('beta', 'BBB-01', 'backlog'),
  _Item('beta', 'BBB-01', 'done'),
  _Item(null, null, 'backlog'),
];

const reqs = [
  Requirement(id: 'AAA-01', status: Status.proposed, statement: 's', feature: 'alpha'),
  Requirement(id: 'AAA-02', status: Status.backlog, statement: 's', feature: 'alpha'),
  Requirement(id: 'BBB-01', status: Status.backlog, statement: 's', feature: 'beta'),
];

void main() {
  const choices = ['a', 'b', 'c'];

  group('MultiFilter (DSH-04)', () {
    test('DSH-04: a new filter has every choice selected and is not active', () {
      final f = MultiFilter(choices);
      expect(f.selectedList, choices);
      expect(f.isActive, isFalse);
      expect(f.matches('a'), isTrue);
      expect(f.matches(null), isTrue, reason: 'an entry with no value is listed while nothing is filtered');
    });

    test('DSH-04: only selects one choice, and the filter is active', () {
      final f = MultiFilter(choices).only('b');
      expect(f.selectedList, ['b']);
      expect(f.isActive, isTrue);
      expect(f.matches('b'), isTrue);
      expect(f.matches('a'), isFalse);
      expect(f.matches(null), isFalse, reason: 'an entry with no value is not listed while filtering');
      expect(MultiFilter(choices).only('zzz').selectedList, isEmpty);
    });

    test('DSH-04: several choices can be selected by toggling, and toggling again removes one', () {
      var f = MultiFilter(choices).selectNone().toggle('a').toggle('c');
      expect(f.selectedList, ['a', 'c']);
      expect(f.isSelected('b'), isFalse);
      f = f.toggle('a');
      expect(f.selectedList, ['c']);
      expect(f.toggle('zzz').selectedList, ['c'], reason: 'an unknown choice changes nothing');
    });

    test('DSH-04: select all and select none', () {
      final none = MultiFilter(choices).selectNone();
      expect(none.selectedList, isEmpty);
      expect(none.isActive, isTrue);
      expect(none.apply(items, (i) => i.status), isEmpty);
      final all = none.selectAll();
      expect(all.selectedList, choices);
      expect(all.isActive, isFalse);
    });

    test('DSH-04: the filter is active exactly when some choice is not selected', () {
      expect(MultiFilter(choices).toggle('a').isActive, isTrue);
      expect(MultiFilter(choices).toggle('a').toggle('a').isActive, isFalse);
      expect(MultiFilter(<String>[]).isActive, isFalse);
    });

    test('DSH-04: restore selects all when nothing was stored, keeps the stored choices, drops the unknown ones', () {
      expect(MultiFilter.restore(choices, null).selectedList, choices);
      expect(MultiFilter.restore(choices, ['c', 'a', 'gone']).selectedList, ['a', 'c']);
      expect(MultiFilter.restore(choices, []).selectedList, isEmpty);
      expect(MultiFilter.restore(choices, ['a']).isActive, isTrue);
    });

    test('DSH-04: new choices are selected while the filter was not active, and stay unselected otherwise', () {
      expect(MultiFilter(choices).withChoices(['a', 'b', 'c', 'd']).selectedList, ['a', 'b', 'c', 'd']);
      expect(MultiFilter(choices).only('a').withChoices(['a', 'b', 'c', 'd']).selectedList, ['a']);
      expect(MultiFilter(choices).only('a').withChoices(['b', 'c']).selectedList, isEmpty, reason: 'a choice that is gone is dropped');
    });

    test('DSH-04: the selected list keeps the order of the choices', () {
      expect(MultiFilter(choices).selectNone().toggle('c').toggle('a').selectedList, ['a', 'c']);
    });
  });

  group('the three filters combined and the count (DSH-04.d)', () {
    List<_Item> shown(MultiFilter feature, MultiFilter requirement, MultiFilter status) =>
        status.apply(requirement.apply(feature.apply(items, (i) => i.feature), (i) => i.requirement), (i) => i.status);

    final features = RequirementChoices.features(reqs);
    final ids = ['AAA-01', 'AAA-02', 'BBB-01'];
    final statuses = [for (final s in Status.values) s.name];

    test('DSH-04.d: with nothing filtered every entry is listed: shown equals total', () {
      expect(shown(MultiFilter(features), MultiFilter(ids), MultiFilter(statuses)), hasLength(items.length));
    });

    test('DSH-04.d: an entry is listed when it meets all three filters', () {
      final out = shown(MultiFilter(features).only('beta'), MultiFilter(ids), MultiFilter(statuses).only('done'));
      expect(out.map((i) => '${i.requirement}/${i.status}'), ['BBB-01/done']);
    });

    test('DSH-04.d: one filter that matches nothing lists nothing; the count is shown out of all', () {
      final out = shown(MultiFilter(features).only('alpha'), MultiFilter(ids).only('BBB-01'), MultiFilter(statuses));
      expect(out, isEmpty);
      expect('${out.length} of ${items.length}', '0 of 5');
    });

    test('DSH-04.d: several selected values in one filter are or-ed, the filters are and-ed', () {
      final out = shown(MultiFilter(features), MultiFilter(ids), MultiFilter(statuses).selectNone().toggle('backlog').toggle('proposed'));
      expect(out, hasLength(4));
      final both = shown(MultiFilter(features).only('alpha'), MultiFilter(ids), MultiFilter(statuses).selectNone().toggle('backlog').toggle('proposed'));
      expect(both.map((i) => i.requirement), ['AAA-01', 'AAA-02']);
    });
  });

  group('the choices of each filter', () {
    test('DSH-04.a: the feature choices are the features of what the column lists, once each', () {
      expect(RequirementChoices.features(reqs), ['alpha', 'beta']);
      expect(RequirementChoices.features(const []), isEmpty);
    });

    test('DSH-04.b: the requirement choices are the requirement IDs of the chosen feature', () {
      expect(RequirementChoices.requirementsOf(reqs, 'alpha'), ['AAA-01', 'AAA-02']);
      expect(RequirementChoices.requirementsOf(reqs, 'beta'), ['BBB-01']);
    });

    test('DSH-04.c and DSH-09.b: the status choices are the four statuses', () {
      expect([for (final s in Status.values) s.name], ['proposed', 'backlog', 'planned', 'done']);
    });

    test('DSH-09.a: with no feature chosen the requirement dropdown is empty, and choosing another feature clears the requirement', () {
      expect(RequirementChoices.requirementsOf(reqs, null), isEmpty);
      expect(RequirementChoices.keepRequirement(reqs, 'alpha', 'AAA-01'), 'AAA-01');
      expect(RequirementChoices.keepRequirement(reqs, 'beta', 'AAA-01'), isNull);
      expect(RequirementChoices.keepRequirement(reqs, null, 'AAA-01'), isNull);
    });
  });

  group('FileFilterStore (the stored selection of DSH-04)', () {
    late Directory dir;
    late String path;
    setUp(() {
      dir = Directory.systemTemp.createTempSync('dsh_filters_');
      path = '${dir.path}/filters.json';
    });
    tearDown(() => dir.deleteSync(recursive: true));

    test('DSH-04: a value set is read back, per key; an unknown key and a missing file give null', () {
      final s = FileFilterStore(path: path);
      expect(s.get('feature'), isNull);
      s.set('feature', ['alpha', 'beta']);
      s.set('status', ['done']);
      expect(FileFilterStore(path: path).get('feature'), ['alpha', 'beta']);
      expect(FileFilterStore(path: path).get('status'), ['done']);
      expect(s.get('nothing'), isNull);
    });

    test('DSH-04: a damaged file reads as nothing stored', () {
      File(path).writeAsStringSync('{not json');
      expect(FileFilterStore(path: path).get('feature'), isNull);
    });
  });
}
