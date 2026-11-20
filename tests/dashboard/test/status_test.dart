// Tests the status model and its small pure rules. One run covers each ID named in the test name.
// DSH-03.b (parse, blank is backlog), DSH-05.a (status of an issue label), DSH-09.b (four statuses, default backlog),
// DSH-13.c (the status rule), DSH-07.g (a refusal has a reason), DSH-06.c (nesting rule), the DEF-01 values the rows cite
// (DSH-05.e, DSH-12.c, DSH-13.a, DSH-14.d, DSH-15.a, DSH-15.c).
import 'package:dashboard/features/dashboard/domain/block_kind.dart';
import 'package:dashboard/features/dashboard/domain/block_rules.dart';
import 'package:dashboard/features/dashboard/domain/dashboard_limits.dart';
import 'package:dashboard/features/dashboard/domain/new_issue.dart';
import 'package:dashboard/features/dashboard/domain/status.dart';
import 'package:dashboard/features/dashboard/domain/status_refused.dart';
import 'package:dashboard/features/dashboard/domain/status_rule.dart';
import 'package:dashboard/features/dashboard/server/dashboard_server_config.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('Status', () {
    test('DSH-03.b and DSH-09.b: there are exactly the four statuses, in this order', () {
      expect(Status.values.map((s) => s.name), ['proposed', 'backlog', 'planned', 'done']);
    });

    test('DSH-03.b: parse reads the first word, ignoring case and spaces', () {
      expect(Status.parse('proposed'), Status.proposed);
      expect(Status.parse('  Planned  '), Status.planned);
      expect(Status.parse('DONE'), Status.done);
      expect(Status.parse('done (see AAA-03)'), Status.done);
      expect(Status.parse('backlog extra words'), Status.backlog);
    });

    test('DSH-03.b: a blank, missing or unknown status counts as backlog', () {
      expect(Status.parse(''), Status.backlog);
      expect(Status.parse('   '), Status.backlog);
      expect(Status.parse(null), Status.backlog);
      expect(Status.parse('weird'), Status.backlog);
      expect(Status.parse('-'), Status.backlog);
    });

    test('DSH-05.a: tryName knows only the four names', () {
      expect(Status.tryName('planned'), Status.planned);
      expect(Status.tryName('feature:x'), isNull);
      expect(Status.tryName('Done'), isNull);
      expect(Status.tryName(null), isNull);
    });
  });

  group('StatusRule (DSH-13.c)', () {
    final order = Status.values;

    test('DSH-13.c: every move up the order is allowed, and staying is allowed', () {
      for (final from in order) {
        for (final to in order) {
          if (to.index >= from.index) {
            expect(StatusRule.refusal(from, to), isNull, reason: '${from.name} to ${to.name}');
          }
        }
      }
    });

    test('DSH-13.c: the only move down is planned to backlog', () {
      for (final from in order) {
        for (final to in order) {
          if (to.index < from.index) {
            final refused = StatusRule.refusal(from, to);
            if (from == Status.planned && to == Status.backlog) {
              expect(refused, isNull);
            } else {
              expect(refused, isNotNull, reason: '${from.name} to ${to.name}');
              expect(refused, contains(from.name));
              expect(refused, contains(to.name));
            }
          }
        }
      }
    });

    test('DSH-07.g and DSH-13.c: a refusal carries its reason as its text', () {
      const e = StatusRefused('no way');
      expect(e.reason, 'no way');
      expect('$e', 'no way');
    });
  });

  group('BlockRules (DSH-06.c)', () {
    test('DSH-06.c: a story sits in an epic, in a sprint or at the top', () {
      expect(BlockRules.canNest(BlockKind.story, BlockKind.epic), isTrue);
      expect(BlockRules.canNest(BlockKind.story, BlockKind.sprint), isTrue);
      expect(BlockRules.canNest(BlockKind.story, null), isTrue);
      expect(BlockRules.canNest(BlockKind.story, BlockKind.story), isFalse);
    });

    test('DSH-06.c: an epic sits in a sprint or at the top, never in a story or an epic', () {
      expect(BlockRules.canNest(BlockKind.epic, BlockKind.sprint), isTrue);
      expect(BlockRules.canNest(BlockKind.epic, null), isTrue);
      expect(BlockRules.canNest(BlockKind.epic, BlockKind.story), isFalse);
      expect(BlockRules.canNest(BlockKind.epic, BlockKind.epic), isFalse);
    });

    test('DSH-06.c: a sprint sits at the top of the board only', () {
      expect(BlockRules.canNest(BlockKind.sprint, null), isTrue);
      for (final p in BlockKind.values) {
        expect(BlockRules.canNest(BlockKind.sprint, p), isFalse, reason: p.name);
      }
    });

    test('DSH-02.b: a block kind is read by name, ignoring case and spaces; anything else is no kind', () {
      expect(BlockKind.parse(' Story '), BlockKind.story);
      expect(BlockKind.parse('EPIC'), BlockKind.epic);
      expect(BlockKind.parse('sprint'), BlockKind.sprint);
      expect(BlockKind.parse('feature'), isNull);
      expect(BlockKind.parse(''), isNull);
    });
  });

  group('NewIssue (DSH-09.a, DSH-09.b, DSH-09.d)', () {
    test('DSH-09.b: a new issue starts as backlog', () {
      expect(const NewIssue(title: 'T').status, Status.backlog);
    });

    test('DSH-09.d: the labels are issue, feature:<feature> and the status', () {
      expect(const NewIssue(title: 'T', feature: 'alpha', status: Status.proposed).labels, ['issue', 'feature:alpha', 'proposed']);
      expect(const NewIssue(title: 'T').labels, ['issue', 'backlog']);
    });

    test('DSH-09.d: the body is the description and a Requirement line', () {
      expect(const NewIssue(title: 'T', description: ' D ', requirement: 'AAA-01').body, 'D\n\nRequirement: AAA-01');
      expect(const NewIssue(title: 'T', requirement: 'AAA-01').body, 'Requirement: AAA-01');
      expect(const NewIssue(title: 'T', description: 'D').body, 'D');
    });

    test('DSH-09.d: fromJson and toJson round trip; an unknown or missing status is backlog', () {
      const n = NewIssue(title: 'T', description: 'D', feature: 'f', requirement: 'AAA-01', status: Status.planned);
      final back = NewIssue.fromJson(n.toJson());
      expect([back.title, back.description, back.feature, back.requirement, back.status],
          ['T', 'D', 'f', 'AAA-01', Status.planned]);
      expect(NewIssue.fromJson({'title': 'T', 'status': 'nope'}).status, Status.backlog);
      expect(NewIssue.fromJson({'title': 'T'}).status, Status.backlog);
    });
  });

  group('DEF-01 values the rows cite', () {
    test('DSH-05.e: the issue list limit is 200', () => expect(DashboardLimits.issues, 200));
    test('DSH-12.c: the progress refresh interval is 5 seconds', () => expect(DashboardLimits.progressRefresh, const Duration(seconds: 5)));
    test('DSH-13.a: the server starts on 127.0.0.1 port 8765', () {
      expect(DashboardServerConfig.host, '127.0.0.1');
      expect(DashboardServerConfig.port, 8765);
    });
    test('DSH-14.d: the estimate range is plus or minus 20 percent', () => expect(DashboardLimits.estimateRange, 0.2));
    test('DSH-15.a: the board takes 2 of 5 parts of the height', () {
      expect(DashboardLimits.boardShareParts, 2);
      expect(DashboardLimits.boardShareOf, 5);
    });
    test('DSH-15.c: the window sizes checked are 1920 x 1080 and 1280 x 720', () {
      expect([DashboardLimits.windowLargeWidth, DashboardLimits.windowLargeHeight], [1920, 1080]);
      expect([DashboardLimits.windowSmallWidth, DashboardLimits.windowSmallHeight], [1280, 720]);
    });
  });
}
