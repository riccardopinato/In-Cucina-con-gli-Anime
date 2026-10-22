import 'package:flutter/material.dart';

abstract final class AppSpacing {
  static const xSmall = 4.0;
  static const small = 8.0;
  static const medium = 16.0;
  static const large = 24.0;
  static const xLarge = 32.0;
  static const xxLarge = 48.0;
  static const xxxLarge = 64.0;
}

abstract final class AppRadii {
  static const small = 10.0;
  static const card = 22.0;
  static const container = 28.0;
  static const hero = 34.0;
  static const pill = 999.0;
}

abstract final class AppElevation {
  static const none = 0.0;
  static const card = 0.0;
}

abstract final class AppLayout {
  static const minInteractiveSize = 48.0;
  static const navigationBarHeight = 76.0;
  static const railBreakpoint = 840.0;
  static const contentMaxWidth = 1240.0;
  static const detailMaxWidth = 1080.0;
}

abstract final class AppMotion {
  static const feedback = Duration(milliseconds: 150);
  static const standard = Duration(milliseconds: 260);
  static const entrance = Duration(milliseconds: 420);
  static const standardCurve = Curves.easeOutCubic;
}
