// Holds: the message of each block kind (DSH-06.b). Depends on: BlockKind, AppLocalizations.
// Used by: BlockCard, AddBlockDialog. Reads or writes: nothing.

import '../../../l10n/app_localizations.dart';
import '../domain/block_kind.dart';

/// Block kind as text.
class BlockKindText {
  const BlockKindText._();

  static String of(AppLocalizations l, BlockKind kind) => switch (kind) {
        BlockKind.story => l.dshKindStory,
        BlockKind.epic => l.dshKindEpic,
        BlockKind.sprint => l.dshKindSprint,
      };
}
