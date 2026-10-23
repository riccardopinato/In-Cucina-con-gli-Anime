import 'consent.dart';

abstract interface class ConsentRepository {
  ConsentState load();

  Future<void> saveLocalPreference(AdPrivacyPreference preference);

  Future<void> clearLocalPreference();
}
