// Holds: the dashboard home page: loads the sprint, requirements and issues, shows the two filtered backlog lists,
// has the Reload control (DSH-01.c), DSH-01.f, DSH-05.f. Depends on: the repositories, IssueTracker, Backlog, ListFilterBar, AppLocalizations.
// Used by: main.dart. Reads or writes: through the repositories and the service.

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import '../data/issue_tracker.dart';
import '../data/server_unreachable_exception.dart';
import '../data/requirement_repository.dart';
import '../data/sprint_repository.dart';
import '../domain/backlog.dart';
import '../domain/dashboard_limits.dart';
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
  final IssueTracker issues;

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  Sprint _sprint = const Sprint();
  List<Requirement> _requirements = const [];
  List<Issue> _issues = const [];
  Object? _sprintError; // DSH-01.f: only the sprint is affected
  Object? _requirementError; // DSH-01.f: only the requirement list is affected
  Object? _issueError; // DSH-01.b: only the issue list is affected
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
      if (!mounted) return;
      setState(() {
        _sprint = sprint;
        _sprintError = null;
      });
    } catch (e) {
      if (mounted) setState(() => _sprintError = e);
    }
    try {
      final requirements = await widget.requirements.load();
      if (!mounted) return;
      setState(() {
        _requirements = requirements;
        _requirementError = null;
      });
    } catch (e) {
      if (mounted) setState(() => _requirementError = e);
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
        _issueError = e;
      });
    }
  }

  /// The message for a failed load: the server being unreachable is said so (DSH-10.e); any other failure uses
  /// [otherwise] (DSH-01.b, DSH-01.f).
  static String _failed(AppLocalizations t, Object error, String Function(String) otherwise) =>
      error is ServerUnreachableException ? t.dshServerUnreachable(error.reason) : otherwise('$error');

  /// Opens the New issue form (DSH-08); when an issue was created, the issue status filter is set to All (DSH-08.f)
  /// and the lists are read again.
  Future<void> _newIssue() async {
    final created = await showDialog<bool>(
      context: context,
      barrierDismissible: false,
      builder: (_) => NewIssueDialog(issues: widget.issues, requirements: _requirements),
    );
    if (created != true) return;
    setState(() => _issueFilter = ListFilter(feature: _issueFilter.feature, requirement: _issueFilter.requirement));
    await _reload();
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
    // DSH-03.d: the reader yields only backlog and proposed
    String requirementStatus(String s) => s == 'proposed' ? t.dshStatusProposed : t.dshStatusBacklog;
    final error = Theme.of(context).colorScheme.error;
    final backlog = BacklogDropArea(
      onRemove: (id) => _apply(SprintEdit.removeStory(_sprint, id)),
      child: ListView(padding: const EdgeInsets.all(DashboardLayout.gap), children: [
        ListTile(title: Text(t.dshRequirements, style: Theme.of(context).textTheme.titleMedium)),
        if (_requirementError != null)
          ListTile(title: Text(_failed(t, _requirementError!, t.dshLoadFailed), style: TextStyle(color: error)))
        else ...[
          ListFilterBar(
            filter: _requirementFilter,
            onChanged: (f) => setState(() => _requirementFilter = f),
            features: ListFilter.choices(requirements.map((r) => r.feature)),
            statuses: ListFilter.choices(requirements.map((r) => r.status)),
            statusLabel: requirementStatus,
            shown: shownRequirements.length,
            total: requirements.length,
          ),
          for (final r in shownRequirements)
            BacklogItemTile(
                id: r.id, title: r.statement, subtitle: '${r.feature} (${requirementStatus(r.status)}): ${r.statement}'),
        ],
        ListTile(title: Text(t.dshIssues, style: Theme.of(context).textTheme.titleMedium)),
        if (_issueError != null)
          ListTile(
            title: Text(_failed(t, _issueError!, t.dshTrackerUnreachable), style: TextStyle(color: error)),
          )
        else ...[
          if (_issues.length >= DashboardLimits.issues)
            ListTile(title: Text(t.dshIssuesTruncated('${DashboardLimits.issues}'))), // DSH-05.f
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
      body: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
              SizedBox(width: DashboardLayout.backlogWidth, child: backlog),
              Expanded(
                child: SingleChildScrollView(
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    if (_sprintError != null)
                      Padding(
                        padding: const EdgeInsets.all(DashboardLayout.gap),
                        child: Text(_failed(t, _sprintError!, t.dshLoadFailed), style: TextStyle(color: error)),
                      )
                    else ...[
                      SprintBoard(sprint: _sprint, onChanged: _apply),
                      UsagePanel(sprint: _sprint),
                    ],
                  ]),
                ),
              ),
            ]),
    );
  }
}
