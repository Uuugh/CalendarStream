// Holds: the file access the repositories use, so tests can pass a fake or a temp dir.
// Depends on: nothing. Used by: SprintRepository, RequirementRepository.
// Reads or writes: nothing itself; implementations read and write files.

/// Text-file access. Paths use forward slashes.
abstract class FileAccess {
  /// The text of the file, or null when it does not exist.
  Future<String?> read(String path);

  /// Writes the file, creating it and its folders when missing.
  Future<void> write(String path, String content);

  /// Paths of the files directly in [dir]; empty when the folder does not exist.
  Future<List<String>> listFiles(String dir);

  /// Paths of the folders directly in [dir]; empty when the folder does not exist.
  Future<List<String>> listDirectories(String dir);
}
