import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import 'app_design_tokens.dart';
import 'app_palette.dart';

abstract final class AppTheme {
  static ThemeData light() => _build(Brightness.light);
  static ThemeData dark() => _build(Brightness.dark);

  static ThemeData _build(Brightness brightness) {
    final baseScheme = ColorScheme.fromSeed(
      seedColor: AppPalette.meadow,
      brightness: brightness,
    );

    final colors = baseScheme.copyWith(
      primary: AppPalette.meadow,
      secondary: AppPalette.ember,
      tertiary: AppPalette.skyWash,
      surface: brightness == Brightness.light
          ? AppPalette.ricePaper
          : const Color(0xFF171915),
    );

    final baseText = ThemeData(
      useMaterial3: true,
      brightness: brightness,
      colorScheme: colors,
    ).textTheme;

    final roundedText = GoogleFonts.nunitoTextTheme(baseText);
    final typography = roundedText.copyWith(
      displaySmall: GoogleFonts.caveat(
        textStyle: roundedText.displaySmall,
        fontWeight: FontWeight.w700,
        height: 1.05,
      ),
      headlineMedium: GoogleFonts.caveat(
        textStyle: roundedText.headlineMedium,
        fontWeight: FontWeight.w700,
        height: 1.1,
      ),
      titleLarge: roundedText.titleLarge?.copyWith(
        fontWeight: FontWeight.w800,
      ),
      titleMedium: roundedText.titleMedium?.copyWith(
        fontWeight: FontWeight.w700,
      ),
      bodyLarge: roundedText.bodyLarge?.copyWith(height: 1.5),
      bodyMedium: roundedText.bodyMedium?.copyWith(height: 1.45),
      labelMedium: roundedText.labelMedium?.copyWith(
        fontWeight: FontWeight.w700,
      ),
    );

    return ThemeData(
      useMaterial3: true,
      brightness: brightness,
      colorScheme: colors,
      textTheme: typography,
      scaffoldBackgroundColor: colors.surface,
      appBarTheme: AppBarTheme(
        centerTitle: false,
        backgroundColor: colors.surface,
        foregroundColor: colors.onSurface,
        surfaceTintColor: colors.surface,
        elevation: AppElevation.none,
        scrolledUnderElevation: AppElevation.none,
        titleTextStyle: typography.titleLarge?.copyWith(
          color: colors.onSurface,
        ),
      ),
      cardTheme: CardThemeData(
        color: colors.surfaceContainerLow,
        elevation: AppElevation.card,
        margin: EdgeInsets.zero,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadii.container),
          side: BorderSide(color: colors.outlineVariant),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: colors.surfaceContainerLow,
        contentPadding: const EdgeInsets.symmetric(
          horizontal: AppSpacing.medium,
          vertical: 14,
        ),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadii.card),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadii.card),
          borderSide: BorderSide(color: colors.outlineVariant),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadii.card),
          borderSide: BorderSide(color: colors.primary, width: 2),
        ),
      ),
      chipTheme: ChipThemeData(
        backgroundColor: colors.surfaceContainerLow,
        selectedColor: colors.secondaryContainer,
        side: BorderSide(color: colors.outlineVariant),
        shape: const StadiumBorder(),
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          minimumSize: const Size(
            AppLayout.minInteractiveSize,
            AppLayout.minInteractiveSize,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppRadii.card),
          ),
        ),
      ),
      iconButtonTheme: IconButtonThemeData(
        style: IconButton.styleFrom(
          minimumSize: const Size(
            AppLayout.minInteractiveSize,
            AppLayout.minInteractiveSize,
          ),
        ),
      ),
      navigationBarTheme: NavigationBarThemeData(
        height: AppLayout.navigationBarHeight,
        backgroundColor: colors.surface,
        indicatorColor: colors.secondaryContainer,
        elevation: AppElevation.none,
        surfaceTintColor: colors.surface,
      ),
      navigationRailTheme: NavigationRailThemeData(
        backgroundColor: colors.surface,
        indicatorColor: colors.secondaryContainer,
        labelType: NavigationRailLabelType.all,
        useIndicator: true,
      ),
      bottomSheetTheme: BottomSheetThemeData(
        backgroundColor: colors.surface,
        surfaceTintColor: colors.surface,
        showDragHandle: true,
        shape: const RoundedRectangleBorder(
          borderRadius: BorderRadius.vertical(
            top: Radius.circular(AppRadii.container),
          ),
        ),
      ),
      dialogTheme: DialogThemeData(
        backgroundColor: colors.surface,
        surfaceTintColor: colors.surface,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadii.container),
        ),
      ),
    );
  }
}
