// Holds: the assignee's dot (DSH-06.d): the assignee's color with the name as tooltip, or an empty ring when none.
// Depends on: AssigneeColors, AppLocalizations. Used by: StoryCard. Reads or writes: nothing.

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import 'assignee_colors.dart';

/// The dot of [assignee]; empty (outline only, tooltip msg:dshNoAssignee) when [assignee] is empty.
class AssigneeDot extends StatelessWidget {
  const AssigneeDot({super.key, required this.assignee});

  static const double size = 14;

  final String assignee;

  @override
  Widget build(BuildContext context) {
    final empty = assignee.isEmpty;
    final outline = Theme.of(context).colorScheme.outline;
    return Tooltip(
      message: empty ? AppLocalizations.of(context).dshNoAssignee : assignee,
      child: Container(
        width: size,
        height: size,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: empty ? null : AssigneeColors.of(Theme.of(context), assignee),
          border: empty ? Border.all(color: outline) : null,
        ),
      ),
    );
  }
}
