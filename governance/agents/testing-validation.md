# Testing and validation

Prefer tests at the highest stable seam:
- authoring behaviour through deterministic Python tools;
- catalog behaviour through the catalog interface;
- user-state persistence through repositories/notifiers;
- entitlement decisions through ProductLimits;
- UI smoke/widget tests for navigation/content states.

Baseline validation:
- `python3 tool/validate_structure.py`
- `python3 tool/compile_recipe_catalog.py --check`
- `python3 -m unittest discover -s tool/tests -p 'test_*.py'`
- `python3 tool/validate_recipe_catalog.py`
- `flutter analyze`
- `flutter test`
- `python3 tool/build_recipe_preview.py`
- `flutter build web --release`

F2 completion also requires that the synthetic preview command restores the production catalog and that production authoring/runtime still contain zero real recipes.

Android runtime/AppLab, physical-device and store evidence are separate gates. A green build is not feature certification.
