// Holds: the dashboard page (DSH-01, DSH-15): the app bar with Reload, the board on top and the three columns below it
// (Requirements, Issues, Agent progress); the page itself does not scroll. Depends on: DashboardBackend, FilterStore,
// DashboardController, BoardView, the three columns, DashboardLimits. Used by: main.dart. Reads or writes: through the
// backend; re-reads progress and usage on a timer.

import 'dart:async';

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import '../data/dashboard_backend.dart';
import '../data/filter_store_factory.dart';
import '../domain/dashboard_limits.dart';
import '../domain/filter_store.dart';
import 'board_view.dart';
import 'dashboard_controller.dart';
import 'issues_column.dart';
import 'progress_column.dart';
import 'requirements_column.dart';

/// The page. [filters] keeps the filters' choices (the platform's store when null); [refresh] is how often progress and
/// usage are read again (DashboardLimits.progressRefresh when null; [Duration.zero] turns the timer off).
class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key, required this.backend, this.filters, this.refresh});

  final DashboardBackend backend;
  final FilterStore? filters;
  final Duration? refresh;

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  late final DashboardController _controller =
      DashboardController(backend: widget.backend, filterStore: widget.filters ?? FilterStoreFactory.create());
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _controller.reload();
    final every = widget.refresh ?? DashboardLimits.progressRefresh;
    if (every > Duration.zero) _timer = Timer.periodic(every, (_) => _controller.reloadLive());
  }

  @override
  void dispose() {
    _timer?.cancel();
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l = AppLocalizations.of(context);
    return Scaffold(
      appBar: AppBar(
        actions: [
          IconButton(key: const Key('reload-button'), tooltip: l.dshReload, onPressed: _controller.reload, icon: const Icon(Icons.refresh)),
        ],
      ),
      body: ListenableBuilder(
        listenable: _controller,
        builder: (context, _) => Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Expanded(flex: DashboardLimits.boardShareParts, child: BoardView(controller: _controller)),
            Expanded(
              flex: DashboardLimits.boardShareOf - DashboardLimits.boardShareParts,
              child: Row(children: [
                Expanded(child: RequirementsColumn(controller: _controller)),
                Expanded(child: IssuesColumn(controller: _controller)),
                Expanded(child: ProgressColumn(controller: _controller)),
              ]),
            ),
          ],
        ),
      ),
    );
  }
}
