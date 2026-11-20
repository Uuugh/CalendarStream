// Holds: the dashboard home page: loads the sprint, requirements and issues, shows the two filtered backlog lists,
// has the Reload control (DSH-01.c). Depends on: the repositories, IssueService, Backlog, ListFilterBar, AppLocalizations.
// Used by: main.dart. Reads or writes: through the repositories and the service.

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import '../data/issue_service.dart';
import '../data/requirement_repository.dart';
import '../data/sprint_repository.dart';
import '../domain/backlog.dart';
import '../domain/issue.dart';
import '../domain/list_filter.dart';
import '../domain/requirement.dart';
import '../domain/sprint.dart';
import '../domain/sprint_edit.dart';
import 'backlog_drop_area.dart';
import 'backlog_item_tile.dart';
import 'dashboard_layout.dart';
import 'list_filter_bar.dart';
import 'new_issue_dialog.dart';
import 'sprint_board.dart';
import 'usage_panel.dart';

/// Minimal page: sprint goal, its stories, the backlog requirements and the backlog issues, with a Reload control.
class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key, required this.sprints, required this.requirements, required this.issues});

  final SprintRepository sprints;
  final RequirementRepository requirements;
  final IssueService issues;

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  Sprint _sprint = const Sprint();
  List<Requirement> _requirements = const [];
  List<Issue> _issues = const [];
  Object? _error;
  String? _issueError; // DSH-01.b: only the issue list is affected
  ListFilter _requirementFilter = const ListFilter(status: 'backlog'); // DSH-03.c
  ListFilter _issueFilter = const ListFilter(status: 'open'); // DSH-05.a

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
    try {
      final issues = await widget.issues.load();
      if (!mounted) return;
      setState(() {
        _issues = issues;
        _issueError = null;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _issues = const [];
        _issueError = '$e';
      });
    }
  }

  /// Opens the New issue form (DSH-08); reloads the lists when an issue was created.
  Future<void> _newIssue() async {
    final created = await showDialog<bool>(
      context: context,
      builder: (_) => NewIssueDialog(issues: widget.issues, requirements: _requirements),
    );
    if (created == true) await _reload();
  }

  /// Shows [next] and writes it to the sprint file at once (DSH-02.c); nothing happens when it is the same sprint.
  Future<void> _apply(Sprint next) async {
    if (identical(next, _sprint)) return;
    setState(() => _sprint = next);
    await widget.sprints.save(next);
  }

  @override
  Widget build(BuildContext context) {
    final t = AppLocalizations.of(context);
    final requirements = Backlog.requirements(_requirements, _sprint);
    final shownRequirements = _requirementFilter.apply(requirements,
        feature: (r) => r.feature, requirementId: (r) => r.id, status: (r) => r.status);
    final issues = Backlog.issues(_issues, _sprint);
    final shownIssues = _issueFilter.apply(issues,
        feature: (i) => i.feature, requirementId: (i) => i.requirement, status: (i) => i.status.name);
    String issueStatus(String s) => s == IssueStatus.closed.name ? t.dshStatusClosed : t.dshStatusOpen;
    final backlog = BacklogDropArea(
      onRemove: (id) => _apply(SprintEdit.removeStory(_sprint, id)),
      child: ListView(padding: const EdgeInsets.all(DashboardLayout.gap), children: [
        ListTile(title: Text(t.dshRequirements, style: Theme.of(context).textTheme.titleMedium)),
        ListFilterBar(
          filter: _requirementFilter,
          onChanged: (f) => setState(() => _requirementFilter = f),
          features: ListFilter.choices(requirements.map((r) => r.feature)),
          statuses: ListFilter.choices(requirements.map((r) => r.status)),
          statusLabel: (s) => s,
          shown: shownRequirements.length,
          total: requirements.length,
        ),
        for (final r in shownRequirements)
          BacklogItemTile(id: r.id, title: r.statement, subtitle: '${r.feature} (${r.status}): ${r.statement}'),
        ListTile(title: Text(t.dshIssues, style: Theme.of(context).textTheme.titleMedium)),
        if (_issueError != null)
          ListTile(
            title: Text(t.dshTrackerUnreachable(_issueError!),
                style: TextStyle(color: Theme.of(context).colorScheme.error)),
          )
        else ...[
          ListFilterBar(
            filter: _issueFilter,
            onChanged: (f) => setState(() => _issueFilter = f),
            features: ListFilter.choices(issues.map((i) => i.feature)),
            statuses: ListFilter.choices(issues.map((i) => i.status.name)),
            statusLabel: issueStatus,
            shown: shownIssues.length,
            total: issues.length,
          ),
          for (final i in shownIssues)
            BacklogItemTile(
              id: '#${i.number}',
              title: i.title,
              subtitle: '${i.title} | ${issueStatus(i.status.name)} | ${i.feature ?? DashboardLayout.dash} | '
                  '${i.requirement ?? DashboardLayout.dash} | ${i.assignee.isEmpty ? DashboardLayout.dash : i.assignee}',
            ),
        ],
      ]),
    );
    return Scaffold(
      appBar: AppBar(actions: [
        TextButton(key: const Key('new-issue-button'), onPressed: _newIssue, child: Text(t.dshNewIssue)),
        TextButton(key: const Key('reload-button'), onPressed: _reload, child: Text(t.dshReload)),
      ]),
      body: _error != null
          ? Center(child: Text('$_error'))
          : Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
              SizedBox(width: DashboardLayout.backlogWidth, child: backlog),
              Expanded(
                child: SingleChildScrollView(
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    SprintBoard(sprint: _sprint, onChanged: _apply),
                    UsagePanel(sprint: _sprint),
                  ]),
                ),
              ),
            ]),
    );
  }
}
