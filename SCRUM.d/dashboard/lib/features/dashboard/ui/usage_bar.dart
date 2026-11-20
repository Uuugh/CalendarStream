// Holds: the bar of usage against estimate (DSH-10.c): in the warn color when usage is above the estimate.
// Depends on: StatusColors, DashboardLayout. Used by: StoryBody, BlockCard. Reads or writes: nothing.

import 'package:flutter/material.dart';

import '../../../theme/app_theme.dart';
import 'dashboard_layout.dart';

/// A bar filled with [usage] out of [estimate]; full and warn-colored when usage is above the estimate.
class UsageBar extends StatelessWidget {
  const UsageBar({super.key, required this.estimate, required this.usage});

  final double estimate;
  final double usage;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colors = StatusColors.of(theme);
    final over = usage > estimate;
    final fraction = estimate > 0 ? (usage / estimate).clamp(0.0, 1.0) : (usage > 0 ? 1.0 : 0.0);
    return ClipRRect(
      borderRadius: BorderRadius.circular(DashboardLayout.barHeight),
      child: LinearProgressIndicator(
        value: fraction,
        minHeight: DashboardLayout.barHeight,
        color: over ? colors.warn : colors.run,
        backgroundColor: theme.colorScheme.surfaceContainerHigh,
      ),
    );
  }
}
