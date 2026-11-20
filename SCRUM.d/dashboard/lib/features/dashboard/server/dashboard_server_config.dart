// Holds: the DEF-01 values of the server (DSH-13.a), written once. Depends on: nothing.
// Used by: DashboardServer, bin/dashboard_server.dart. Reads or writes: nothing.

/// Where the server listens: this machine only.
class DashboardServerConfig {
  const DashboardServerConfig._();

  /// The address the server binds (DSH-13.a).
  static const host = '127.0.0.1';

  /// The port the server listens on (DSH-13.a).
  static const port = 8765;
}
