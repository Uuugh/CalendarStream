// Holds: the app entry point and shell. Depends on: the dashboard feature, AppLocalizations.
// Used by: Flutter. Reads or writes: nothing itself; the repositories read the repo at REPO_ROOT
// (dart-define, default `../..`). The web build cannot read files, so it shows an error there.

import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

import 'features/dashboard/data/disk_file_access.dart';
import 'features/dashboard/data/requirement_repository.dart';
import 'features/dashboard/data/sprint_repository.dart';
import 'features/dashboard/ui/dashboard_page.dart';
import 'l10n/app_localizations.dart';

const _repoRoot = String.fromEnvironment('REPO_ROOT', defaultValue: '../..');

void main() {
  const files = DiskFileAccess();
  runApp(MaterialApp(
    localizationsDelegates: const [
      AppLocalizations.delegate,
      GlobalMaterialLocalizations.delegate,
      GlobalWidgetsLocalizations.delegate,
      GlobalCupertinoLocalizations.delegate,
    ],
    supportedLocales: AppLocalizations.supportedLocales,
    home: DashboardPage(
      sprints: SprintRepository(files: files, path: '$_repoRoot/SCRUM.d/sprint.md'),
      requirements: RequirementRepository(files: files, directory: '$_repoRoot/requirements'),
    ),
  ));
}
