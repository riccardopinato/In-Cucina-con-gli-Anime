import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import 'app_design_tokens.dart';
import 'app_palette.dart';

abstract final class AppTheme {
  static ThemeData light() => _build(Brightness.light);
  static ThemeData dark() => _build(Brightness.dark);

  static ThemeData _build(Brightness brightness) {
    final isDark = brightness == Brightness.dark;
    final base = ThemeData(
      useMaterial3: true,
      brightness: brightness,
    );

    final baseScheme = ColorScheme.fromSeed(
      seedColor: AppPalette.meadow,
      brightness: brightness,
    );

    final colors = baseScheme.copyWith(
      primary: AppPalette.meadow,
      secondary: AppPalette.ember,
      tertiary: AppPalette.plum,
      surface: isDark ? AppPalette.nightPaper : AppPalette.ricePaper,
      surfaceContainerLowest:
          isDark ? AppPalette.nightPaper : AppPalette.ricePaper,
      surfaceContainerLow:
          isDark ? AppPalette.nightRaised : AppPalette.washi,
      surfaceContainer:
          isDark ? const Color(0xFF272A21) : const Color(0xFFF2EBDD),
      outlineVariant:
          isDark ? const Color(0xFF44483D) : const Color(0xFFE1D8C8),
    );

    final textTheme = base.textTheme.copyWith(
      displayMedium: GoogleFonts.caveat(
        fontSize: 46,
        fontWeight: FontWeight.w700,
        height: 0.98,
        color: colors.onSurface,
      ),
      headlineLarge: base.textTheme.headlineLarge?.copyWith(
        fontWeight: FontWeight.w800,
        letterSpacing: -0.8,
        height: 1.04,
      ),
      headlineMedium: base.textTheme.headlineMedium?.copyWith(
        fontWeight: FontWeight.w800,
        letterSpacing: -0.45,
      ),
      titleLarge: base.textTheme.titleLarge?.copyWith(
        fontWeight: FontWeight.w800,
        letterSpacing: -0.25,
      ),
      titleMedium: base.textTheme.titleMedium?.copyWith(
        fontWeight: FontWeight.w700,
      ),
      labelLarge: base.textTheme.labelLarge?.copyWith(
        fontWeight: FontWeight.w700,
      ),
    );

    return base.copyWith(
      colorScheme: colors,
      scaffoldBackgroundColor: colors.surface,
      textTheme: textTheme,
      appBarTheme: AppBarTheme(
        centerTitle: false,
        backgroundColor: colors.surface.withValues(alpha: 0.94),
        foregroundColor: colors.onSurface,
        surfaceTintColor: Colors.transparent,
        elevation: AppElevation.none,
        scrolledUnderElevation: AppElevation.none,
        titleTextStyle: GoogleFonts.caveat(
          fontSize: 30,
          fontWeight: FontWeight.w700,
          color: colors.onSurface,
          height: 1,
        ),
      ),
      cardTheme: CardThemeData(
        color: colors.surfaceContainerLow,
        elevation: AppElevation.card,
        margin: EdgeInsets.zero,
        clipBehavior: Clip.antiAlias,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadii.container),
          side: BorderSide(
            color: colors.outlineVariant.withValues(alpha: 0.72),
          ),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: colors.surfaceContainerLow,
        contentPadding: const EdgeInsets.symmetric(
          horizontal: AppSpacing.medium,
          vertical: 15,
        ),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadii.card),
          borderSide: BorderSide.none,
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadii.card),
          borderSide: BorderSide(
            color: colors.outlineVariant.withValues(alpha: 0.78),
          ),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppRadii.card),
          borderSide: BorderSide(color: colors.primary, width: 1.6),
        ),
      ),
      chipTheme: ChipThemeData(
        backgroundColor: colors.surfaceContainerLow,
        selectedColor: isDark
            ? colors.primaryContainer
            : AppPalette.matchaMist,
        side: BorderSide(
          color: colors.outlineVariant.withValues(alpha: 0.72),
        ),
        shape: const StadiumBorder(),
        labelStyle: textTheme.labelMedium?.copyWith(
          fontWeight: FontWeight.w700,
        ),
        padding: const EdgeInsets.symmetric(
          horizontal: AppSpacing.small,
          vertical: 2,
        ),
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
          textStyle: textTheme.labelLarge,
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          minimumSize: const Size(
            AppLayout.minInteractiveSize,
            AppLayout.minInteractiveSize,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppRadii.card),
          ),
          side: BorderSide(color: colors.outlineVariant),
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
        backgroundColor: colors.surfaceContainerLow,
        indicatorColor: isDark
            ? colors.primaryContainer
            : AppPalette.matchaMist,
        elevation: AppElevation.none,
        surfaceTintColor: Colors.transparent,
        labelTextStyle: WidgetStatePropertyAll(
          textTheme.labelMedium?.copyWith(fontWeight: FontWeight.w700),
        ),
      ),
      navigationRailTheme: NavigationRailThemeData(
        backgroundColor: colors.surfaceContainerLow,
        indicatorColor: isDark
            ? colors.primaryContainer
            : AppPalette.matchaMist,
        labelType: NavigationRailLabelType.all,
        useIndicator: true,
        selectedLabelTextStyle: textTheme.labelMedium?.copyWith(
          fontWeight: FontWeight.w800,
        ),
      ),
      bottomSheetTheme: BottomSheetThemeData(
        backgroundColor: colors.surface,
        surfaceTintColor: Colors.transparent,
        showDragHandle: true,
        shape: const RoundedRectangleBorder(
          borderRadius: BorderRadius.vertical(
            top: Radius.circular(AppRadii.container),
          ),
        ),
      ),
      dialogTheme: DialogThemeData(
        backgroundColor: colors.surface,
        surfaceTintColor: Colors.transparent,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadii.container),
        ),
      ),
      dividerTheme: DividerThemeData(
        color: colors.outlineVariant.withValues(alpha: 0.72),
      ),
    );
  }
}
