import 'package:flutter/material.dart';

abstract final class AppSpacing {
  static const xSmall = 4.0;
  static const small = 8.0;
  static const medium = 16.0;
  static const large = 24.0;
  static const xLarge = 32.0;
  static const xxLarge = 48.0;
}

abstract final class AppRadii {
  static const small = 8.0;
  static const card = 16.0;
  static const container = 20.0;
  static const hero = 28.0;
}

abstract final class AppElevation {
  static const none = 0.0;
  static const card = 1.0;
}

abstract final class AppLayout {
  static const minInteractiveSize = 48.0;
  static const navigationBarHeight = 80.0;
  static const railBreakpoint = 840.0;
  static const contentMaxWidth = 1180.0;
}

abstract final class AppMotion {
  static const feedback = Duration(milliseconds: 160);
  static const standard = Duration(milliseconds: 240);
  static const standardCurve = Curves.easeInOut;
}
