// Holds: the app entry point and shell. Depends on: the dashboard feature, DashboardBackend, AppLocalizations.
// Used by: Flutter. Reads or writes: nothing itself; the backend of the platform does (desktop: files and `gh`; web: the server).

import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

import 'features/dashboard/data/dashboard_backend.dart';
import 'features/dashboard/ui/dashboard_page.dart';
import 'l10n/app_localizations.dart';
import 'theme/app_theme.dart';

void main() {
  runApp(MaterialApp(
    localizationsDelegates: const [
      AppLocalizations.delegate,
      GlobalMaterialLocalizations.delegate,
      GlobalWidgetsLocalizations.delegate,
      GlobalCupertinoLocalizations.delegate,
    ],
    supportedLocales: AppLocalizations.supportedLocales,
    theme: AppTheme.light,
    darkTheme: AppTheme.dark,
    home: DashboardPage(backend: DashboardBackend.create()),
  ));
}
