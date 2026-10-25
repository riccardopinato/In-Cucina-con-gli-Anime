import 'package:flutter/material.dart';

enum DecorativeCulture {
  japanese,
  chinese,
}

enum DecorativeMotion {
  float,
  peek,
  sway,
}

enum DecorativeSlot {
  exploreHero,
  favoritesEmpty,
  shoppingEmpty,
  searchEmpty,
  wideEditorialGap,
  recipeCardCorner,
}

class DecorativeCharacterDefinition {
  const DecorativeCharacterDefinition({
    required this.id,
    required this.name,
    required this.culture,
    required this.motion,
    required this.slots,
    required this.bodyColor,
    required this.secondaryColor,
    required this.accentColor,
  });

  final String id;
  final String name;
  final DecorativeCulture culture;
  final DecorativeMotion motion;
  final Set<DecorativeSlot> slots;
  final Color bodyColor;
  final Color secondaryColor;
  final Color accentColor;
}

abstract final class DecorativeCharacterRegistry {
  static const characters = <DecorativeCharacterDefinition>[
    DecorativeCharacterDefinition(
      id: 'kitsune',
      name: 'Kitsune',
      culture: DecorativeCulture.japanese,
      motion: DecorativeMotion.float,
      slots: {
        DecorativeSlot.exploreHero,
        DecorativeSlot.searchEmpty,
        DecorativeSlot.wideEditorialGap,
        DecorativeSlot.recipeCardCorner,
      },
      bodyColor: Color(0xFFE68A45),
      secondaryColor: Color(0xFFFFF4DE),
      accentColor: Color(0xFF9C4A2D),
    ),
    DecorativeCharacterDefinition(
      id: 'kappa',
      name: 'Kappa',
      culture: DecorativeCulture.japanese,
      motion: DecorativeMotion.peek,
      slots: {
        DecorativeSlot.shoppingEmpty,
        DecorativeSlot.searchEmpty,
        DecorativeSlot.wideEditorialGap,
        DecorativeSlot.recipeCardCorner,
      },
      bodyColor: Color(0xFF79A85A),
      secondaryColor: Color(0xFFDCE7A7),
      accentColor: Color(0xFF4C7D65),
    ),
    DecorativeCharacterDefinition(
      id: 'tanuki',
      name: 'Tanuki',
      culture: DecorativeCulture.japanese,
      motion: DecorativeMotion.sway,
      slots: {
        DecorativeSlot.favoritesEmpty,
        DecorativeSlot.shoppingEmpty,
        DecorativeSlot.exploreHero,
        DecorativeSlot.recipeCardCorner,
      },
      bodyColor: Color(0xFF9B7559),
      secondaryColor: Color(0xFFE7D3B8),
      accentColor: Color(0xFF4F3A31),
    ),
    DecorativeCharacterDefinition(
      id: 'oni',
      name: 'Oni',
      culture: DecorativeCulture.japanese,
      motion: DecorativeMotion.sway,
      slots: {
        DecorativeSlot.exploreHero,
        DecorativeSlot.wideEditorialGap,
        DecorativeSlot.recipeCardCorner,
      },
      bodyColor: Color(0xFFD96657),
      secondaryColor: Color(0xFFF4D48A),
      accentColor: Color(0xFF653A52),
    ),
    DecorativeCharacterDefinition(
      id: 'sun_wukong',
      name: 'Sun Wukong',
      culture: DecorativeCulture.chinese,
      motion: DecorativeMotion.float,
      slots: {
        DecorativeSlot.exploreHero,
        DecorativeSlot.favoritesEmpty,
        DecorativeSlot.wideEditorialGap,
        DecorativeSlot.recipeCardCorner,
      },
      bodyColor: Color(0xFFA96A3F),
      secondaryColor: Color(0xFFE7BC68),
      accentColor: Color(0xFFB8483D),
    ),
    DecorativeCharacterDefinition(
      id: 'chinese_dragon',
      name: 'Chinese Dragon',
      culture: DecorativeCulture.chinese,
      motion: DecorativeMotion.sway,
      slots: {
        DecorativeSlot.exploreHero,
        DecorativeSlot.shoppingEmpty,
        DecorativeSlot.wideEditorialGap,
        DecorativeSlot.recipeCardCorner,
      },
      bodyColor: Color(0xFF4C8E76),
      secondaryColor: Color(0xFFF1D389),
      accentColor: Color(0xFFC64F48),
    ),
  ];

  static final Map<DecorativeSlot, String> _lastBySlot = {};
  static String? _lastGlobalId;

  static List<DecorativeCharacterDefinition> compatibleWith(
    DecorativeSlot slot,
  ) {
    return characters
        .where((character) => character.slots.contains(slot))
        .toList(growable: false);
  }

  static DecorativeCharacterDefinition pick(
    DecorativeSlot slot, {
    int? entropy,
  }) {
    final candidates = compatibleWith(slot);
    assert(candidates.isNotEmpty, 'No decorative character for $slot.');

    final value = entropy ?? DateTime.now().microsecondsSinceEpoch;
    var index = value.abs() % candidates.length;
    var selected = candidates[index];

    if (candidates.length > 1 &&
        (selected.id == _lastBySlot[slot] ||
            selected.id == _lastGlobalId)) {
      index = (index + 1) % candidates.length;
      selected = candidates[index];

      if (candidates.length > 2 &&
          selected.id == _lastGlobalId) {
        selected = candidates[(index + 1) % candidates.length];
      }
    }

    _lastBySlot[slot] = selected.id;
    _lastGlobalId = selected.id;
    return selected;
  }

  @visibleForTesting
  static void resetSelectionMemory() {
    _lastBySlot.clear();
    _lastGlobalId = null;
  }
}
