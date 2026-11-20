// Holds: one story as a draggable card (DSH-06.b, DSH-06.c, DSH-07.b, DSH-07.c). Depends on: Story, AssigneeDot, DragPayload.
// Used by: SprintBoard. Reads or writes: nothing.

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import '../domain/points_format.dart';
import '../domain/story.dart';
import 'assignee_dot.dart';
import 'dashboard_layout.dart';
import 'drag_payload.dart';
import 'points_dialog.dart';

/// A card: story ID, estimate, usage, title and the assignee's dot, in the color [color] of its column (DSH-06.b, DSH-09.a).
/// Tapping the estimate (key `estimate-<storyId>`) or usage (`usage-<storyId>`) opens a dialog whose input has key
/// `estimate-field-<storyId>` or `usage-field-<storyId>`.
/// Key `card-<storyId>`; the dot has key `assignee-dot-<storyId>`.
class StoryCard extends StatelessWidget {
  const StoryCard({
    super.key,
    required this.story,
    required this.color,
    this.onEstimateChanged,
    this.onUsageChanged,
  });

  final Story story;
  final Color color;

  /// Called with the new estimate or usage when the user edits it (DSH-09.a).
  final ValueChanged<double>? onEstimateChanged;
  final ValueChanged<double>? onUsageChanged;

  Future<void> _edit(BuildContext context, String label, double current, Key fieldKey, ValueChanged<double>? done) async {
    if (done == null) return;
    final value = await showDialog<double>(
      context: context,
      builder: (_) => PointsDialog(label: label, initial: current, fieldKey: fieldKey),
    );
    if (value != null) done(value);
  }

  Widget _points(BuildContext context, String label, double value, Key key, Key fieldKey, ValueChanged<double>? done) =>
      InkWell(
        key: key,
        onTap: () => _edit(context, label, value, fieldKey, done),
        child: Text('$label: ${PointsFormat.format(value)}', style: Theme.of(context).textTheme.bodySmall),
      );

  Widget _body(BuildContext context) {
    final t = AppLocalizations.of(context);
    final text = Theme.of(context).textTheme;
    return Card(
      color: color.withValues(alpha: 0.18),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(DashboardLayout.gap),
        side: BorderSide(color: color),
      ),
      child: Padding(
        padding: const EdgeInsets.all(DashboardLayout.gap),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Row(children: [
            Expanded(child: Text(story.id, style: text.titleSmall)),
            AssigneeDot(key: Key('assignee-dot-${story.id}'), assignee: story.assignee),
          ]),
          Wrap(spacing: DashboardLayout.gap, children: [
            _points(context, t.dshEstimate, story.estimate, Key('estimate-${story.id}'),
                Key('estimate-field-${story.id}'), onEstimateChanged),
            _points(context, t.dshUsage, story.usage, Key('usage-${story.id}'), Key('usage-field-${story.id}'),
                onUsageChanged),
          ]),
          Text(story.title, style: text.bodyMedium),
        ]),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Draggable<DragPayload>(
      key: Key('card-${story.id}'),
      data: CardDrag(story.id),
      feedback: Material(
        color: Colors.transparent,
        child: SizedBox(width: DashboardLayout.columnWidth - 2 * DashboardLayout.gap, child: _body(context)),
      ),
      childWhenDragging: Opacity(opacity: 0.4, child: _body(context)),
      child: _body(context),
    );
  }
}
