// Holds: the New issue form (DSH-09): title, description, feature, requirement and status, Cancel and Save, and the
// reason when saving fails. Depends on: DashboardController, RequirementChoices, NewIssue, StatusText.
// Used by: IssuesColumn. Reads or writes: creates an issue through the controller on Save.

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import '../domain/new_issue.dart';
import '../domain/requirement_choices.dart';
import '../domain/status.dart';
import 'dashboard_controller.dart';
import 'dashboard_layout.dart';
import 'status_text.dart';

/// The form dialog. Keys: `issue-title`, `issue-description`, `issue-feature`, `issue-requirement`, `issue-status`,
/// `issue-cancel`, `issue-save`.
class NewIssueDialog extends StatefulWidget {
  const NewIssueDialog({super.key, required this.controller});

  final DashboardController controller;

  /// Opens the form; completes when it is closed.
  static Future<void> show(BuildContext context, DashboardController controller) =>
      showDialog<void>(context: context, builder: (_) => NewIssueDialog(controller: controller));

  @override
  State<NewIssueDialog> createState() => _NewIssueDialogState();
}

class _NewIssueDialogState extends State<NewIssueDialog> {
  final _title = TextEditingController();
  final _description = TextEditingController();
  String? _feature;
  String? _requirement;
  Status _status = Status.backlog;
  String? _failure;
  bool _saving = false;

  @override
  void dispose() {
    _title.dispose();
    _description.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    setState(() {
      _saving = true;
      _failure = null;
    });
    try {
      await widget.controller.createIssue(NewIssue(
        title: _title.text.trim(),
        description: _description.text,
        feature: _feature,
        requirement: _requirement,
        status: _status,
      ));
      if (mounted) Navigator.of(context).pop();
    } catch (e) {
      if (mounted) {
        setState(() {
          _saving = false;
          _failure = '$e';
        });
      }
    }
  }

  Widget _dropdown<T>({
    required Key key,
    required String label,
    required T? value,
    required List<DropdownMenuItem<T>> items,
    required ValueChanged<T?> onChanged,
  }) {
    return InputDecorator(
      decoration: InputDecoration(labelText: label, border: const OutlineInputBorder()),
      isEmpty: value == null,
      child: DropdownButtonHideUnderline(
        child: DropdownButton<T>(key: key, isExpanded: true, isDense: true, value: value, items: items, onChanged: onChanged),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final l = AppLocalizations.of(context);
    final requirements = widget.controller.requirements ?? const [];
    final features = RequirementChoices.features(requirements);
    final ids = RequirementChoices.requirementsOf(requirements, _feature);
    return AlertDialog(
      title: Text(l.dshNewIssue),
      content: SizedBox(
        width: DashboardLayout.blockWidth * 1.5,
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              TextField(
                key: const Key('issue-title'),
                controller: _title,
                decoration: InputDecoration(labelText: l.dshIssueTitle),
                onChanged: (_) => setState(() {}),
              ),
              const SizedBox(height: DashboardLayout.gap),
              TextField(
                key: const Key('issue-description'),
                controller: _description,
                minLines: 2,
                maxLines: 5,
                decoration: InputDecoration(labelText: l.dshIssueDescription),
              ),
              const SizedBox(height: DashboardLayout.gap),
              _dropdown<String>(
                key: const Key('issue-feature'),
                label: l.dshFilterFeature,
                value: _feature,
                items: [for (final f in features) DropdownMenuItem(value: f, child: Text(f, overflow: TextOverflow.ellipsis))],
                onChanged: (f) => setState(() {
                  _feature = f;
                  _requirement = RequirementChoices.keepRequirement(requirements, f, _requirement);
                }),
              ),
              const SizedBox(height: DashboardLayout.gap),
              _dropdown<String>(
                key: const Key('issue-requirement'),
                label: l.dshFilterRequirement,
                value: _requirement,
                items: [for (final r in ids) DropdownMenuItem(value: r, child: Text(r, overflow: TextOverflow.ellipsis))],
                onChanged: (r) => setState(() => _requirement = r),
              ),
              const SizedBox(height: DashboardLayout.gap),
              _dropdown<Status>(
                key: const Key('issue-status'),
                label: l.dshFilterStatus,
                value: _status,
                items: [for (final s in Status.values) DropdownMenuItem(value: s, child: Text(StatusText.of(l, s)))],
                onChanged: (s) => setState(() => _status = s ?? _status),
              ),
              if (_failure != null) ...[
                const SizedBox(height: DashboardLayout.gap),
                Text(l.dshIssueFailed(_failure!), style: TextStyle(color: Theme.of(context).colorScheme.error)),
              ],
            ],
          ),
        ),
      ),
      actions: [
        TextButton(key: const Key('issue-cancel'), onPressed: () => Navigator.of(context).pop(), child: Text(l.cancel)),
        FilledButton(
          key: const Key('issue-save'),
          onPressed: _title.text.trim().isEmpty || _saving ? null : _save,
          child: Text(l.dshSave),
        ),
      ],
    );
  }
}
