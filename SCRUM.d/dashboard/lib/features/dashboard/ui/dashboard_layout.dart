// Holds: the layout constants of the dashboard widgets (spacing, widths, the dash for a missing value).
// Depends on: nothing. Used by: the dashboard widgets. Reads or writes: nothing.

/// Layout numbers; colors and fonts come from the theme.
class DashboardLayout {
  const DashboardLayout._();

  static const double gap = 8;
  static const double filterWidth = 180;
  static const String dash = '-';
}
