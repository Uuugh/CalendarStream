/// Source URL rules, separated from networking so clients cannot silently
/// bypass them. The eventual downloader must validate every redirect.
class CalendarSourcePolicy {
  static const int maxResponseBytes = 5 * 1024 * 1024;
  static const int maxRedirects = 5;
  static const Duration connectTimeout = Duration(seconds: 20);
  static const Duration totalTimeout = Duration(seconds: 60);

  static Uri validateUrl(String value) {
    final uri = Uri.tryParse(value);
    if (uri == null ||
        uri.scheme.toLowerCase() != 'https' ||
        uri.host.isEmpty ||
        uri.userInfo.isNotEmpty ||
        uri.hasFragment) {
      throw const FormatException(
        'Calendar URLs must be HTTPS without embedded credentials or fragments.',
      );
    }
    return uri;
  }

  /// Never forward Basic-auth credentials to a different origin.
  static bool mayForwardCredentials(Uri original, Uri target) {
    return original.scheme.toLowerCase() == 'https' &&
        target.scheme.toLowerCase() == 'https' &&
        original.host.toLowerCase() == target.host.toLowerCase() &&
        original.port == target.port;
  }
}
