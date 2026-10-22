import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../../domain/recipe.dart';

class RecipeArtwork extends StatelessWidget {
  const RecipeArtwork({
    super.key,
    required this.recipe,
    this.showReference = false,
    this.borderRadius = BorderRadius.zero,
  });

  final Recipe recipe;
  final bool showReference;
  final BorderRadius borderRadius;

  @override
  Widget build(BuildContext context) {
    final visual = _RecipeVisual.forRecipe(recipe);
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final start = isDark
        ? Color.lerp(visual.start, Colors.black, 0.42)!
        : visual.start;
    final end = isDark
        ? Color.lerp(visual.end, Colors.black, 0.34)!
        : visual.end;
    final ink = isDark ? Colors.white : visual.ink;

    return ClipRRect(
      borderRadius: borderRadius,
      child: DecoratedBox(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [start, end],
          ),
        ),
        child: Stack(
          fit: StackFit.expand,
          children: [
            CustomPaint(
              painter: _RecipePatternPainter(
                ink: ink.withValues(alpha: isDark ? 0.12 : 0.10),
                accent: visual.accent.withValues(alpha: isDark ? 0.34 : 0.42),
              ),
            ),
            Positioned(
              left: 22,
              top: 18,
              child: Text(
                visual.number,
                style: Theme.of(context).textTheme.labelLarge?.copyWith(
                      color: ink.withValues(alpha: 0.72),
                      fontWeight: FontWeight.w800,
                      letterSpacing: 2.2,
                    ),
              ),
            ),
            Align(
              alignment: const Alignment(0.45, 0.12),
              child: Container(
                width: 116,
                height: 116,
                decoration: BoxDecoration(
                  color: Colors.white.withValues(
                    alpha: isDark ? 0.10 : 0.46,
                  ),
                  shape: BoxShape.circle,
                  border: Border.all(
                    color: ink.withValues(alpha: 0.12),
                  ),
                ),
                child: Icon(
                  visual.icon,
                  size: 58,
                  color: ink.withValues(alpha: 0.88),
                ),
              ),
            ),
            if (showReference)
              Positioned(
                left: 20,
                right: 20,
                bottom: 18,
                child: Align(
                  alignment: Alignment.bottomLeft,
                  child: Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 12,
                      vertical: 7,
                    ),
                    decoration: BoxDecoration(
                      color: Colors.black.withValues(
                        alpha: isDark ? 0.30 : 0.54,
                      ),
                      borderRadius: BorderRadius.circular(999),
                    ),
                    child: Text(
                      recipe.animeSource,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: Theme.of(context).textTheme.labelMedium?.copyWith(
                            color: Colors.white,
                            fontWeight: FontWeight.w700,
                          ),
                    ),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}

class _RecipeVisual {
  const _RecipeVisual({
    required this.number,
    required this.start,
    required this.end,
    required this.ink,
    required this.accent,
    required this.icon,
  });

  final String number;
  final Color start;
  final Color end;
  final Color ink;
  final Color accent;
  final IconData icon;

  static _RecipeVisual forRecipe(Recipe recipe) {
    final match = RegExp(r'(\d+)$').firstMatch(recipe.id);
    final ordinal = int.tryParse(match?.group(1) ?? '') ?? 1;
    final index = (ordinal - 1) % _visuals.length;
    final base = _visuals[index];

    return _RecipeVisual(
      number: ordinal.toString().padLeft(2, '0'),
      start: base.start,
      end: base.end,
      ink: base.ink,
      accent: base.accent,
      icon: base.icon,
    );
  }

  static const _visuals = <_RecipeVisual>[
    _RecipeVisual(
      number: '01',
      start: Color(0xFFF6D6B8),
      end: Color(0xFFF8EEE1),
      ink: Color(0xFF5C342A),
      accent: Color(0xFFE07A5F),
      icon: Icons.egg_alt_rounded,
    ),
    _RecipeVisual(
      number: '02',
      start: Color(0xFFF0C98A),
      end: Color(0xFFF7E7C6),
      ink: Color(0xFF4B372A),
      accent: Color(0xFFB65A3A),
      icon: Icons.ramen_dining_rounded,
    ),
    _RecipeVisual(
      number: '03',
      start: Color(0xFFD9E8C7),
      end: Color(0xFFF3EBD2),
      ink: Color(0xFF304A32),
      accent: Color(0xFF6A8F5B),
      icon: Icons.rice_bowl_rounded,
    ),
    _RecipeVisual(
      number: '04',
      start: Color(0xFFF5D3A7),
      end: Color(0xFFF8EFE2),
      ink: Color(0xFF5B3C2A),
      accent: Color(0xFFD99A4E),
      icon: Icons.bakery_dining_rounded,
    ),
    _RecipeVisual(
      number: '05',
      start: Color(0xFFBFD9D2),
      end: Color(0xFFE8F0E6),
      ink: Color(0xFF294943),
      accent: Color(0xFF4A7C59),
      icon: Icons.takeout_dining_rounded,
    ),
    _RecipeVisual(
      number: '06',
      start: Color(0xFFD3DFC1),
      end: Color(0xFFF2E7CE),
      ink: Color(0xFF39482F),
      accent: Color(0xFF788B5B),
      icon: Icons.local_dining_rounded,
    ),
    _RecipeVisual(
      number: '07',
      start: Color(0xFFC6DCEA),
      end: Color(0xFFF4E1C8),
      ink: Color(0xFF27495A),
      accent: Color(0xFF4C8EAA),
      icon: Icons.soup_kitchen_rounded,
    ),
    _RecipeVisual(
      number: '08',
      start: Color(0xFFF3CC8E),
      end: Color(0xFFF9E9CB),
      ink: Color(0xFF5A4023),
      accent: Color(0xFFD78732),
      icon: Icons.egg_rounded,
    ),
    _RecipeVisual(
      number: '09',
      start: Color(0xFFE8D9B9),
      end: Color(0xFFD7E3C5),
      ink: Color(0xFF435039),
      accent: Color(0xFF6F845A),
      icon: Icons.dinner_dining_rounded,
    ),
    _RecipeVisual(
      number: '10',
      start: Color(0xFFD5C7E6),
      end: Color(0xFFF1E2CC),
      ink: Color(0xFF493C57),
      accent: Color(0xFF8D6DA8),
      icon: Icons.kitchen_rounded,
    ),
  ];
}

class _RecipePatternPainter extends CustomPainter {
  const _RecipePatternPainter({
    required this.ink,
    required this.accent,
  });

  final Color ink;
  final Color accent;

  @override
  void paint(Canvas canvas, Size size) {
    final stroke = Paint()
      ..color = ink
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.4;

    final accentPaint = Paint()
      ..color = accent
      ..style = PaintingStyle.fill;

    canvas.drawCircle(
      Offset(size.width * 0.84, size.height * 0.18),
      math.min(size.width, size.height) * 0.17,
      accentPaint,
    );

    for (var i = 0; i < 4; i++) {
      final y = size.height * (0.18 + i * 0.18);
      final path = Path()
        ..moveTo(-12, y)
        ..cubicTo(
          size.width * 0.20,
          y - 22,
          size.width * 0.32,
          y + 22,
          size.width * 0.52,
          y,
        );
      canvas.drawPath(path, stroke);
    }

    final chopstickPaint = Paint()
      ..color = ink
      ..strokeWidth = 3
      ..strokeCap = StrokeCap.round;
    canvas.drawLine(
      Offset(size.width * 0.76, size.height * 0.64),
      Offset(size.width * 1.04, size.height * 0.39),
      chopstickPaint,
    );
    canvas.drawLine(
      Offset(size.width * 0.82, size.height * 0.70),
      Offset(size.width * 1.08, size.height * 0.48),
      chopstickPaint,
    );
  }

  @override
  bool shouldRepaint(covariant _RecipePatternPainter oldDelegate) {
    return oldDelegate.ink != ink || oldDelegate.accent != accent;
  }
}
