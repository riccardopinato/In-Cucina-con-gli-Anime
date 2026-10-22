import 'package:flutter/material.dart';

import 'decorative_character_registry.dart';

class DecorativeCharacterStage extends StatefulWidget {
  const DecorativeCharacterStage({
    super.key,
    required this.slot,
    this.size = 124,
    this.entropy,
  });

  final DecorativeSlot slot;
  final double size;
  final int? entropy;

  @override
  State<DecorativeCharacterStage> createState() =>
      _DecorativeCharacterStageState();
}

class _DecorativeCharacterStageState
    extends State<DecorativeCharacterStage>
    with SingleTickerProviderStateMixin {
  late DecorativeCharacterDefinition _character;
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _character = DecorativeCharacterRegistry.pick(
      widget.slot,
      entropy: widget.entropy,
    );
    _controller = AnimationController(
      vsync: this,
      duration: _durationFor(_character.motion),
    );
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _syncMotionPreference();
  }

  void _syncMotionPreference() {
    final reduceMotion =
        MediaQuery.maybeOf(context)?.disableAnimations ?? false;
    if (reduceMotion) {
      _controller
        ..stop()
        ..value = 0.5;
      return;
    }
    if (!_controller.isAnimating) {
      _controller.repeat(reverse: true);
    }
  }

  @override
  void didUpdateWidget(covariant DecorativeCharacterStage oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.slot != widget.slot ||
        oldWidget.entropy != widget.entropy) {
      _character = DecorativeCharacterRegistry.pick(
        widget.slot,
        entropy: widget.entropy,
      );
      _controller
        ..duration = _durationFor(_character.motion)
        ..reset();
      _syncMotionPreference();
    }
  }

  Duration _durationFor(DecorativeMotion motion) {
    return switch (motion) {
      DecorativeMotion.float => const Duration(milliseconds: 2600),
      DecorativeMotion.peek => const Duration(milliseconds: 2200),
      DecorativeMotion.sway => const Duration(milliseconds: 3000),
    };
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final reduceMotion =
        MediaQuery.maybeOf(context)?.disableAnimations ?? false;

    final artwork = ExcludeSemantics(
      child: DecorativeCharacterArtwork(
        definition: _character,
        size: widget.size,
      ),
    );

    if (reduceMotion) {
      return artwork;
    }

    return AnimatedBuilder(
      animation: _controller,
      child: artwork,
      builder: (context, child) {
        final t = Curves.easeInOut.transform(_controller.value);

        return switch (_character.motion) {
          DecorativeMotion.float => Transform.translate(
              offset: Offset(0, -4 + (8 * t)),
              child: child,
            ),
          DecorativeMotion.peek => Transform.translate(
              offset: Offset(0, 7 - (9 * t)),
              child: Transform.scale(
                scale: 0.96 + (0.04 * t),
                alignment: Alignment.bottomCenter,
                child: child,
              ),
            ),
          DecorativeMotion.sway => Transform.rotate(
              angle: -0.045 + (0.09 * t),
              alignment: Alignment.bottomCenter,
              child: child,
            ),
        };
      },
    );
  }
}

class DecorativeCharacterArtwork extends StatelessWidget {
  const DecorativeCharacterArtwork({
    super.key,
    required this.definition,
    required this.size,
  });

  final DecorativeCharacterDefinition definition;
  final double size;

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return SizedBox.square(
      dimension: size,
      child: CustomPaint(
        painter: _DecorativeCharacterPainter(
          definition: definition,
          outline: isDark
              ? colors.onSurface.withValues(alpha: 0.72)
              : const Color(0xFF3D3A34),
          shadow: Colors.black.withValues(alpha: isDark ? 0.20 : 0.10),
        ),
      ),
    );
  }
}

class _DecorativeCharacterPainter extends CustomPainter {
  const _DecorativeCharacterPainter({
    required this.definition,
    required this.outline,
    required this.shadow,
  });

  final DecorativeCharacterDefinition definition;
  final Color outline;
  final Color shadow;

  @override
  void paint(Canvas canvas, Size size) {
    final scale = size.shortestSide / 120;
    canvas.save();
    canvas.scale(scale, scale);

    final shadowPaint = Paint()..color = shadow;
    canvas.drawOval(
      const Rect.fromLTWH(26, 101, 68, 11),
      shadowPaint,
    );

    switch (definition.id) {
      case 'kitsune':
        _paintKitsune(canvas);
        break;
      case 'kappa':
        _paintKappa(canvas);
        break;
      case 'tanuki':
        _paintTanuki(canvas);
        break;
      case 'oni':
        _paintOni(canvas);
        break;
      case 'sun_wukong':
        _paintMonkeyKing(canvas);
        break;
      case 'chinese_dragon':
        _paintDragon(canvas);
        break;
      default:
        _paintFallback(canvas);
        break;
    }

    canvas.restore();
  }

  Paint get _body => Paint()..color = definition.bodyColor;
  Paint get _secondary => Paint()..color = definition.secondaryColor;
  Paint get _accent => Paint()..color = definition.accentColor;

  Paint get _line => Paint()
    ..color = outline
    ..style = PaintingStyle.stroke
    ..strokeWidth = 2.2
    ..strokeCap = StrokeCap.round
    ..strokeJoin = StrokeJoin.round;

  void _paintKitsune(Canvas canvas) {
    final tail = Path()
      ..moveTo(82, 82)
      ..cubicTo(112, 69, 111, 101, 89, 104)
      ..cubicTo(102, 91, 91, 87, 82, 82);
    canvas.drawPath(tail, _body);
    canvas.drawPath(tail, _line);

    final leftEar = Path()
      ..moveTo(38, 35)
      ..lineTo(45, 10)
      ..lineTo(59, 38)
      ..close();
    final rightEar = Path()
      ..moveTo(64, 38)
      ..lineTo(80, 11)
      ..lineTo(86, 41)
      ..close();
    canvas.drawPath(leftEar, _body);
    canvas.drawPath(rightEar, _body);
    canvas.drawPath(leftEar, _line);
    canvas.drawPath(rightEar, _line);

    canvas.drawCircle(const Offset(61, 62), 31, _body);
    canvas.drawCircle(const Offset(61, 62), 31, _line);
    canvas.drawOval(
      const Rect.fromLTWH(43, 60, 36, 27),
      _secondary,
    );

    final eyeLeft = Path()
      ..moveTo(45, 55)
      ..quadraticBezierTo(51, 59, 57, 55);
    final eyeRight = Path()
      ..moveTo(65, 55)
      ..quadraticBezierTo(71, 59, 77, 55);
    canvas.drawPath(eyeLeft, _line);
    canvas.drawPath(eyeRight, _line);
    canvas.drawCircle(const Offset(61, 70), 2.3, _accent);
  }

  void _paintKappa(Canvas canvas) {
    canvas.drawCircle(const Offset(61, 66), 31, _body);
    canvas.drawCircle(const Offset(61, 66), 31, _line);

    canvas.drawOval(
      const Rect.fromLTWH(39, 20, 44, 14),
      _secondary,
    );
    canvas.drawOval(
      const Rect.fromLTWH(39, 20, 44, 14),
      _line,
    );
    canvas.drawOval(
      const Rect.fromLTWH(44, 24, 34, 8),
      Paint()..color = const Color(0xFF8FC5D8),
    );

    final beak = Path()
      ..moveTo(51, 68)
      ..lineTo(71, 68)
      ..lineTo(61, 78)
      ..close();
    canvas.drawPath(beak, Paint()..color = const Color(0xFFE4A75E));
    canvas.drawPath(beak, _line);

    canvas.drawCircle(const Offset(49, 58), 2.6, _accent);
    canvas.drawCircle(const Offset(73, 58), 2.6, _accent);

    final shell = Path()
      ..moveTo(38, 84)
      ..quadraticBezierTo(60, 103, 83, 84)
      ..quadraticBezierTo(61, 94, 38, 84);
    canvas.drawPath(shell, _secondary);
    canvas.drawPath(shell, _line);
  }

  void _paintTanuki(Canvas canvas) {
    final tail = Path()
      ..moveTo(83, 75)
      ..cubicTo(111, 60, 113, 92, 88, 100)
      ..cubicTo(98, 84, 94, 78, 83, 75);
    canvas.drawPath(tail, _body);
    canvas.drawPath(tail, _line);
    canvas.drawLine(const Offset(92, 74), const Offset(102, 93), _line);

    canvas.drawOval(
      const Rect.fromLTWH(33, 38, 56, 63),
      _body,
    );
    canvas.drawOval(
      const Rect.fromLTWH(33, 38, 56, 63),
      _line,
    );

    canvas.drawCircle(const Offset(45, 41), 9, _body);
    canvas.drawCircle(const Offset(77, 41), 9, _body);
    canvas.drawCircle(const Offset(45, 41), 9, _line);
    canvas.drawCircle(const Offset(77, 41), 9, _line);

    canvas.drawOval(
      const Rect.fromLTWH(39, 50, 18, 15),
      _accent,
    );
    canvas.drawOval(
      const Rect.fromLTWH(65, 50, 18, 15),
      _accent,
    );
    canvas.drawCircle(const Offset(48, 56), 2.2, _secondary);
    canvas.drawCircle(const Offset(74, 56), 2.2, _secondary);

    canvas.drawOval(
      const Rect.fromLTWH(45, 67, 32, 24),
      _secondary,
    );
    canvas.drawCircle(const Offset(61, 72), 2.4, _accent);
  }

  void _paintOni(Canvas canvas) {
    final hornLeft = Path()
      ..moveTo(42, 35)
      ..lineTo(44, 12)
      ..lineTo(55, 36)
      ..close();
    final hornRight = Path()
      ..moveTo(68, 35)
      ..lineTo(78, 12)
      ..lineTo(81, 39)
      ..close();
    canvas.drawPath(hornLeft, _secondary);
    canvas.drawPath(hornRight, _secondary);
    canvas.drawPath(hornLeft, _line);
    canvas.drawPath(hornRight, _line);

    canvas.drawCircle(const Offset(61, 64), 33, _body);
    canvas.drawCircle(const Offset(61, 64), 33, _line);

    canvas.drawLine(const Offset(42, 50), const Offset(55, 46), _line);
    canvas.drawLine(const Offset(67, 46), const Offset(80, 50), _line);
    canvas.drawCircle(const Offset(50, 57), 2.8, _accent);
    canvas.drawCircle(const Offset(72, 57), 2.8, _accent);

    final mouth = Path()
      ..moveTo(47, 74)
      ..quadraticBezierTo(61, 84, 76, 74);
    canvas.drawPath(mouth, _line);

    final tuskLeft = Path()
      ..moveTo(51, 76)
      ..lineTo(54, 85)
      ..lineTo(58, 77)
      ..close();
    final tuskRight = Path()
      ..moveTo(65, 77)
      ..lineTo(69, 85)
      ..lineTo(72, 76)
      ..close();
    canvas.drawPath(tuskLeft, _secondary);
    canvas.drawPath(tuskRight, _secondary);
  }

  void _paintMonkeyKing(Canvas canvas) {
    final staff = Paint()
      ..color = const Color(0xFF8E5638)
      ..strokeWidth = 5
      ..strokeCap = StrokeCap.round;
    canvas.drawLine(const Offset(93, 18), const Offset(86, 103), staff);
    canvas.drawCircle(const Offset(61, 64), 31, _body);
    canvas.drawCircle(const Offset(61, 64), 31, _line);
    canvas.drawCircle(const Offset(34, 63), 10, _body);
    canvas.drawCircle(const Offset(88, 63), 10, _body);

    canvas.drawOval(
      const Rect.fromLTWH(43, 47, 36, 37),
      _secondary,
    );
    canvas.drawOval(
      const Rect.fromLTWH(43, 47, 36, 37),
      _line,
    );

    final band = Paint()
      ..color = definition.accentColor
      ..strokeWidth = 6
      ..strokeCap = StrokeCap.round;
    canvas.drawLine(const Offset(39, 43), const Offset(83, 43), band);

    canvas.drawCircle(const Offset(51, 59), 2.5, _accent);
    canvas.drawCircle(const Offset(71, 59), 2.5, _accent);
    final smile = Path()
      ..moveTo(53, 72)
      ..quadraticBezierTo(61, 77, 69, 72);
    canvas.drawPath(smile, _line);
  }

  void _paintDragon(Canvas canvas) {
    final bodyPaint = Paint()
      ..color = definition.bodyColor
      ..style = PaintingStyle.stroke
      ..strokeWidth = 18
      ..strokeCap = StrokeCap.round;

    final body = Path()
      ..moveTo(18, 82)
      ..cubicTo(33, 48, 55, 104, 74, 68)
      ..cubicTo(86, 45, 96, 55, 103, 40);
    canvas.drawPath(body, bodyPaint);
    canvas.drawPath(
      body,
      Paint()
        ..color = outline
        ..style = PaintingStyle.stroke
        ..strokeWidth = 2.2,
    );

    canvas.drawCircle(const Offset(96, 37), 18, _body);
    canvas.drawCircle(const Offset(96, 37), 18, _line);

    final hornA = Path()
      ..moveTo(86, 23)
      ..lineTo(83, 10)
      ..lineTo(91, 20);
    final hornB = Path()
      ..moveTo(102, 21)
      ..lineTo(108, 9)
      ..lineTo(108, 24);
    canvas.drawPath(hornA, _line);
    canvas.drawPath(hornB, _line);

    canvas.drawCircle(const Offset(91, 35), 2.3, _accent);
    canvas.drawCircle(const Offset(102, 34), 2.3, _accent);

    final whiskerLeft = Path()
      ..moveTo(86, 45)
      ..cubicTo(70, 46, 72, 56, 62, 58);
    final whiskerRight = Path()
      ..moveTo(106, 45)
      ..cubicTo(119, 48, 115, 57, 120, 59);
    canvas.drawPath(whiskerLeft, _line);
    canvas.drawPath(whiskerRight, _line);

    for (var i = 0; i < 4; i++) {
      canvas.drawCircle(
        Offset(29 + (i * 17), 77 - (i.isEven ? 7 : 0)),
        3.5,
        _secondary,
      );
    }
  }

  void _paintFallback(Canvas canvas) {
    canvas.drawCircle(const Offset(61, 62), 31, _body);
    canvas.drawCircle(const Offset(61, 62), 31, _line);
    canvas.drawCircle(const Offset(50, 58), 2.5, _accent);
    canvas.drawCircle(const Offset(72, 58), 2.5, _accent);
  }

  @override
  bool shouldRepaint(covariant _DecorativeCharacterPainter oldDelegate) {
    return oldDelegate.definition != definition ||
        oldDelegate.outline != outline ||
        oldDelegate.shadow != shadow;
  }
}
