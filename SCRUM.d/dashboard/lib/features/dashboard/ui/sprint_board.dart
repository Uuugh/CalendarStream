// Holds: the sprint board (DSH-06, DSH-07.a, DSH-07.b, DSH-07.d, DSH-09.a): the goal and one drop column per stage.
// Depends on: Sprint, SprintEdit, Stage, StageColors, StoryCard, AppLocalizations. Used by: the dashboard page.
// Reads or writes: nothing; it reports the edited sprint through [onChanged].

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import '../domain/sprint.dart';
import '../domain/sprint_edit.dart';
import '../domain/stage.dart';
import 'dashboard_layout.dart';
import 'drag_payload.dart';
import 'stage_colors.dart';
import 'story_card.dart';

/// The board. Columns have key `column-<stage name>`. A drop that changes the sprint calls [onChanged] with the
/// new sprint; a drop that changes nothing (a card on its own column) does not call it.
class SprintBoard extends StatelessWidget {
  const SprintBoard({super.key, required this.sprint, required this.onChanged});

  final Sprint sprint;
  final ValueChanged<Sprint> onChanged;

  String _stageName(AppLocalizations t, Stage s) => switch (s) {
        Stage.backlog => t.dshBacklog,
        Stage.ready => t.dshReady,
        Stage.build => t.dshBuild,
        Stage.test => t.dshTest,
        Stage.review => t.dshReview,
        Stage.done => t.dshDone,
      };

  /// Reports [next] unless it is the same sprint.
  void _edit(Sprint next) {
    if (!identical(next, sprint)) onChanged(next);
  }


  void _drop(Stage stage, DragPayload payload) {
    final next = switch (payload) {
      BacklogDrag(:final id, :final title) => SprintEdit.addStory(sprint, id: id, title: title, stage: stage),
      CardDrag(:final storyId) => SprintEdit.moveStory(sprint, storyId, stage),
    };
    _edit(next);
  }

  @override
  Widget build(BuildContext context) {
    final t = AppLocalizations.of(context);
    final scheme = Theme.of(context).colorScheme;
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Padding(
        padding: const EdgeInsets.all(DashboardLayout.gap),
        child: Text('${t.dshSprintGoal}: ${sprint.goal}', style: Theme.of(context).textTheme.titleMedium),
      ),
      SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
          for (final stage in Stage.values) _column(context, t, scheme, stage),
        ]),
      ),
    ]);
  }

  Widget _column(BuildContext context, AppLocalizations t, ColorScheme scheme, Stage stage) {
    final color = StageColors.of(scheme, stage);
    final cards = sprint.stories.where((s) => s.stage == stage).toList();
    return DragTarget<DragPayload>(
      key: Key('column-${stage.name}'),
      onAcceptWithDetails: (d) => _drop(stage, d.data),
      builder: (context, candidates, rejected) => Container(
        width: DashboardLayout.columnWidth,
        constraints: const BoxConstraints(minHeight: DashboardLayout.columnMinHeight),
        margin: const EdgeInsets.all(DashboardLayout.gap / 2),
        padding: const EdgeInsets.all(DashboardLayout.gap / 2),
        decoration: BoxDecoration(
          color: color.withValues(alpha: candidates.isEmpty ? 0.06 : 0.2),
          border: Border(top: BorderSide(color: color, width: 4)),
        ),
        child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          Padding(
            padding: const EdgeInsets.all(DashboardLayout.gap / 2),
            child: Text(
              '${_stageName(t, stage)}  ${t.dshColumnCount('${cards.length}', '${sprint.stories.length}')}',
              style: Theme.of(context).textTheme.titleSmall?.copyWith(color: color),
            ),
          ),
          for (final story in cards)
            StoryCard(
              story: story,
              color: color,
              onEstimateChanged: (v) => _edit(SprintEdit.setEstimate(sprint, story.id, v)),
              onUsageChanged: (v) => _edit(SprintEdit.setUsage(sprint, story.id, v)),
            ),
        ]),
      ),
    );
  }
}
