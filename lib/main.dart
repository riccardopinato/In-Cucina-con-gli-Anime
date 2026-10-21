import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'app.dart';
import 'core/persistence/shared_preferences_provider.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final preferences = await SharedPreferences.getInstance();
  final overrides = [sharedPreferencesProvider.overrideWithValue(preferences)];
  runApp(ProviderScope(overrides: overrides, child: const AnimeKitchenApp()));
}
