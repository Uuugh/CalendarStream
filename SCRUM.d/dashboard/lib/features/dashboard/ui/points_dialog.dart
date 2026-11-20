// Holds: the small dialog that edits one number of usage points (DSH-09.a). Depends on: PointsFormat, AppLocalizations.
// Used by: StoryCard. Reads or writes: nothing; it returns the new value.

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import '../domain/points_format.dart';

/// Asks for a number of points. The input has key [fieldKey]; Save (or Enter) returns the number, Cancel returns null.
/// A text that is not a number of 0 or more is not accepted.
class PointsDialog extends StatefulWidget {
  const PointsDialog({super.key, required this.label, required this.initial, required this.fieldKey});

  final String label;
  final double initial;
  final Key fieldKey;

  @override
  State<PointsDialog> createState() => _PointsDialogState();
}

class _PointsDialogState extends State<PointsDialog> {
  late final TextEditingController _controller = TextEditingController(text: PointsFormat.format(widget.initial));

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _save() {
    final n = PointsFormat.parse(_controller.text);
    if (n != null) Navigator.of(context).pop(n);
  }

  @override
  Widget build(BuildContext context) {
    final t = AppLocalizations.of(context);
    return AlertDialog(
      title: Text(widget.label),
      content: TextField(
        key: widget.fieldKey,
        controller: _controller,
        autofocus: true,
        keyboardType: const TextInputType.numberWithOptions(decimal: true),
        onSubmitted: (_) => _save(),
      ),
      actions: [
        TextButton(onPressed: () => Navigator.of(context).pop(), child: Text(t.cancel)),
        TextButton(key: const Key('points-save'), onPressed: _save, child: Text(t.save)),
      ],
    );
  }
}
