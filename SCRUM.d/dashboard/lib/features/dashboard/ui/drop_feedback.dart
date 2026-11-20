// Holds: the message shown when a drop or an accept is refused (DSH-07.g). Depends on: AppLocalizations.
// Used by: BlockCard, BacklogBlock, BoardView, StoryBody. Reads or writes: nothing.

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';

/// Waits for a change and says why when it was refused.
class DropFeedback {
  const DropFeedback._();

  /// Awaits [result] (the reason it was refused, or null) and shows msg:dshMoveRefused in a snack bar for a reason.
  static Future<void> run(BuildContext context, Future<String?> result) async {
    final messenger = ScaffoldMessenger.maybeOf(context);
    final l = AppLocalizations.of(context);
    final reason = await result;
    if (reason != null) messenger?.showSnackBar(SnackBar(content: Text(l.dshMoveRefused(reason))));
  }
}
