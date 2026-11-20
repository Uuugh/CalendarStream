// Holds: the dashboard home page: loads the sprint and requirements, shows them, has the Reload control (DSH-01.c).
// Depends on: the repositories, AppLocalizations. Used by: main.dart. Reads or writes: through the repositories.

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import '../data/requirement_repository.dart';
import '../data/sprint_repository.dart';
import '../domain/requirement.dart';
import '../domain/sprint.dart';

/// Minimal page: sprint goal, its stories and the backlog requirements, with a Reload control.
class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key, required this.sprints, required this.requirements});

  final SprintRepository sprints;
  final RequirementRepository requirements;

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  Sprint _sprint = const Sprint();
  List<Requirement> _requirements = const [];
  Object? _error;

  @override
  void initState() {
    super.initState();
    _reload();
  }

  Future<void> _reload() async {
    try {
      final sprint = await widget.sprints.load();
      final requirements = await widget.requirements.load();
      if (!mounted) return;
      setState(() {
        _sprint = sprint;
        _requirements = requirements;
        _error = null;
      });
    } catch (e) {
      if (mounted) setState(() => _error = e);
    }
  }

  @override
  Widget build(BuildContext context) {
    final t = AppLocalizations.of(context);
    final inSprint = {for (final s in _sprint.stories) ...s.items, for (final s in _sprint.stories) s.id};
    final backlog = _requirements.where((r) => r.status == 'backlog' && !inSprint.contains(r.id)).toList();
    return Scaffold(
      appBar: AppBar(
        title: Text('${t.dshSprintGoal}: ${_sprint.goal}'),
        actions: [TextButton(onPressed: _reload, child: Text(t.dshReload))],
      ),
      body: _error != null
          ? Center(child: Text('$_error'))
          : ListView(children: [
              for (final s in _sprint.stories)
                ListTile(title: Text('${s.id} ${s.title}'), subtitle: Text(s.stage.name), trailing: Text(s.assignee)),
              ListTile(title: Text(t.dshRequirements)),
              for (final r in backlog) ListTile(title: Text(r.id), subtitle: Text('${r.feature}: ${r.statement}')),
            ]),
    );
  }
}
