import 'package:animekitchen/core/decorative_characters/decorative_character_stage.dart';
import 'package:animekitchen/core/widgets/motion_entrance.dart';
import 'package:animekitchen/features/recipes/presentation/widgets/animated_favorite_button.dart';
import 'package:animekitchen/features/recipes/presentation/widgets/recipe_card_mascot_peek.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('recipe card passive mascots stay sparse and deterministic', () {
    final visible = [
      for (var index = 1; index <= 60; index++)
        if (RecipeCardMascotPeek.isPassiveCandidate(
          'recipe_${index.toString().padLeft(6, '0')}',
        ))
          index,
    ];

    expect(visible.length, 10);
    expect(visible, everyElement(predicate<int>((value) => value % 6 == 3)));
  });

  testWidgets('recipe card mascot is suppressed by reduced motion',
      (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: MediaQuery(
          data: MediaQueryData(disableAnimations: true),
          child: Scaffold(
            body: RecipeCardMascotPeek(
              recipeId: 'recipe_000003',
              celebrationToken: 1,
            ),
          ),
        ),
      ),
    );

    await tester.pump(const Duration(seconds: 2));

    expect(find.byType(DecorativeCharacterStage), findsNothing);
  });

  testWidgets('passive mascot peeks on an eligible recipe card',
      (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: RecipeCardMascotPeek(
            recipeId: 'recipe_000003',
            celebrationToken: 0,
          ),
        ),
      ),
    );

    await tester.pump(const Duration(seconds: 2));

    expect(find.byType(DecorativeCharacterStage), findsOneWidget);

    await tester.pumpWidget(const SizedBox.shrink());
  });

  testWidgets('motion entrance bypasses tweening in reduced-motion mode',
      (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: MediaQuery(
          data: MediaQueryData(disableAnimations: true),
          child: MotionEntrance(
            child: Text('Ready'),
          ),
        ),
      ),
    );

    expect(find.text('Ready'), findsOneWidget);
    expect(find.byType(TweenAnimationBuilder<double>), findsNothing);
  });

  testWidgets('favorite action stays functional in reduced-motion mode',
      (tester) async {
    var pressed = false;

    await tester.pumpWidget(
      MaterialApp(
        home: MediaQuery(
          data: const MediaQueryData(disableAnimations: true),
          child: Scaffold(
            body: AnimatedFavoriteButton(
              isFavorite: false,
              onPressed: () => pressed = true,
            ),
          ),
        ),
      ),
    );

    await tester.tap(find.byIcon(Icons.favorite_border));
    await tester.pump();

    expect(pressed, isTrue);
  });
}
