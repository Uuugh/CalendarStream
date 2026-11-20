// Tests reading the requirement files (DSH-03, DSH-03.a, DSH-03.b) and changing one row's status
// (DSH-13.d; DSH-07.d/e/f and DSH-08.a through the backend are in local_backend_test.dart).
// Reads only temp copies and in-memory files; the real requirements folder is read, never written.
// One run covers each ID named in the test name.
import 'dart:io';

import 'package:dashboard/features/dashboard/data/requirement_repository.dart';
import 'package:dashboard/features/dashboard/domain/requirement.dart';
import 'package:dashboard/features/dashboard/domain/status.dart';
import 'package:flutter_test/flutter_test.dart';

import '../support/fixtures.dart';
import '../support/memory_file_access.dart';

void main() {
  late MemoryFileAccess files;
  late RequirementRepository repo;
  setUp(() {
    files = MemoryFileAccess(memoryFiles());
    repo = RequirementRepository(files: files, directory: memRequirementsDir);
  });

  Future<Requirement> one(String id) async => (await repo.load()).firstWhere((r) => r.id == id);

  group('reading (DSH-03, DSH-03.a, DSH-03.b)', () {
    test('DSH-03.a: every row of a feature file is read', () async {
      final ids = (await repo.load()).map((r) => r.id);
      expect(ids, containsAll(['AAA-01', 'AAA-02', 'AAA-03', 'AAA-04', 'DDD-01']));
    });

    test('DSH-03.a: rows of the files in connections.d and plugins.d are read', () async {
      expect((await repo.load()).map((r) => r.id), containsAll(['BBB-01', 'GGG-01']));
    });

    test('DSH-03.a: the README, oldkey.md and open-questions.md hold no requirements, in any folder', () async {
      final ids = (await repo.load()).map((r) => r.id).toList();
      for (final skipped in ['RDM-01', 'OLD-01', 'OQ-01', 'CRD-01']) {
        expect(ids, isNot(contains(skipped)), reason: skipped);
      }
      expect(ids, hasLength(9));
    });

    test('DSH-03: a sub-requirement ID such as AAA-05.a is a row; the header row is not', () async {
      final ids = (await repo.load()).map((r) => r.id).toList();
      expect(ids, contains('AAA-05.a'));
      expect(ids, isNot(contains('ID')));
    });

    test('DSH-03: each requirement has ID, status, statement and feature (the file name without .md)', () async {
      final b = await one('BBB-01');
      expect([b.status, b.statement, b.feature], [Status.backlog, 'Beta one.', 'beta']);
      final g = await one('GGG-01');
      expect([g.status, g.feature], [Status.proposed, 'gamma']);
      final a = await one('AAA-01');
      expect([a.status, a.statement, a.feature], [Status.proposed, 'Alpha one.', 'alpha']);
    });

    test('DSH-03.b: a blank status counts as backlog, and a status is its first word', () async {
      expect((await one('AAA-02')).status, Status.backlog);
      expect((await one('AAA-03')).status, Status.planned);
      expect((await one('AAA-04')).status, Status.done);
    });

    test('DSH-03: a CRLF file is read the same as an LF file', () async {
      final d = await one('DDD-02');
      expect([d.status, d.statement, d.feature], [Status.proposed, 'Delta two.', 'delta']);
    });

    test('DSH-03: a requirement round trips through JSON', () async {
      final r = await one('AAA-03');
      final back = Requirement.fromJson(r.toJson());
      expect([back.id, back.status, back.statement, back.feature], [r.id, r.status, r.statement, r.feature]);
    });

    test('DSH-03.a: a folder or a file that is missing gives an empty list', () async {
      expect(await RequirementRepository(files: MemoryFileAccess(), directory: memRequirementsDir).load(), isEmpty);
    });

    test('DSH-03.a: the real requirements folder is read, with the connections and plugins parts, and its README rows are not', () async {
      final real = RequirementRepository(files: disk, directory: '../../requirements');
      final list = await real.load();
      final ids = list.map((r) => r.id).toSet();
      expect(ids, containsAll(['DSH-01', 'DSH-01.a', 'DSH-13.c']));
      expect(list.map((r) => r.feature), contains('dashboard'));
      final parts = Directory('../../requirements/connections.d')
          .listSync()
          .whereType<File>()
          .map((f) => f.path.replaceAll('\\', '/').split('/').last)
          .where((n) => n.endsWith('.md') && n != 'README.md')
          .map((n) => n.substring(0, n.length - 3));
      for (final p in parts) {
        expect(list.map((r) => r.feature), contains(p), reason: 'connections.d/$p.md');
      }
      expect(list.map((r) => r.feature), isNot(anyOf(contains('README'), contains('oldkey'), contains('open-questions'))));
      expect(list.where((r) => r.id == 'DSH-01').single.feature, 'dashboard');
    });
  });

  group('changing one row (DSH-13.d)', () {
    test('DSH-13.d: only the status cell of that row changes; every other line and cell stays as it was', () async {
      final path = '$memRequirementsDir/alpha.md';
      final before = files.files[path]!;
      expect(await repo.setStatus('AAA-01', Status.backlog), isTrue);
      final after = files.files[path]!;
      expect(after, before.replaceFirst('| AAA-01 | proposed | Alpha one. | — | — |', '| AAA-01 | backlog | Alpha one. | — | — |'));
      expect(after, isNot(before));
    });

    test('DSH-13.d: a blank status cell gets the status; a cell with extra words is replaced as a whole', () async {
      await repo.setStatus('AAA-02', Status.planned);
      await repo.setStatus('AAA-04', Status.done);
      final text = files.files['$memRequirementsDir/alpha.md']!;
      expect(text, contains('| AAA-02 | planned | Alpha two blank. | — | — |'));
      expect(text, contains('| AAA-04 | done | Alpha four. | — | — |'), reason: 'the old words in the status cell are replaced');
    });

    test('DSH-13.d: the row is found in a file of a .d folder and the other files are not touched', () async {
      final others = {for (final e in files.files.entries) if (!e.key.endsWith('beta.md')) e.key: e.value};
      await repo.setStatus('BBB-01', Status.planned);
      expect(files.files['$memRequirementsDir/connections.d/beta.md'], contains('| BBB-01 | planned | Beta one. | — | — |'));
      for (final e in others.entries) {
        expect(files.files[e.key], e.value, reason: e.key);
      }
    });

    test('DSH-13.d: the CRLF line endings of a file are kept, on every line', () async {
      final path = '$memRequirementsDir/delta.md';
      final before = files.files[path]!;
      await repo.setStatus('DDD-02', Status.backlog);
      final after = files.files[path]!;
      expect(after, before.replaceFirst('| DDD-02 | proposed |', '| DDD-02 | backlog |'));
      expect(after.split('\r\n').length, before.split('\r\n').length);
      expect(RegExp(r'(?<!\r)\n').hasMatch(after), isFalse, reason: 'no line ended with a bare LF');
    });

    test('DSH-13.d: the file is replaced with an atomic write, never a plain write', () async {
      await repo.setStatus('AAA-01', Status.planned);
      expect(files.atomicWrites, ['$memRequirementsDir/alpha.md']);
      expect(files.writes, isEmpty);
    });

    test('DSH-13.d: a row that is not found returns false and writes nothing; a status already set writes nothing', () async {
      expect(await repo.setStatus('ZZZ-99', Status.done), isFalse);
      expect(await repo.setStatus('AAA-01', Status.proposed), isTrue);
      expect(files.atomicWrites, isEmpty);
      expect(files.writes, isEmpty);
    });

    test('DSH-13.d: when the replacing write fails the file is exactly as it was', () async {
      final broken = _AtomicFails(files.files);
      final before = Map.of(broken.files);
      await expectLater(RequirementRepository(files: broken, directory: memRequirementsDir).setStatus('AAA-01', Status.done), throwsA(anything));
      expect(broken.files, before);
    });

    test('DSH-13.d: on a real disk the file is replaced as a whole and no temporary file is left behind', () async {
      final dir = makeRepo();
      addTearDown(() => dir.deleteSync(recursive: true));
      final reqDir = makeRequirements(dir);
      final p = '$reqDir/delta.md';
      final before = File(p).readAsStringSync();
      expect(await RequirementRepository(files: disk, directory: reqDir).setStatus('DDD-01', Status.planned), isTrue);
      expect(File(p).readAsStringSync(), before.replaceFirst('| DDD-01 | backlog |', '| DDD-01 | planned |'));
      final leftovers = Directory(reqDir).listSync(recursive: true).where((e) => e.path.endsWith('.tmp'));
      expect(leftovers, isEmpty);
    });

    test('DSH-13.d: withStatus changes only the named row and returns null when there is none', () {
      const text = '| ID | status | statement |\n|---|---|---|\n| X-01 | backlog | one |\n| X-02 | backlog | two |\n';
      expect(RequirementRepository.withStatus(text, 'X-02', Status.done),
          '| ID | status | statement |\n|---|---|---|\n| X-01 | backlog | one |\n| X-02 | done | two |\n');
      expect(RequirementRepository.withStatus(text, 'X-03', Status.done), isNull);
    });
  });
}

class _AtomicFails extends MemoryFileAccess {
  _AtomicFails(super.files);

  @override
  Future<void> writeAtomic(String path, String content) async => throw Exception('disk full');
}
