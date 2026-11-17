import 'package:domain/domain.dart';
import 'package:test/test.dart';

void main() {
  // RUL-21: the limits (S52-07..11 use these)
  test('RUL-21 limits match the Python app', () {
    expect(maxConditions, 12);
    expect(maxActions, 6);
    expect(maxRules, 60);
  });
  test('RUL-11 action types', () {
    expect(actionTypes.keys, containsAll(['color', 'emoji', 'event', 'change', 'add', 'move', 'delete', 'changes']));
    expect(linkActions, ['delete', 'move']);
  });
  test('color pattern', () {
    expect(colorPattern.hasMatch('#039be5'), isTrue);
    expect(colorPattern.hasMatch('#03be5'), isFalse);
  });
}
