from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

required = [
    ROOT / "APP_BOOTSTRAP.yaml",
    ROOT / "AGENTS.md",
    ROOT / "ROADMAP.md",
    ROOT / "docs" / "PRODUCT_BIBLE.md",
    ROOT / "docs" / "CONTENT_RIGHTS_POLICY.md",
    ROOT / "docs" / "RECIPE_CATALOG_CONTRACT.md",
    ROOT / "docs" / "RECIPE_AUTHORING_PIPELINE.md",
    ROOT / "docs" / "GOLDEN_REUSE_MANIFEST.txt",
    ROOT / "lib" / "main.dart",
    ROOT / "lib" / "core" / "theme" / "app_theme.dart",
    ROOT
    / "lib"
    / "features"
    / "recipes"
    / "data"
    / "versioned_recipe_catalog_repository.dart",
    ROOT / "assets" / "catalog" / "manifest.json",
    ROOT / "assets" / "catalog" / "recipes.json",
    ROOT / "authoring" / "catalog.json",
    ROOT / "authoring" / "schema" / "recipe_authoring.schema.json",
    ROOT / "authoring" / "assets" / "manifest.json",
    ROOT / "authoring" / "config" / "similarity_policy.json",
    ROOT / "authoring" / "reviews" / "decisions.json",
    ROOT / "authoring" / "templates" / "recipe.template.json",
    ROOT / "authoring" / "fixtures" / "fixture_noodles.json",
    ROOT / "tool" / "recipe_authoring_lib.py",
    ROOT / "tool" / "compile_recipe_catalog.py",
    ROOT / "tool" / "review_recipe_similarity.py",
    ROOT / "tool" / "build_recipe_preview.py",
    ROOT / "tool" / "validate_recipe_catalog.py",
    ROOT / "tool" / "tests" / "test_recipe_authoring.py",
    ROOT
    / "lib"
    / "features"
    / "recipes"
    / "presentation"
    / "widgets"
    / "recipe_artwork.dart",
    ROOT / "test" / "recipe_visual_identity_test.dart",
    ROOT
    / "lib"
    / "core"
    / "decorative_characters"
    / "decorative_character_registry.dart",
    ROOT
    / "lib"
    / "core"
    / "decorative_characters"
    / "decorative_character_stage.dart",
    ROOT / "test" / "decorative_character_system_test.dart",
]

missing = [
    str(path.relative_to(ROOT))
    for path in required
    if not path.exists()
]
if missing:
    raise SystemExit(
        f"Missing required files: {', '.join(missing)}"
    )

arb_dir = ROOT / "lib" / "l10n"
arb_files = sorted(arb_dir.glob("app_*.arb"))
if len(arb_files) != 6:
    raise SystemExit(
        f"Expected 6 ARB files, found {len(arb_files)}"
    )

key_sets = {}
for path in arb_files:
    payload = json.loads(
        path.read_text(encoding="utf-8")
    )
    key_sets[path.name] = {
        key
        for key in payload
        if not key.startswith("@")
    }

template = key_sets["app_en.arb"]
for name, keys in key_sets.items():
    if keys != template:
        raise SystemExit(
            f"{name} localization keys do not "
            "match app_en.arb"
        )

production_authoring = sorted(
    (ROOT / "authoring" / "recipes").glob("*.json")
)
if not production_authoring:
    raise SystemExit("Production authoring catalog is empty")

authoring_ids = set()
for path in production_authoring:
    payload = json.loads(path.read_text(encoding="utf-8"))
    recipe_id = payload.get("id")
    if recipe_id in authoring_ids:
        raise SystemExit(f"Duplicate authoring recipe id: {recipe_id}")
    authoring_ids.add(recipe_id)

expected_recipe_ids = {
    f"recipe_{index:06d}"
    for index in range(1, len(production_authoring) + 1)
}
if authoring_ids != expected_recipe_ids:
    raise SystemExit(
        "Production authoring IDs must form one contiguous stable sequence "
        f"from recipe_000001 to recipe_{len(production_authoring):06d}"
    )

catalog = json.loads(
    (
        ROOT / "assets" / "catalog" / "recipes.json"
    ).read_text(encoding="utf-8")
)
runtime_recipes = catalog.get("recipes")
if (
    not isinstance(runtime_recipes, list)
    or len(runtime_recipes) != len(production_authoring)
):
    raise SystemExit(
        "Runtime catalog recipe count must match production authoring: "
        f"{len(production_authoring)} expected"
    )

runtime_ids = {
    recipe.get("id")
    for recipe in runtime_recipes
    if isinstance(recipe, dict)
}
if runtime_ids != authoring_ids:
    raise SystemExit(
        "Runtime recipe IDs do not match production authoring IDs"
    )

for forbidden in (
    "calcifer_bacon",
    "ichiraku_ramen",
    "ponyo_ramen",
    "totoro_bento",
):
    for path in (ROOT / "lib").rglob("*.dart"):
        if forbidden in path.read_text(
            encoding="utf-8"
        ).lower():
            raise SystemExit(
                "Flutter source contains recipe data marker "
                f"{forbidden}: {path}"
            )

print("Structure validation PASS")
