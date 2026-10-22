import 'package:animekitchen/core/decorative_characters/decorative_character_registry.dart';
import 'package:animekitchen/core/decorative_characters/decorative_character_stage.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  tearDown(DecorativeCharacterRegistry.resetSelectionMemory);

  test('registry covers cultures, motions and contextual slots', () {
    final cultures = DecorativeCharacterRegistry.characters
        .map((character) => character.culture)
        .toSet();
    final motions = DecorativeCharacterRegistry.characters
        .map((character) => character.motion)
        .toSet();

    expect(
      cultures,
      containsAll([
        DecorativeCulture.japanese,
        DecorativeCulture.chinese,
      ]),
    );
    expect(
      motions,
      containsAll([
        DecorativeMotion.float,
        DecorativeMotion.peek,
        DecorativeMotion.sway,
      ]),
    );

    for (final slot in DecorativeSlot.values) {
      expect(
        DecorativeCharacterRegistry.compatibleWith(slot),
        isNotEmpty,
        reason: 'Every decorative slot must have at least one candidate.',
      );
    }
  });

  test('selector prevents immediate repetition for the same context', () {
    DecorativeCharacterRegistry.resetSelectionMemory();

    final first = DecorativeCharacterRegistry.pick(
      DecorativeSlot.exploreHero,
      entropy: 0,
    );
    final second = DecorativeCharacterRegistry.pick(
      DecorativeSlot.exploreHero,
      entropy: 0,
    );

    expect(second.id, isNot(first.id));
  });

  testWidgets('all original procedural archetypes render', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SingleChildScrollView(
            child: Column(
              children: [
                for (final character
                    in DecorativeCharacterRegistry.characters)
                  DecorativeCharacterArtwork(
                    definition: character,
                    size: 96,
                  ),
              ],
            ),
          ),
        ),
      ),
    );

    expect(
      find.byType(DecorativeCharacterArtwork),
      findsNWidgets(DecorativeCharacterRegistry.characters.length),
    );
    expect(tester.takeException(), isNull);
  });

  testWidgets('stage respects reduced-motion mode', (tester) async {
    DecorativeCharacterRegistry.resetSelectionMemory();

    await tester.pumpWidget(
      const MaterialApp(
        home: MediaQuery(
          data: MediaQueryData(disableAnimations: true),
          child: Scaffold(
            body: Center(
              child: DecorativeCharacterStage(
                slot: DecorativeSlot.shoppingEmpty,
                size: 120,
                entropy: 4,
              ),
            ),
          ),
        ),
      ),
    );

    await tester.pump(const Duration(seconds: 1));

    expect(find.byType(DecorativeCharacterStage), findsOneWidget);
    expect(find.byType(DecorativeCharacterArtwork), findsOneWidget);
    expect(tester.takeException(), isNull);
  });
}
