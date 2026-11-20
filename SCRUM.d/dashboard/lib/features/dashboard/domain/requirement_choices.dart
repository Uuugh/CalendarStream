// Holds: the dropdown dependency of the New issue form (DSH-08.a): which requirements a feature offers.
// Depends on: Requirement. Used by: the New issue dialog. Reads or writes: nothing.

import 'requirement.dart';

/// Pure choices for the feature and requirement dropdowns.
class RequirementChoices {
  const RequirementChoices._();

  /// The features of [requirements], without repeats, in order of first appearance.
  static List<String> features(Iterable<Requirement> requirements) => [
        for (final f in {for (final r in requirements) r.feature}) f,
      ];

  /// The IDs of the requirements of [feature]; none when [feature] is null (DSH-08.a).
  static List<String> requirementsOf(Iterable<Requirement> requirements, String? feature) => [
        if (feature != null)
          for (final r in requirements)
            if (r.feature == feature) r.id,
      ];

  /// [requirement] when [feature] offers it, otherwise null: choosing another feature clears it (DSH-08.a).
  static String? keepRequirement(Iterable<Requirement> requirements, String? feature, String? requirement) =>
      requirementsOf(requirements, feature).contains(requirement) ? requirement : null;
}
