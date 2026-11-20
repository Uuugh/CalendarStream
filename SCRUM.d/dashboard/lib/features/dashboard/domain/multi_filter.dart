// Holds: the multi-select filter of the Requirements and Issues columns (DSH-04, UIC-21): a set of selected choices out
// of a list of choices. Depends on: nothing. Used by: the page, FilterStore users. Reads or writes: nothing.

/// An immutable filter over [choices]. Every choice starts selected; an entry is listed when its value is selected.
class MultiFilter {
  /// All of [choices] selected.
  MultiFilter(List<String> choices) : this._(choices, {...choices});

  /// [choices] with the stored selection [stored] kept where it still applies; null (nothing stored) selects all.
  MultiFilter.restore(List<String> choices, List<String>? stored)
      : this._(choices, stored == null ? {...choices} : {for (final c in choices) if (stored.contains(c)) c});

  const MultiFilter._(this.choices, this.selected);

  final List<String> choices;
  final Set<String> selected;

  /// True when some choice is not selected, so the filter hides something (UIC-21).
  bool get isActive => choices.any((c) => !selected.contains(c));

  bool isSelected(String choice) => selected.contains(choice);

  /// Only [choice] selected.
  MultiFilter only(String choice) => MultiFilter._(choices, choices.contains(choice) ? {choice} : {});

  /// [choice] selected when it was not, not selected when it was.
  MultiFilter toggle(String choice) {
    if (!choices.contains(choice)) return this;
    final next = {...selected};
    if (!next.remove(choice)) next.add(choice);
    return MultiFilter._(choices, next);
  }

  MultiFilter selectAll() => MultiFilter._(choices, {...choices});

  MultiFilter selectNone() => MultiFilter._(choices, {});

  /// The same selection over [newChoices]: choices that stay keep their state, and new choices are selected when
  /// nothing was hidden before.
  MultiFilter withChoices(List<String> newChoices) {
    final wasAll = !isActive;
    return MultiFilter._(newChoices, {for (final c in newChoices) if (selected.contains(c) || (wasAll && !choices.contains(c))) c});
  }

  /// True when an entry whose value is [value] is listed. An entry with no value (null) is listed only when nothing is hidden.
  bool matches(String? value) => value == null ? !isActive : selected.contains(value);

  /// The entries of [items] whose [valueOf] is selected, in order.
  List<T> apply<T>(List<T> items, String? Function(T) valueOf) => [
        for (final i in items)
          if (matches(valueOf(i))) i
      ];

  /// The selected choices in the order of [choices], the form a [FilterStore] keeps.
  List<String> get selectedList => [for (final c in choices) if (selected.contains(c)) c];
}
