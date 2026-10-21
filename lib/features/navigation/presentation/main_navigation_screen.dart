import 'package:flutter/material.dart';

import '../../../core/widgets/responsive_destination_shell.dart';
import '../../../l10n/app_localizations.dart';
import '../../favorites/presentation/favorites_screen.dart';
import '../../recipes/presentation/screens/recipe_list_screen.dart';
import '../../settings/presentation/settings_screen.dart';
import '../../shopping/presentation/shopping_list_screen.dart';

class MainNavigationScreen extends StatefulWidget {
  const MainNavigationScreen({super.key});

  @override
  State<MainNavigationScreen> createState() => _MainNavigationScreenState();
}

class _MainNavigationScreenState extends State<MainNavigationScreen> {
  int _selectedIndex = 0;

  static const _screens = <Widget>[
    RecipeListScreen(),
    FavoritesScreen(),
    ShoppingListScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    final destinations = <NavigationDestination>[
      NavigationDestination(
        icon: const Icon(Icons.restaurant_menu_outlined),
        selectedIcon: const Icon(Icons.restaurant_menu),
        label: l10n.navRecipes,
      ),
      NavigationDestination(
        icon: const Icon(Icons.favorite_outline),
        selectedIcon: const Icon(Icons.favorite),
        label: l10n.navFavorites,
      ),
      NavigationDestination(
        icon: const Icon(Icons.shopping_bag_outlined),
        selectedIcon: const Icon(Icons.shopping_bag),
        label: l10n.navShopping,
      ),
    ];

    return ResponsiveDestinationShell(
      selectedIndex: _selectedIndex,
      onDestinationSelected: (index) {
        setState(() => _selectedIndex = index);
      },
      destinations: destinations,
      title: l10n.appName,
      actions: [
        IconButton(
          tooltip: l10n.settingsTitle,
          icon: const Icon(Icons.settings_outlined),
          onPressed: () {
            Navigator.of(context).push(
              MaterialPageRoute<void>(
                builder: (_) => const SettingsScreen(),
              ),
            );
          },
        ),
      ],
      body: IndexedStack(
        index: _selectedIndex,
        children: _screens,
      ),
    );
  }
}
