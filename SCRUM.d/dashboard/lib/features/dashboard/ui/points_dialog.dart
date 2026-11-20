// Holds: the dialog that edits a story's estimate or usage (DSH-10.a): one number, Cancel and Save. Depends on:
// PointsFormat, AppLocalizations. Used by: StoryBody. Reads or writes: nothing; it returns the number.

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import '../domain/points_format.dart';
import 'dashboard_layout.dart';

/// The dialog. Keys: `points-input`, `points-cancel`, `points-save` (off while the text is not a number of 0 or more).
class PointsDialog extends StatefulWidget {
  const PointsDialog({super.key, required this.label, required this.initial});

  final String label;
  final double initial;

  /// Opens the dialog; the new number, or null when it is cancelled.
  static Future<double?> show(BuildContext context, {required String label, required double initial}) =>
      showDialog<double>(context: context, builder: (_) => PointsDialog(label: label, initial: initial));

  @override
  State<PointsDialog> createState() => _PointsDialogState();
}

class _PointsDialogState extends State<PointsDialog> {
  late final TextEditingController _text = TextEditingController(text: PointsFormat.format(widget.initial));

  @override
  void dispose() {
    _text.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l = AppLocalizations.of(context);
    final value = PointsFormat.parse(_text.text);
    return AlertDialog(
      title: Text(widget.label),
      content: SizedBox(
        width: DashboardLayout.blockWidth,
        child: TextField(
          key: const Key('points-input'),
          controller: _text,
          autofocus: true,
          keyboardType: const TextInputType.numberWithOptions(decimal: true),
          decoration: InputDecoration(labelText: widget.label),
          onChanged: (_) => setState(() {}),
          onSubmitted: (_) => value == null ? null : Navigator.of(context).pop(value),
        ),
      ),
      actions: [
        TextButton(key: const Key('points-cancel'), onPressed: () => Navigator.of(context).pop(), child: Text(l.cancel)),
        FilledButton(
          key: const Key('points-save'),
          onPressed: value == null ? null : () => Navigator.of(context).pop(value),
          child: Text(l.dshSave),
        ),
      ],
    );
  }
}
