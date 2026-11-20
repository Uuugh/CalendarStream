// Holds: the New issue form dialog (DSH-08, DSH-08.a-d, DSH-08.g, DSH-08.h): title, description, feature, requirement and status; Save
// creates the issue and closes the dialog with true. Depends on: IssueTracker, NewIssue, RequirementChoices,
// Requirement, AppLocalizations. Used by: the dashboard page. Reads or writes: the issue tracker, through the service.

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import '../data/issue_partial_failure.dart';
import '../data/issue_tracker.dart';
import '../data/issue_tracker_exception.dart';
import '../domain/new_issue.dart';
import '../domain/requirement.dart';
import '../domain/requirement_choices.dart';
import 'dashboard_layout.dart';

/// The form; pops with true once the issue is created (or exists after a failed later step and the form is cancelled),
/// and stays filled and shows the reason when it cannot be created. Keys: `issue-save`, `issue-cancel`.
class NewIssueDialog extends StatefulWidget {
  const NewIssueDialog({super.key, required this.issues, required this.requirements});

  final IssueTracker issues;
  final List<Requirement> requirements;

  @override
  State<NewIssueDialog> createState() => _NewIssueDialogState();
}

class _NewIssueDialogState extends State<NewIssueDialog> {
  final _title = TextEditingController();
  final _description = TextEditingController();
  String? _feature;
  String? _requirement;
  bool _closed = false; // DSH-08.b: starts open
  bool _saving = false;
  String? _failure;
  int? _created; // the number of the issue once it exists, so saving again never creates another (DSH-08.g)
  String? _partialReason;

  @override
  void initState() {
    super.initState();
    _title.addListener(() => setState(() {}));
  }

  @override
  void dispose() {
    _title.dispose();
    _description.dispose();
    super.dispose();
  }

  /// Creates the issue, or, when it already exists, only does the step that failed (DSH-08.g).
  Future<void> _save() async {
    setState(() {
      _saving = true;
      _failure = null;
      _partialReason = null;
    });
    try {
      final existing = _created;
      if (existing == null) {
        _created = await widget.issues.create(NewIssue(
          title: _title.text.trim(),
          description: _description.text,
          feature: _feature,
          requirement: _requirement,
          closed: _closed,
        ));
      } else {
        await widget.issues.close(existing);
      }
      if (mounted) Navigator.of(context).pop(true);
    } on IssuePartialFailure catch (e) {
      if (mounted) {
        setState(() {
          _saving = false;
          _created = e.number;
          _partialReason = e.reason;
        });
      }
    } on IssueTrackerException catch (e) {
      if (mounted) {
        setState(() {
          _saving = false;
          if (_created == null) {
            _failure = e.reason;
          } else {
            _partialReason = e.reason;
          }
        });
      }
    }
  }


  Widget _dropdown(Key key, String label, String? value, List<String> values, String Function(String) text,
      ValueChanged<String?> onSelected, {bool blank = true}) {
    return InputDecorator(
      decoration: InputDecoration(labelText: label),
      child: DropdownButtonHideUnderline(
        child: DropdownButton<String?>(
          key: key,
          isDense: true,
          isExpanded: true,
          value: values.contains(value) ? value : null,
          items: [
            if (blank) const DropdownMenuItem<String?>(value: null, child: SizedBox.shrink()),
            for (final v in values) DropdownMenuItem<String?>(value: v, child: Text(text(v))),
          ],
          onChanged: onSelected,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final t = AppLocalizations.of(context);
    final requirementIds = RequirementChoices.requirementsOf(widget.requirements, _feature);
    return AlertDialog(
      title: Text(t.dshNewIssue),
      content: SizedBox(
        width: DashboardLayout.backlogWidth,
        child: SingleChildScrollView(
          child: Column(mainAxisSize: MainAxisSize.min, children: [
            TextField(
              key: const Key('issue-title'),
              controller: _title,
              decoration: InputDecoration(labelText: t.dshIssueTitle),
            ),
            TextField(
              key: const Key('issue-description'),
              controller: _description,
              minLines: 3,
              maxLines: 6,
              decoration: InputDecoration(labelText: t.dshIssueDescription),
            ),
            _dropdown(const Key('issue-feature'), t.dshFilterFeature, _feature,
                RequirementChoices.features(widget.requirements), (v) => v, (v) {
              setState(() {
                _feature = v;
                _requirement = RequirementChoices.keepRequirement(widget.requirements, v, _requirement);
              });
            }),
            _dropdown(const Key('issue-requirement'), t.dshFilterRequirement, _requirement, requirementIds,
                (v) => v, (v) => setState(() => _requirement = v)),
            _dropdown(const Key('issue-status'), t.dshFilterStatus, _closed ? 'closed' : 'open',
                const ['open', 'closed'], (v) => v == 'closed' ? t.dshStatusClosed : t.dshStatusOpen,
                (v) => setState(() => _closed = v == 'closed'), blank: false),
            if (_partialReason != null)
              Text(t.dshIssuePartial('$_created', _partialReason!), style: TextStyle(color: Theme.of(context).colorScheme.error)),
            if (_failure != null)
              Text(t.dshIssueFailed(_failure!), style: TextStyle(color: Theme.of(context).colorScheme.error)),
          ]),
        ),
      ),
      actions: [
        TextButton(
          key: const Key('issue-cancel'),
          onPressed: () => Navigator.of(context).pop(_created != null),
          child: Text(t.cancel),
        ),
        FilledButton(
          key: const Key('issue-save'),
          onPressed: _title.text.trim().isEmpty || _saving ? null : _save,
          child: Text(t.dshSave),
        ),
      ],
    );
  }
}
