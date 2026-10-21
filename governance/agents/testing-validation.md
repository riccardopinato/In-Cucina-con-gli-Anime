# Testing and validation

Prefer tests at the highest stable seam:
- catalog behaviour through the catalog interface;
- user-state persistence through repositories/notifiers;
- entitlement decisions through ProductLimits;
- UI smoke/widget tests for navigation and empty states.

Baseline validation:
- `python3 tool/validate_structure.py`
- `flutter analyze`
- `flutter test`
- `flutter build web --release`

Android runtime/AppLab and store evidence are separate gates. A green build is not feature certification.
