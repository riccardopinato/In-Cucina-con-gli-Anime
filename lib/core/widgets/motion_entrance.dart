import 'package:flutter/material.dart';

import '../theme/app_design_tokens.dart';

class MotionEntrance extends StatelessWidget {
  const MotionEntrance({
    super.key,
    required this.child,
    this.distance = 8,
  });

  final Widget child;
  final double distance;

  @override
  Widget build(BuildContext context) {
    final reduceMotion =
        MediaQuery.maybeOf(context)?.disableAnimations ?? false;

    if (reduceMotion) {
      return child;
    }

    return TweenAnimationBuilder<double>(
      tween: Tween<double>(begin: 0, end: 1),
      duration: AppMotion.entrance,
      curve: AppMotion.standardCurve,
      child: child,
      builder: (context, value, child) {
        return Opacity(
          opacity: value,
          child: Transform.translate(
            offset: Offset(0, distance * (1 - value)),
            child: child,
          ),
        );
      },
    );
  }
}
