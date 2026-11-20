// Holds: the web backend: an HttpBackend through the server at the page's origin (DSH-01.e). Depends on:
// JsHttpTransport, HttpBackend. Used by: DashboardBackend (web builds only; no dart:io). Reads or writes: network.

import 'dashboard_backend.dart';
import 'http_backend.dart';
import 'js_http_transport.dart';

DashboardBackend createPlatformBackend() => const HttpBackend(JsHttpTransport());
