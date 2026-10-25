import 'dart:async';

import 'package:flutter/material.dart';

import '../../../../core/decorative_characters/decorative_character_registry.dart';
import '../../../../core/decorative_characters/decorative_character_stage.dart';
import '../../../../core/theme/app_design_tokens.dart';

class RecipeCardMascotPeek extends StatefulWidget {
  const RecipeCardMascotPeek({
    super.key,
    required this.recipeId,
    required this.celebrationToken,
    this.size = 58,
  });

  final String recipeId;
  final int celebrationToken;
  final double size;

  @visibleForTesting
  static bool isPassiveCandidate(String recipeId) {
    final match = RegExp(r'(\d+)$').firstMatch(recipeId);
    final ordinal = int.tryParse(match?.group(1) ?? '');
    if (ordinal != null) {
      return ordinal % 6 == 3;
    }

    final checksum = recipeId.codeUnits.fold<int>(
      0,
      (value, unit) => value + unit,
    );
    return checksum % 6 == 0;
  }

  @override
  State<RecipeCardMascotPeek> createState() => _RecipeCardMascotPeekState();
}

class _RecipeCardMascotPeekState extends State<RecipeCardMascotPeek> {
  Timer? _showTimer;
  Timer? _hideTimer;
  bool _visible = false;
  int _appearanceSerial = 0;

  bool get _reduceMotion =>
      MediaQuery.maybeOf(context)?.disableAnimations ?? false;

  int get _entropy {
    final match = RegExp(r'(\d+)$').firstMatch(widget.recipeId);
    return int.tryParse(match?.group(1) ?? '') ??
        widget.recipeId.codeUnits.fold<int>(
          0,
          (value, unit) => value + unit,
        );
  }

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (mounted) {
        _schedulePassive(initial: true);
      }
    });
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (_reduceMotion) {
      _showTimer?.cancel();
      _hideTimer?.cancel();
      if (_visible) {
        setState(() => _visible = false);
      }
      return;
    }

    if (!_visible &&
        RecipeCardMascotPeek.isPassiveCandidate(widget.recipeId) &&
        _showTimer == null) {
      _schedulePassive(initial: true);
    }
  }

  @override
  void didUpdateWidget(covariant RecipeCardMascotPeek oldWidget) {
    super.didUpdateWidget(oldWidget);

    if (oldWidget.recipeId != widget.recipeId) {
      _showTimer?.cancel();
      _hideTimer?.cancel();
      _visible = false;
      _schedulePassive(initial: true);
    }

    if (widget.celebrationToken > oldWidget.celebrationToken) {
      _showFor(const Duration(milliseconds: 1500));
    }
  }

  void _schedulePassive({required bool initial}) {
    _showTimer?.cancel();
    _showTimer = null;

    if (_reduceMotion ||
        !RecipeCardMascotPeek.isPassiveCandidate(widget.recipeId)) {
      return;
    }

    final delay = initial
        ? Duration(milliseconds: 850 + ((_entropy % 5) * 180))
        : Duration(milliseconds: 7000 + ((_entropy % 4) * 900));

    _showTimer = Timer(delay, () {
      _showTimer = null;
      if (!mounted || _reduceMotion) {
        return;
      }
      _showFor(const Duration(milliseconds: 2100));
    });
  }

  void _showFor(Duration duration) {
    _showTimer?.cancel();
    _showTimer = null;
    _hideTimer?.cancel();

    if (!mounted || _reduceMotion) {
      return;
    }

    setState(() {
      _visible = true;
      _appearanceSerial += 1;
    });

    _hideTimer = Timer(duration, () {
      if (!mounted) {
        return;
      }
      setState(() => _visible = false);
      _schedulePassive(initial: false);
    });
  }

  @override
  void dispose() {
    _showTimer?.cancel();
    _hideTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_reduceMotion) {
      return const SizedBox.shrink();
    }

    return IgnorePointer(
      child: SizedBox.square(
        dimension: widget.size,
        child: AnimatedSwitcher(
          duration: AppMotion.standard,
          reverseDuration: AppMotion.feedback,
          switchInCurve: AppMotion.standardCurve,
          switchOutCurve: Curves.easeInCubic,
          transitionBuilder: (child, animation) {
            final slide = Tween<Offset>(
              begin: const Offset(0, 0.42),
              end: Offset.zero,
            ).animate(
              CurvedAnimation(
                parent: animation,
                curve: AppMotion.standardCurve,
              ),
            );

            return FadeTransition(
              opacity: animation,
              child: SlideTransition(
                position: slide,
                child: child,
              ),
            );
          },
          child: _visible
              ? DecorativeCharacterStage(
                  key: ValueKey(
                    'recipe-card-mascot-${widget.recipeId}-$_appearanceSerial',
                  ),
                  slot: DecorativeSlot.recipeCardCorner,
                  size: widget.size,
                  entropy: _entropy + _appearanceSerial,
                )
              : const SizedBox.shrink(
                  key: ValueKey('recipe-card-mascot-hidden'),
                ),
        ),
      ),
    );
  }
}
