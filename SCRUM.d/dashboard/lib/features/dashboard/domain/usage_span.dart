// Holds: one drawn span of a usage meter (DSH-14.c, DSH-14.d, DSH-14.e). Depends on: nothing.
// Used by: UsageChart, the chart. Reads or writes: nothing.

/// A span of block [block] on a 0 to 100 meter from [from] to [to]. A band has [low], where the estimate's range
/// starts; a bar and a projection have none. Values are the real numbers and may be above 100 (DSH-14.f).
class UsageSpan {
  const UsageSpan(this.block, this.from, this.to, {this.low});

  final String block;
  final double from;
  final double to;
  final double? low;
}
