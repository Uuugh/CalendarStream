// Holds: one meter of the usage chart (DSH-14.b to DSH-14.f): a 0 to 100 track with the before-to-after bars in the data
// color, the lighter estimate bands, the projection band ending in a mark, a triangle on the 100 line for values above
// 100 with the real numbers in its tooltip, and the names of the blocks drawn. Depends on: UsageChart, UsageMeter,
// UsageRow, Sprint, StatusColors, PointsFormat. Used by: UsageChartView. Reads or writes: nothing.

import 'package:flutter/material.dart';

import '../../../l10n/app_localizations.dart';
import '../../../theme/app_theme.dart';
import '../domain/points_format.dart';
import '../domain/sprint.dart';
import '../domain/usage_chart.dart';
import '../domain/usage_meter.dart';
import '../domain/usage_row.dart';
import '../domain/usage_span.dart';
import 'dashboard_layout.dart';

/// A meter, `Key('usage-meter-session')` or `Key('usage-meter-week')`; the over-100 triangle is `Key('usage-over-<meter>')`.
class UsageMeterView extends StatelessWidget {
  UsageMeterView({required this.meter, required this.rows, required this.sprint}) : super(key: Key('usage-meter-${meter.name}'));

  final UsageMeter meter;
  final List<UsageRow> rows;
  final Sprint? sprint;

  @override
  Widget build(BuildContext context) {
    final l = AppLocalizations.of(context);
    final theme = Theme.of(context);
    final colors = StatusColors.of(theme);
    final bars = UsageChart.bars(rows, meter);
    final bands = UsageChart.bands(rows, meter);
    final projection = sprint == null ? null : UsageChart.projection(rows, sprint!, meter);
    final over = <double>[
      for (final s in [...bars, ...bands, ?projection])
        if (UsageChart.overHundred(s.to)) s.to,
    ];
    final names = <String>{
      for (final s in [...bars, ...bands, ?projection]) s.block,
    };
    String nameOf(String id) => sprint?.block(id)?.name ?? id;
    return Padding(
      padding: const EdgeInsets.only(bottom: DashboardLayout.gap),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(meter == UsageMeter.session ? l.dshMeterSession : l.dshMeterWeek, style: theme.textTheme.labelMedium),
          const SizedBox(height: 2),
          SizedBox(
            height: DashboardLayout.meterHeight,
            child: Stack(children: [
              Positioned.fill(
                child: CustomPaint(
                  painter: _MeterPainter(
                    bars: bars,
                    bands: bands,
                    projection: projection,
                    over: over.isNotEmpty,
                    track: theme.colorScheme.surfaceContainerHigh,
                    data: colors.run,
                    mark: theme.colorScheme.onSurface,
                    overColor: colors.warn,
                  ),
                ),
              ),
              if (over.isNotEmpty)
                Positioned(
                  right: 0,
                  top: 0,
                  bottom: 0,
                  width: 18,
                  child: Tooltip(
                    key: Key('usage-over-${meter.name}'),
                    message: [for (final v in over) PointsFormat.format(v)].join(', '),
                    child: const SizedBox.expand(),
                  ),
                ),
            ]),
          ),
          if (names.isNotEmpty)
            Wrap(
              spacing: DashboardLayout.gap,
              children: [for (final n in names) Text(nameOf(n), style: theme.textTheme.labelSmall, overflow: TextOverflow.ellipsis)],
            ),
        ],
      ),
    );
  }
}

class _MeterPainter extends CustomPainter {
  _MeterPainter({
    required this.bars,
    required this.bands,
    required this.projection,
    required this.over,
    required this.track,
    required this.data,
    required this.mark,
    required this.overColor,
  });

  final List<UsageSpan> bars;
  final List<UsageSpan> bands;
  final UsageSpan? projection;
  final bool over;
  final Color track;
  final Color data;
  final Color mark;
  final Color overColor;

  double _x(double value, double width) => UsageChart.position(value) / UsageChart.scaleMax * width;

  void _span(Canvas canvas, Size size, UsageSpan s, Paint paint, {double inset = 0}) {
    final a = _x(s.from < s.to ? s.from : s.to, size.width);
    final b = _x(s.from < s.to ? s.to : s.from, size.width);
    canvas.drawRect(Rect.fromLTRB(a, inset, b < a + 1 ? a + 1 : b, size.height - inset), paint);
  }

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRRect(RRect.fromRectAndRadius(Offset.zero & size, const Radius.circular(3)), Paint()..color = track);
    final band = Paint()..color = data.withValues(alpha: 0.25);
    for (final s in bands) {
      _span(canvas, size, s, band);
    }
    final bar = Paint()..color = data;
    for (final s in bars) {
      _span(canvas, size, s, bar, inset: size.height * 0.25);
    }
    final p = projection;
    if (p != null) {
      _span(canvas, size, p, Paint()..color = data.withValues(alpha: 0.5), inset: size.height * 0.1);
      final x = _x(p.to, size.width);
      canvas.drawLine(Offset(x, 0), Offset(x, size.height), Paint()..color = mark..strokeWidth = 2);
    }
    if (over) {
      final path = Path()
        ..moveTo(size.width, 0)
        ..lineTo(size.width - 10, size.height / 2)
        ..lineTo(size.width, size.height)
        ..close();
      canvas.drawPath(path, Paint()..color = overColor);
    }
  }

  @override
  bool shouldRepaint(_MeterPainter old) =>
      old.bars != bars || old.bands != bands || old.projection != projection || old.over != over || old.data != data || old.track != track;
}
