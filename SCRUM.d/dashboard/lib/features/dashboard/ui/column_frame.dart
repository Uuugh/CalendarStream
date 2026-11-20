// Holds: the frame of a column below the board (DSH-15.b): a heading area and a body that scrolls on its own.
// Depends on: DashboardLayout. Used by: RequirementsColumn, IssuesColumn, ProgressColumn. Reads or writes: nothing.

import 'package:flutter/material.dart';

import 'dashboard_layout.dart';

/// A bordered column with [header] on top and [body] filling the rest; the body is a scrollable the caller builds from
/// the [ScrollController] given to [builder] so the scrollbar and the list share it.
class ColumnFrame extends StatefulWidget {
  const ColumnFrame({super.key, required this.header, required this.builder});

  final Widget header;
  final Widget Function(BuildContext context, ScrollController controller) builder;

  @override
  State<ColumnFrame> createState() => _ColumnFrameState();
}

class _ColumnFrameState extends State<ColumnFrame> {
  final ScrollController _controller = ScrollController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.all(DashboardLayout.pad / 2),
      child: Padding(
        padding: const EdgeInsets.all(DashboardLayout.pad),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            widget.header,
            const SizedBox(height: DashboardLayout.gap),
            Expanded(child: Scrollbar(controller: _controller, child: widget.builder(context, _controller))),
          ],
        ),
      ),
    );
  }
}
