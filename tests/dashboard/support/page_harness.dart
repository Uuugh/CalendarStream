// A test app and a dashboard page on in-memory files, so page tests wait for nothing in real time.
// Depends on the dashboard package and fixtures.dart; used by every widget test; touches nothing outside memory.
import 'package:dashboard/features/dashboard/data/command_runner.dart';
import 'package:dashboard/features/dashboard/data/issue_service.dart';
import 'package:dashboard/features/dashboard/data/file_access.dart';
import 'package:dashboard/features/dashboard/data/requirement_repository.dart';
import 'package:dashboard/features/dashboard/data/sprint_repository.dart';
import 'package:dashboard/features/dashboard/ui/dashboard_page.dart';
import 'package:dashboard/l10n/app_localizations.dart';
import 'package:dashboard/theme/app_theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_test/flutter_test.dart';

import 'fixtures.dart';

/// A MaterialApp with the dashboard's localizations and, unless [theme] is given, its light theme.
Widget testApp(Widget home, {ThemeData? theme, Locale? locale}) => MaterialApp(
      theme: theme ?? AppTheme.light,
      locale: locale,
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: AppLocalizations.supportedLocales,
      home: home,
    );

/// Makes the test window large enough for the whole page.
void bigView(WidgetTester t, {Size size = const Size(2400, 1800)}) {
  t.view.physicalSize = size;
  t.view.devicePixelRatio = 1;
  addTearDown(t.view.reset);
}

/// Pumps a [DashboardPage] on [files] and [runner] and settles it.
Future<void> pumpPage(
  WidgetTester t, {
  required FileAccess files,
  required CommandRunner runner,
  ThemeData? theme,
  String sprintPath = memSprintPath,
  String requirementsDir = memRequirementsDir,
}) async {
  bigView(t);
  await t.pumpWidget(const SizedBox()); // a fresh page, never the state of an earlier one
  await t.pumpWidget(testApp(
    DashboardPage(
      sprints: SprintRepository(files: files, path: sprintPath),
      requirements: RequirementRepository(files: files, directory: requirementsDir),
      issues: IssueService(runner: runner),
    ),
    theme: theme,
  ));
  await t.pumpAndSettle();
}
