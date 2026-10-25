from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG_DIR = ROOT / "assets" / "catalog"
MANIFEST_PATH = CATALOG_DIR / "manifest.json"
SUPPORTED_SCHEMA_VERSION = 1
APP_LOCALES = {"en", "it", "es", "fr", "de", "pt"}
ID_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


def load_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"Missing file: {path.relative_to(ROOT)}")
        return None
    except json.JSONDecodeError as exc:
        errors.append(
            f"Invalid JSON {path.relative_to(ROOT)}: line {exc.lineno}, col {exc.colno}"
        )
        return None
    if not isinstance(data, dict):
        errors.append(f"{path.relative_to(ROOT)} must contain a JSON object")
        return None
    return data


def app_path(value: Any, label: str, errors: list[str]) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} must be a non-empty string")
        return None
    path = (ROOT / value).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError:
        errors.append(f"{label} escapes repository root")
        return None
    return path


def is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_recipe(
    recipe: Any,
    index: int,
    ids: set[str],
    errors: list[str],
) -> tuple[str | None, set[str], set[str]]:
    label = f"recipes[{index}]"
    if not isinstance(recipe, dict):
        errors.append(f"{label} must be an object")
        return None, set(), set()

    recipe_id = recipe.get("id")
    if not non_empty_string(recipe_id) or not ID_RE.fullmatch(recipe_id):
        errors.append(f"{label}.id is invalid")
        return None, set(), set()
    if recipe_id in ids:
        errors.append(f"Duplicate recipe id: {recipe_id}")
    ids.add(recipe_id)

    version = recipe.get("contentVersion")
    if not is_int(version) or version < 1:
        errors.append(f"{recipe_id}.contentVersion must be an integer >= 1")

    if recipe.get("status") not in {"draft", "published", "archived"}:
        errors.append(f"{recipe_id}.status is invalid")

    if not non_empty_string(recipe.get("inspirationTitle")):
        errors.append(f"{recipe_id}.inspirationTitle is required")

    anime_references = recipe.get("animeReferences", [])
    if not isinstance(anime_references, list):
        errors.append(f"{recipe_id}.animeReferences must be an array")
    else:
        for position, reference in enumerate(anime_references):
            ref_label = f"{recipe_id}.animeReferences[{position}]"
            if not isinstance(reference, dict):
                errors.append(f"{ref_label} must be an object")
                continue
            if not non_empty_string(reference.get("workTitle")):
                errors.append(f"{ref_label}.workTitle is required")
            if reference.get("relation") not in {
                "verified_appearance",
                "recurring_association",
                "inspired",
                "unverified",
            }:
                errors.append(f"{ref_label}.relation is invalid")
            season = reference.get("season")
            if season is not None and (
                not is_int(season) or season < 1
            ):
                errors.append(
                    f"{ref_label}.season must be null or integer >= 1"
                )
            for key in ("episode", "chapter"):
                value = reference.get(key)
                if value is not None and not isinstance(value, str):
                    errors.append(
                        f"{ref_label}.{key} must be null or string"
                    )

    for field in ("prepMinutes", "cookMinutes"):
        value = recipe.get(field)
        if not is_int(value) or value < 0:
            errors.append(f"{recipe_id}.{field} must be an integer >= 0")

    servings = recipe.get("servings")
    if not is_int(servings) or servings < 1:
        errors.append(f"{recipe_id}.servings must be an integer >= 1")

    if recipe.get("difficulty") not in {"easy", "medium", "hard"}:
        errors.append(f"{recipe_id}.difficulty is invalid")

    if recipe.get("contentOrigin") not in {"original", "inspired", "adapted"}:
        errors.append(f"{recipe_id}.contentOrigin is invalid")

    for field in ("sourceNote", "imageAsset"):
        value = recipe.get(field)
        if value is not None and not isinstance(value, str):
            errors.append(f"{recipe_id}.{field} must be null or a string")

    image_asset = recipe.get("imageAsset")
    if isinstance(image_asset, str) and image_asset.strip():
        image_path = app_path(image_asset, f"{recipe_id}.imageAsset", errors)
        if image_path is not None and not image_path.is_file():
            errors.append(f"{recipe_id}.imageAsset does not exist: {image_asset}")

    ingredient_ids: set[str] = set()
    ingredients = recipe.get("ingredients")
    if not isinstance(ingredients, list) or not ingredients:
        errors.append(f"{recipe_id}.ingredients must be a non-empty array")
    else:
        for position, ingredient in enumerate(ingredients):
            item_label = f"{recipe_id}.ingredients[{position}]"
            if not isinstance(ingredient, dict):
                errors.append(f"{item_label} must be an object")
                continue
            item_id = ingredient.get("id")
            if not non_empty_string(item_id) or not ID_RE.fullmatch(item_id):
                errors.append(f"{item_label}.id is invalid")
                continue
            if item_id in ingredient_ids:
                errors.append(f"{recipe_id} duplicate ingredient id: {item_id}")
            ingredient_ids.add(item_id)
            quantity = ingredient.get("quantity")
            if quantity is not None:
                if isinstance(quantity, bool) or not isinstance(quantity, (int, float)):
                    errors.append(f"{item_label}.quantity must be numeric or null")
                elif quantity <= 0:
                    errors.append(f"{item_label}.quantity must be > 0")
            unit = ingredient.get("unit")
            if unit is not None and not isinstance(unit, str):
                errors.append(f"{item_label}.unit must be null or a string")

    step_ids: set[str] = set()
    steps = recipe.get("steps")
    if not isinstance(steps, list) or not steps:
        errors.append(f"{recipe_id}.steps must be a non-empty array")
    else:
        for position, step in enumerate(steps):
            item_label = f"{recipe_id}.steps[{position}]"
            if not isinstance(step, dict):
                errors.append(f"{item_label} must be an object")
                continue
            step_id = step.get("id")
            if not non_empty_string(step_id) or not ID_RE.fullmatch(step_id):
                errors.append(f"{item_label}.id is invalid")
                continue
            if step_id in step_ids:
                errors.append(f"{recipe_id} duplicate step id: {step_id}")
            step_ids.add(step_id)
            timer = step.get("timerSeconds")
            if timer is not None and (not is_int(timer) or timer < 0):
                errors.append(f"{item_label}.timerSeconds must be null or >= 0")

    return recipe_id, ingredient_ids, step_ids


def validate() -> list[str]:
    errors: list[str] = []
    manifest = load_json(MANIFEST_PATH, errors)
    if manifest is None:
        return errors

    if manifest.get("schemaVersion") != SUPPORTED_SCHEMA_VERSION:
        errors.append("manifest.schemaVersion is unsupported")

    catalog_version = manifest.get("catalogVersion")
    if not non_empty_string(catalog_version) or not SEMVER_RE.fullmatch(catalog_version):
        errors.append("manifest.catalogVersion must use x.y.z semantic versioning")

    default_locale = manifest.get("defaultLocale")
    supported_locales = manifest.get("supportedLocales")
    if not isinstance(supported_locales, list) or any(
        not non_empty_string(locale) for locale in supported_locales
    ):
        errors.append("manifest.supportedLocales must be an array of locale strings")
        supported_set: set[str] = set()
    else:
        supported_set = set(supported_locales)
        if len(supported_set) != len(supported_locales):
            errors.append("manifest.supportedLocales contains duplicates")
        if supported_set != APP_LOCALES:
            errors.append(
                "manifest.supportedLocales must be exactly: "
                + ", ".join(sorted(APP_LOCALES))
            )

    if default_locale not in supported_set:
        errors.append("manifest.defaultLocale must be supported")

    content_path = app_path(manifest.get("contentAsset"), "manifest.contentAsset", errors)

    locale_assets = manifest.get("localeAssets")
    if not isinstance(locale_assets, dict):
        errors.append("manifest.localeAssets must be an object")
        locale_assets = {}
    if set(locale_assets) != supported_set:
        errors.append("manifest.localeAssets keys must match supportedLocales")

    content = load_json(content_path, errors) if content_path else None
    canonical: dict[str, dict[str, Any]] = {}
    ingredient_ids_by_recipe: dict[str, set[str]] = {}
    step_ids_by_recipe: dict[str, set[str]] = {}
    published_ids: set[str] = set()

    if content is not None:
        if content.get("schemaVersion") != SUPPORTED_SCHEMA_VERSION:
            errors.append("recipes.schemaVersion is unsupported")
        recipes = content.get("recipes")
        if not isinstance(recipes, list):
            errors.append("recipes.recipes must be an array")
        else:
            ids: set[str] = set()
            for index, raw_recipe in enumerate(recipes):
                recipe_id, ingredient_ids, step_ids = validate_recipe(
                    raw_recipe,
                    index,
                    ids,
                    errors,
                )
                if recipe_id is None or not isinstance(raw_recipe, dict):
                    continue
                canonical[recipe_id] = raw_recipe
                ingredient_ids_by_recipe[recipe_id] = ingredient_ids
                step_ids_by_recipe[recipe_id] = step_ids
                if raw_recipe.get("status") == "published":
                    published_ids.add(recipe_id)

    localized_by_locale: dict[str, dict[str, Any]] = {}
    for locale in sorted(supported_set):
        locale_path = app_path(
            locale_assets.get(locale),
            f"manifest.localeAssets.{locale}",
            errors,
        )
        payload = load_json(locale_path, errors) if locale_path else None
        if payload is None:
            continue
        if payload.get("schemaVersion") != SUPPORTED_SCHEMA_VERSION:
            errors.append(f"{locale}: schemaVersion is unsupported")
        if payload.get("locale") != locale:
            errors.append(f"{locale}: locale envelope mismatch")
        localized = payload.get("recipes")
        if not isinstance(localized, dict):
            errors.append(f"{locale}: recipes must be an object")
            continue
        localized_by_locale[locale] = localized

        for recipe_id, text in sorted(localized.items()):
            if recipe_id not in canonical:
                errors.append(f"{locale}: orphan recipe id {recipe_id}")
                continue
            if not isinstance(text, dict):
                errors.append(f"{locale}.{recipe_id} must be an object")
                continue
            if not non_empty_string(text.get("title")):
                errors.append(f"{locale}.{recipe_id}.title is required")
            for field in ("description", "animeContext"):
                value = text.get(field)
                if value is not None and not non_empty_string(value):
                    errors.append(
                        f"{locale}.{recipe_id}.{field} must be "
                        "null or a non-empty string"
                    )

            ingredient_texts = text.get("ingredientTexts")
            if not isinstance(ingredient_texts, dict):
                errors.append(f"{locale}.{recipe_id}.ingredientTexts must be an object")
            else:
                expected = ingredient_ids_by_recipe.get(recipe_id, set())
                if set(ingredient_texts) != expected:
                    errors.append(
                        f"{locale}.{recipe_id}.ingredientTexts ids do not match canonical ids"
                    )
                for item_id, item_text in sorted(ingredient_texts.items()):
                    if not isinstance(item_text, dict):
                        errors.append(
                            f"{locale}.{recipe_id}.ingredientTexts.{item_id} must be an object"
                        )
                        continue
                    if not non_empty_string(item_text.get("name")):
                        errors.append(
                            f"{locale}.{recipe_id}.ingredientTexts.{item_id}.name is required"
                        )
                    note = item_text.get("note")
                    if note is not None and not isinstance(note, str):
                        errors.append(
                            f"{locale}.{recipe_id}.ingredientTexts.{item_id}.note must be null or string"
                        )

            step_texts = text.get("stepTexts")
            if not isinstance(step_texts, dict):
                errors.append(f"{locale}.{recipe_id}.stepTexts must be an object")
            else:
                expected = step_ids_by_recipe.get(recipe_id, set())
                if set(step_texts) != expected:
                    errors.append(
                        f"{locale}.{recipe_id}.stepTexts ids do not match canonical ids"
                    )
                for step_id, step_text in sorted(step_texts.items()):
                    if not non_empty_string(step_text):
                        errors.append(
                            f"{locale}.{recipe_id}.stepTexts.{step_id} is required"
                        )

    default_recipes = localized_by_locale.get(default_locale, {})
    for recipe_id in sorted(published_ids):
        if recipe_id not in default_recipes:
            errors.append(
                f"Published recipe {recipe_id} is missing default locale {default_locale}"
            )

    return sorted(errors)


if __name__ == "__main__":
    failures = validate()
    if failures:
        print("Recipe catalog validation FAILED", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        raise SystemExit(1)
    print("Recipe catalog validation PASS")
