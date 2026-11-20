// Holds: the Add block dialog (DSH-06.b): the kind, the name, Cancel and Save. Depends on: BlockKind, AppLocalizations.
// Used by: BoardView. Reads or writes: nothing; it returns the choice.

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import '../domain/block_kind.dart';
import 'block_kind_text.dart';
import 'dashboard_layout.dart';

/// The chosen kind and name of a new block.
typedef NewBlock = ({BlockKind kind, String name});

/// The dialog. Keys: `add-block-kind`, `add-block-name`, `add-block-cancel`, `add-block-save` (off while the name is blank).
class AddBlockDialog extends StatefulWidget {
  const AddBlockDialog({super.key});

  /// Opens the dialog; the choice, or null when it is cancelled.
  static Future<NewBlock?> show(BuildContext context) =>
      showDialog<NewBlock>(context: context, builder: (_) => const AddBlockDialog());

  @override
  State<AddBlockDialog> createState() => _AddBlockDialogState();
}

class _AddBlockDialogState extends State<AddBlockDialog> {
  final _name = TextEditingController();
  BlockKind _kind = BlockKind.story;

  @override
  void dispose() {
    _name.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l = AppLocalizations.of(context);
    return AlertDialog(
      title: Text(l.dshAddBlock),
      content: SizedBox(
        width: DashboardLayout.blockWidth,
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              InputDecorator(
                decoration: InputDecoration(labelText: l.dshBlockKind, border: const OutlineInputBorder()),
                child: DropdownButtonHideUnderline(
                  child: DropdownButton<BlockKind>(
                    key: const Key('add-block-kind'),
                    isExpanded: true,
                    isDense: true,
                    value: _kind,
                    items: [for (final k in BlockKind.values) DropdownMenuItem(value: k, child: Text(BlockKindText.of(l, k)))],
                    onChanged: (k) => setState(() => _kind = k ?? _kind),
                  ),
                ),
              ),
              const SizedBox(height: DashboardLayout.gap),
              TextField(
                key: const Key('add-block-name'),
                controller: _name,
                decoration: InputDecoration(labelText: l.dshBlockName),
                onChanged: (_) => setState(() {}),
              ),
            ],
          ),
        ),
      ),
      actions: [
        TextButton(key: const Key('add-block-cancel'), onPressed: () => Navigator.of(context).pop(), child: Text(l.cancel)),
        FilledButton(
          key: const Key('add-block-save'),
          onPressed: _name.text.trim().isEmpty ? null : () => Navigator.of(context).pop((kind: _kind, name: _name.text.trim())),
          child: Text(l.dshSave),
        ),
      ],
    );
  }
}
