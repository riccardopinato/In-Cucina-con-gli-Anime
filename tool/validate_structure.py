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
expected_recipe_ids = {
    f"recipe_{index:06d}"
    for index in range(1, 11)
}
if len(production_authoring) != 10:
    raise SystemExit(
        "F3A must contain exactly 10 production authoring "
        f"recipes, found {len(production_authoring)}"
    )

authoring_ids = set()
for path in production_authoring:
    payload = json.loads(path.read_text(encoding="utf-8"))
    recipe_id = payload.get("id")
    if recipe_id in authoring_ids:
        raise SystemExit(f"Duplicate authoring recipe id: {recipe_id}")
    authoring_ids.add(recipe_id)

if authoring_ids != expected_recipe_ids:
    raise SystemExit(
        "F3A authoring IDs do not match expected ten-recipe batch IDs"
    )

catalog = json.loads(
    (
        ROOT / "assets" / "catalog" / "recipes.json"
    ).read_text(encoding="utf-8")
)
runtime_recipes = catalog.get("recipes")
if not isinstance(runtime_recipes, list) or len(runtime_recipes) != 10:
    raise SystemExit(
        "F3A runtime catalog must contain exactly 10 recipes"
    )

runtime_ids = {
    recipe.get("id")
    for recipe in runtime_recipes
    if isinstance(recipe, dict)
}
if runtime_ids != expected_recipe_ids:
    raise SystemExit(
        "F3A runtime recipe IDs do not match authoring IDs"
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
