from __future__ import annotations

import hashlib
import json
import math
import re
import unicodedata
from pathlib import Path
from typing import Any, Iterable

ID_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
SUPPORTED_AUTHORING_VERSION = 1
SUPPORTED_RUNTIME_SCHEMA_VERSION = 1
SUPPORTED_ASSET_MANIFEST_VERSION = 1
SUPPORTED_REVIEW_VERSION = 1


class AuthoringError(Exception):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AuthoringError(f"Missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AuthoringError(
            f"Invalid JSON {path}: line {exc.lineno}, col {exc.colno}"
        ) from exc
    if not isinstance(payload, dict):
        raise AuthoringError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def normalize_text(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    asciiish = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    lowered = asciiish.casefold()
    return " ".join(re.findall(r"[a-z0-9]+", lowered))


def token_set(value: str) -> set[str]:
    return {token for token in normalize_text(value).split() if token}


def jaccard(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 1.0
    union = left | right
    if not union:
        return 1.0
    return len(left & right) / len(union)


def closeness(left: float, right: float) -> float:
    if left == right:
        return 1.0
    denominator = max(abs(left), abs(right), 1.0)
    return max(0.0, 1.0 - abs(left - right) / denominator)


def stable_json_bytes(payload: Any) -> bytes:
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def recipe_fingerprint(recipe: dict[str, Any]) -> str:
    return hashlib.sha256(stable_json_bytes(recipe)).hexdigest()


def recipe_semantic_fingerprint(recipe: dict[str, Any]) -> str:
    semantic = dict(recipe)
    for key in (
        "id",
        "contentVersion",
        "status",
        "sourceNote",
        "imageAssetId",
    ):
        semantic.pop(key, None)
    return hashlib.sha256(stable_json_bytes(semantic)).hexdigest()


def _require_string(
    obj: dict[str, Any], key: str, label: str, errors: list[str]
) -> str | None:
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}.{key} must be a non-empty string")
        return None
    return value.strip()


def _require_int(
    obj: dict[str, Any], key: str, label: str, errors: list[str]
) -> int | None:
    value = obj.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        errors.append(f"{label}.{key} must be an integer")
        return None
    return value


def _optional_string(value: Any, label: str, errors: list[str]) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        errors.append(f"{label} must be null or a string")
        return None
    return value.strip() or None


def load_asset_manifest(path: Path) -> dict[str, dict[str, Any]]:
    payload = load_json(path)
    if payload.get("schemaVersion") != SUPPORTED_ASSET_MANIFEST_VERSION:
        raise AuthoringError(f"{path} has unsupported schemaVersion")
    raw_assets = payload.get("assets")
    if not isinstance(raw_assets, list):
        raise AuthoringError(f"{path}.assets must be an array")
    assets: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(raw_assets):
        if not isinstance(raw, dict):
            raise AuthoringError(f"{path}.assets[{index}] must be an object")
        asset_id = raw.get("id")
        if not isinstance(asset_id, str) or not ID_RE.fullmatch(asset_id):
            raise AuthoringError(f"{path}.assets[{index}].id is invalid")
        if asset_id in assets:
            raise AuthoringError(f"Duplicate asset id: {asset_id}")
        asset_path = raw.get("path")
        if not isinstance(asset_path, str) or not asset_path.strip():
            raise AuthoringError(f"{asset_id}.path is required")
        rights = raw.get("rights")
        if rights not in {"original", "public_domain", "licensed"}:
            raise AuthoringError(f"{asset_id}.rights is invalid")
        assets[asset_id] = raw
    return assets


def validate_asset_files(
    assets: dict[str, dict[str, Any]], root: Path
) -> list[str]:
    errors: list[str] = []
    root_resolved = root.resolve()
    for asset_id, asset in sorted(assets.items()):
        raw_path = asset.get("path")
        if not isinstance(raw_path, str):
            continue
        path = (root / raw_path).resolve()
        try:
            path.relative_to(root_resolved)
        except ValueError:
            errors.append(f"{asset_id}.path escapes repository root")
            continue
        if not raw_path.startswith("assets/"):
            errors.append(f"{asset_id}.path must live under assets/")
        if not path.is_file():
            errors.append(f"{asset_id}.path does not exist: {raw_path}")
    return errors


def load_policy(path: Path) -> dict[str, Any]:
    policy = load_json(path)
    if policy.get("normalizerVersion") != 1:
        raise AuthoringError(f"{path} has unsupported normalizerVersion")
    weights = policy.get("weights")
    thresholds = policy.get("thresholds")
    if not isinstance(weights, dict) or not isinstance(thresholds, dict):
        raise AuthoringError(f"{path} must define weights and thresholds")
    required_weights = {
        "reference",
        "ingredients",
        "quantities",
        "steps",
        "timing",
    }
    if set(weights) != required_weights:
        raise AuthoringError(
            f"{path}.weights keys must be {sorted(required_weights)}"
        )
    if any(
        not isinstance(v, (int, float))
        or isinstance(v, bool)
        or v < 0
        for v in weights.values()
    ):
        raise AuthoringError(f"{path}.weights must be non-negative numbers")
    if not math.isclose(
        sum(float(v) for v in weights.values()), 1.0, abs_tol=1e-9
    ):
        raise AuthoringError(f"{path}.weights must sum to 1.0")
    required_thresholds = {
        "probableDuplicate",
        "reviewRequired",
        "possibleVariant",
    }
    if set(thresholds) != required_thresholds:
        raise AuthoringError(
            f"{path}.thresholds keys must be {sorted(required_thresholds)}"
        )
    p = float(thresholds["probableDuplicate"])
    r = float(thresholds["reviewRequired"])
    v = float(thresholds["possibleVariant"])
    if not (1.0 >= p > r > v >= 0.0):
        raise AuthoringError(
            f"{path}.thresholds must satisfy "
            "1 >= probableDuplicate > reviewRequired > possibleVariant >= 0"
        )
    blocking = policy.get("blockingClassifications")
    if not isinstance(blocking, list) or any(
        not isinstance(item, str) for item in blocking
    ):
        raise AuthoringError(
            f"{path}.blockingClassifications must be an array of strings"
        )
    aliases = policy.get("ingredientAliases", {})
    conversions = policy.get("unitConversions", {})
    if not isinstance(aliases, dict) or not isinstance(conversions, dict):
        raise AuthoringError(f"{path} aliases/conversions must be objects")
    return policy


def load_review_decisions(path: Path) -> list[dict[str, Any]]:
    payload = load_json(path)
    if payload.get("schemaVersion") != SUPPORTED_REVIEW_VERSION:
        raise AuthoringError(f"{path} has unsupported schemaVersion")
    decisions = payload.get("decisions")
    if not isinstance(decisions, list):
        raise AuthoringError(f"{path}.decisions must be an array")
    normalized: list[dict[str, Any]] = []
    for index, decision in enumerate(decisions):
        if not isinstance(decision, dict):
            raise AuthoringError(
                f"{path}.decisions[{index}] must be an object"
            )
        required = [
            "leftId",
            "rightId",
            "leftFingerprint",
            "rightFingerprint",
            "normalizerVersion",
            "decision",
            "reviewedAt",
        ]
        if any(key not in decision for key in required):
            raise AuthoringError(
                f"{path}.decisions[{index}] is incomplete"
            )
        if decision["decision"] not in {
            "accept_new",
            "skip_new",
            "replace_existing",
            "merge",
            "keep_variant",
            "defer",
        }:
            raise AuthoringError(
                f"{path}.decisions[{index}].decision is invalid"
            )
        normalized.append(decision)
    return normalized


def load_recipe_files(
    directories: Iterable[Path],
) -> list[tuple[Path, dict[str, Any]]]:
    files: list[tuple[Path, dict[str, Any]]] = []
    for directory in directories:
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.json")):
            files.append((path, load_json(path)))
    return files


def validate_config(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if config.get("authoringVersion") != SUPPORTED_AUTHORING_VERSION:
        errors.append("catalog.authoringVersion is unsupported")
    if config.get("schemaVersion") != SUPPORTED_RUNTIME_SCHEMA_VERSION:
        errors.append("catalog.schemaVersion is unsupported")
    version = config.get("catalogVersion")
    if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
        errors.append(
            "catalog.catalogVersion must use x.y.z semantic versioning"
        )
    locales = config.get("supportedLocales")
    if not isinstance(locales, list) or any(
        not isinstance(v, str) or not v for v in locales
    ):
        errors.append(
            "catalog.supportedLocales must be an array of locale strings"
        )
        locales = []
    if len(set(locales)) != len(locales):
        errors.append("catalog.supportedLocales contains duplicates")
    default_locale = config.get("defaultLocale")
    if default_locale not in locales:
        errors.append(
            "catalog.defaultLocale must be included in supportedLocales"
        )
    return errors


def validate_authoring_recipe(
    recipe: dict[str, Any],
    config: dict[str, Any],
    assets: dict[str, dict[str, Any]],
    *,
    require_complete_published: bool = True,
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    label = str(recipe.get("id") or "<recipe>")

    if recipe.get("authoringVersion") != SUPPORTED_AUTHORING_VERSION:
        errors.append(f"{label}.authoringVersion is unsupported")

    recipe_id = _require_string(recipe, "id", label, errors)
    if recipe_id is not None and not ID_RE.fullmatch(recipe_id):
        errors.append(f"{label}.id is invalid")

    version = _require_int(recipe, "contentVersion", label, errors)
    if version is not None and version < 1:
        errors.append(f"{label}.contentVersion must be >= 1")

    status = recipe.get("status")
    if status not in {"draft", "published", "archived"}:
        errors.append(f"{label}.status is invalid")

    _require_string(recipe, "inspirationTitle", label, errors)

    for field in ("prepMinutes", "cookMinutes"):
        value = _require_int(recipe, field, label, errors)
        if value is not None and value < 0:
            errors.append(f"{label}.{field} must be >= 0")

    servings = _require_int(recipe, "servings", label, errors)
    if servings is not None and servings < 1:
        errors.append(f"{label}.servings must be >= 1")

    if recipe.get("difficulty") not in {"easy", "medium", "hard"}:
        errors.append(f"{label}.difficulty is invalid")
    if recipe.get("contentOrigin") not in {
        "original",
        "inspired",
        "adapted",
    }:
        errors.append(f"{label}.contentOrigin is invalid")
    _optional_string(
        recipe.get("sourceNote"), f"{label}.sourceNote", errors
    )

    asset_id = recipe.get("imageAssetId")
    if asset_id is not None:
        if not isinstance(asset_id, str) or asset_id not in assets:
            errors.append(
                f"{label}.imageAssetId references an unknown asset"
            )

    ingredient_ids: set[str] = set()
    ingredients = recipe.get("ingredients")
    if not isinstance(ingredients, list) or not ingredients:
        errors.append(
            f"{label}.ingredients must be a non-empty array"
        )
        ingredients = []
    for index, ingredient in enumerate(ingredients):
        item_label = f"{label}.ingredients[{index}]"
        if not isinstance(ingredient, dict):
            errors.append(f"{item_label} must be an object")
            continue
        item_id = _require_string(
            ingredient, "id", item_label, errors
        )
        if item_id is not None:
            if not ID_RE.fullmatch(item_id):
                errors.append(f"{item_label}.id is invalid")
            elif item_id in ingredient_ids:
                errors.append(
                    f"{label} duplicate ingredient id: {item_id}"
                )
            ingredient_ids.add(item_id)
        quantity = ingredient.get("quantity")
        if quantity is not None:
            if (
                isinstance(quantity, bool)
                or not isinstance(quantity, (int, float))
            ):
                errors.append(
                    f"{item_label}.quantity must be numeric or null"
                )
            elif quantity <= 0:
                errors.append(
                    f"{item_label}.quantity must be > 0"
                )
        _optional_string(
            ingredient.get("unit"), f"{item_label}.unit", errors
        )

    step_ids: set[str] = set()
    steps = recipe.get("steps")
    if not isinstance(steps, list) or not steps:
        errors.append(f"{label}.steps must be a non-empty array")
        steps = []
    for index, step in enumerate(steps):
        step_label = f"{label}.steps[{index}]"
        if not isinstance(step, dict):
            errors.append(f"{step_label} must be an object")
            continue
        step_id = _require_string(
            step, "id", step_label, errors
        )
        if step_id is not None:
            if not ID_RE.fullmatch(step_id):
                errors.append(f"{step_label}.id is invalid")
            elif step_id in step_ids:
                errors.append(
                    f"{label} duplicate step id: {step_id}"
                )
            step_ids.add(step_id)
        timer = step.get("timerSeconds")
        if timer is not None and (
            isinstance(timer, bool)
            or not isinstance(timer, int)
            or timer < 0
        ):
            errors.append(
                f"{step_label}.timerSeconds must be null "
                "or an integer >= 0"
            )

    supported_locales = config.get("supportedLocales", [])
    default_locale = config.get("defaultLocale")
    locales = recipe.get("locales")
    if not isinstance(locales, dict):
        errors.append(f"{label}.locales must be an object")
        locales = {}

    unknown_locales = set(locales) - set(supported_locales)
    if unknown_locales:
        errors.append(
            f"{label}.locales contains unsupported locales: "
            f"{sorted(unknown_locales)}"
        )
    if default_locale not in locales:
        errors.append(
            f"{label} is missing default locale {default_locale}"
        )

    missing_locales = [
        locale
        for locale in supported_locales
        if locale not in locales
    ]
    if (
        require_complete_published
        and status == "published"
        and missing_locales
    ):
        errors.append(
            f"{label} published recipe is missing locales: "
            f"{', '.join(missing_locales)}"
        )

    for locale, localized in sorted(locales.items()):
        locale_label = f"{label}.locales.{locale}"
        if not isinstance(localized, dict):
            errors.append(f"{locale_label} must be an object")
            continue
        _require_string(
            localized, "title", locale_label, errors
        )

        localized_ingredients = localized.get("ingredients")
        if not isinstance(localized_ingredients, dict):
            errors.append(
                f"{locale_label}.ingredients must be an object"
            )
        else:
            if set(localized_ingredients) != ingredient_ids:
                errors.append(
                    f"{locale_label}.ingredients ids do not "
                    "match canonical ingredient ids"
                )
            for item_id, text in sorted(
                localized_ingredients.items()
            ):
                if not isinstance(text, dict):
                    errors.append(
                        f"{locale_label}.ingredients.{item_id} "
                        "must be an object"
                    )
                    continue
                _require_string(
                    text,
                    "name",
                    f"{locale_label}.ingredients.{item_id}",
                    errors,
                )
                _optional_string(
                    text.get("note"),
                    f"{locale_label}.ingredients.{item_id}.note",
                    errors,
                )

        localized_steps = localized.get("steps")
        if not isinstance(localized_steps, dict):
            errors.append(
                f"{locale_label}.steps must be an object"
            )
        else:
            if set(localized_steps) != step_ids:
                errors.append(
                    f"{locale_label}.steps ids do not "
                    "match canonical step ids"
                )
            for step_id, text in sorted(
                localized_steps.items()
            ):
                if (
                    not isinstance(text, str)
                    or not text.strip()
                ):
                    errors.append(
                        f"{locale_label}.steps.{step_id} "
                        "must be non-empty"
                    )

    completeness = {
        "recipeId": recipe_id or label,
        "status": status,
        "availableLocales": sorted(locales),
        "missingLocales": missing_locales,
        "complete": not missing_locales,
    }
    return sorted(errors), completeness


def _canonical_ingredient_key(
    recipe: dict[str, Any],
    ingredient: dict[str, Any],
    default_locale: str,
    aliases: dict[str, str],
) -> str:
    item_id = str(ingredient.get("id", ""))
    localized = (
        recipe.get("locales", {}).get(default_locale, {})
    )
    localized_ingredients = (
        localized.get("ingredients", {})
        if isinstance(localized, dict)
        else {}
    )
    raw_name = ""
    if isinstance(localized_ingredients, dict):
        text = localized_ingredients.get(item_id)
        if isinstance(text, dict):
            raw_name = str(text.get("name") or "")
    normalized_name = normalize_text(raw_name)
    normalized_id = normalize_text(item_id)
    return aliases.get(
        normalized_name,
        aliases.get(
            normalized_id,
            normalized_name or normalized_id,
        ),
    )


def _ingredient_map(
    recipe: dict[str, Any],
    config: dict[str, Any],
    policy: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    default_locale = str(config["defaultLocale"])
    raw_aliases = policy.get("ingredientAliases", {})
    aliases = {
        normalize_text(str(k)): normalize_text(str(v))
        for k, v in raw_aliases.items()
    }
    result: dict[str, dict[str, Any]] = {}
    for raw in recipe.get("ingredients", []):
        if not isinstance(raw, dict):
            continue
        key = _canonical_ingredient_key(
            recipe, raw, default_locale, aliases
        )
        if key:
            result[key] = raw
    return result


def _normalized_quantity(
    ingredient: dict[str, Any],
    policy: dict[str, Any],
) -> tuple[str | None, float | None]:
    quantity = ingredient.get("quantity")
    if (
        isinstance(quantity, bool)
        or not isinstance(quantity, (int, float))
    ):
        return None, None
    unit = ingredient.get("unit")
    if unit is None:
        return "count", float(quantity)
    normalized_unit = normalize_text(str(unit)).replace(" ", "")
    conversions = policy.get("unitConversions", {})
    rule = conversions.get(normalized_unit)
    if not isinstance(rule, dict):
        return normalized_unit, float(quantity)
    dimension = rule.get("dimension")
    factor = rule.get("factor")
    if (
        not isinstance(dimension, str)
        or not isinstance(factor, (int, float))
    ):
        return normalized_unit, float(quantity)
    return dimension, float(quantity) * float(factor)


def compare_recipes(
    left: dict[str, Any],
    right: dict[str, Any],
    config: dict[str, Any],
    policy: dict[str, Any],
) -> dict[str, Any]:
    default_locale = str(config["defaultLocale"])
    left_fp = recipe_fingerprint(left)
    right_fp = recipe_fingerprint(right)
    left_semantic_fp = recipe_semantic_fingerprint(left)
    right_semantic_fp = recipe_semantic_fingerprint(right)

    left_reference = token_set(
        str(left.get("inspirationTitle", ""))
    )
    right_reference = token_set(
        str(right.get("inspirationTitle", ""))
    )
    reference_score = jaccard(
        left_reference, right_reference
    )

    left_map = _ingredient_map(left, config, policy)
    right_map = _ingredient_map(right, config, policy)
    left_keys = set(left_map)
    right_keys = set(right_map)
    ingredient_score = jaccard(left_keys, right_keys)

    common = sorted(left_keys & right_keys)
    quantity_scores: list[float] = []
    for key in common:
        left_dimension, left_value = _normalized_quantity(
            left_map[key], policy
        )
        right_dimension, right_value = _normalized_quantity(
            right_map[key], policy
        )
        if left_value is None and right_value is None:
            quantity_scores.append(1.0)
        elif left_value is None or right_value is None:
            quantity_scores.append(0.5)
        elif left_dimension == right_dimension:
            quantity_scores.append(
                closeness(left_value, right_value)
            )
        else:
            quantity_scores.append(0.0)
    quantity_score = (
        sum(quantity_scores) / len(quantity_scores)
        if quantity_scores
        else 0.0
    )

    def joined_steps(recipe: dict[str, Any]) -> str:
        localized = (
            recipe.get("locales", {})
            .get(default_locale, {})
        )
        if not isinstance(localized, dict):
            return ""
        steps = localized.get("steps", {})
        if not isinstance(steps, dict):
            return ""
        ordered_ids = [
            str(step.get("id"))
            for step in recipe.get("steps", [])
            if isinstance(step, dict)
            and step.get("id") is not None
        ]
        return " ".join(
            str(steps.get(step_id, ""))
            for step_id in ordered_ids
        )

    step_score = jaccard(
        token_set(joined_steps(left)),
        token_set(joined_steps(right)),
    )

    left_total = float(
        left.get("prepMinutes", 0) or 0
    ) + float(left.get("cookMinutes", 0) or 0)
    right_total = float(
        right.get("prepMinutes", 0) or 0
    ) + float(right.get("cookMinutes", 0) or 0)
    timing_score = closeness(left_total, right_total)

    dimensions = {
        "reference": round(reference_score, 6),
        "ingredients": round(ingredient_score, 6),
        "quantities": round(quantity_score, 6),
        "steps": round(step_score, 6),
        "timing": round(timing_score, 6),
    }
    weights = {
        key: float(value)
        for key, value in policy["weights"].items()
    }
    overall = sum(
        dimensions[key] * weights[key]
        for key in weights
    )
    overall = round(overall, 6)

    thresholds = policy["thresholds"]
    same_id = left.get("id") == right.get("id")
    if same_id and left_fp == right_fp:
        classification = "idempotent_duplicate"
        reason = "SAME_ID_SAME_FINGERPRINT"
    elif same_id:
        classification = "same_entity_update"
        reason = "SAME_ID_CHANGED_CONTENT"
    elif left_semantic_fp == right_semantic_fp:
        classification = "probable_duplicate"
        reason = "EXACT_SEMANTIC_CONTENT_DIFFERENT_ID"
    elif overall >= float(
        thresholds["probableDuplicate"]
    ):
        classification = "probable_duplicate"
        reason = "HIGH_MULTI_DIMENSION_SIMILARITY"
    elif overall >= float(
        thresholds["reviewRequired"]
    ):
        classification = "review_required"
        reason = "AMBIGUOUS_NEAR_DUPLICATE"
    elif overall >= float(
        thresholds["possibleVariant"]
    ):
        classification = "possible_variant"
        reason = "MATERIAL_OVERLAP_WITH_VARIATION"
    else:
        classification = "distinct"
        reason = "NO_MATERIAL_CONFLICT"

    only_left = sorted(left_keys - right_keys)
    only_right = sorted(right_keys - left_keys)
    differences: list[str] = []
    if normalize_text(
        str(left.get("inspirationTitle", ""))
    ) != normalize_text(
        str(right.get("inspirationTitle", ""))
    ):
        differences.append(
            "inspiration_reference_differs"
        )
    if only_left:
        differences.append(
            "ingredients_only_left:" + ",".join(only_left)
        )
    if only_right:
        differences.append(
            "ingredients_only_right:" + ",".join(only_right)
        )
    if dimensions["quantities"] < 0.95:
        differences.append("quantities_differ")
    if dimensions["steps"] < 0.95:
        differences.append("step_text_differs")
    if dimensions["timing"] < 0.95:
        differences.append("timing_differs")

    recommended = {
        "idempotent_duplicate": "SKIP",
        "same_entity_update": "UPDATE_OR_REVIEW",
        "probable_duplicate": "REVIEW_OR_SKIP",
        "review_required": "REVIEW_REQUIRED",
        "possible_variant": "KEEP_VARIANT_OR_REVIEW",
        "distinct": "ACCEPT",
    }[classification]

    return {
        "leftId": str(left.get("id")),
        "rightId": str(right.get("id")),
        "leftFingerprint": left_fp,
        "rightFingerprint": right_fp,
        "leftSemanticFingerprint": left_semantic_fp,
        "rightSemanticFingerprint": right_semantic_fp,
        "normalizerVersion": policy[
            "normalizerVersion"
        ],
        "classification": classification,
        "overallScore": overall,
        "dimensions": dimensions,
        "differences": differences,
        "recommendedAction": recommended,
        "reason": reason,
    }


def _decision_matches(
    comparison: dict[str, Any],
    decision: dict[str, Any],
) -> bool:
    direct = (
        decision.get("leftId") == comparison["leftId"]
        and decision.get("rightId")
        == comparison["rightId"]
        and decision.get("leftFingerprint")
        == comparison["leftFingerprint"]
        and decision.get("rightFingerprint")
        == comparison["rightFingerprint"]
    )
    reverse = (
        decision.get("leftId") == comparison["rightId"]
        and decision.get("rightId")
        == comparison["leftId"]
        and decision.get("leftFingerprint")
        == comparison["rightFingerprint"]
        and decision.get("rightFingerprint")
        == comparison["leftFingerprint"]
    )
    return (
        (direct or reverse)
        and decision.get("normalizerVersion")
        == comparison["normalizerVersion"]
    )


def attach_review_decision(
    comparison: dict[str, Any],
    decisions: list[dict[str, Any]],
) -> dict[str, Any]:
    result = dict(comparison)
    matching = next(
        (
            decision
            for decision in decisions
            if _decision_matches(comparison, decision)
        ),
        None,
    )
    if matching is None:
        result["reviewDecision"] = None
        result["reviewResolved"] = False
    else:
        result["reviewDecision"] = matching.get(
            "decision"
        )
        result["reviewedAt"] = matching.get("reviewedAt")
        result["reviewResolved"] = (
            matching.get("decision") != "defer"
        )
    return result


def build_similarity_report(
    recipes: list[dict[str, Any]],
    config: dict[str, Any],
    policy: dict[str, Any],
    decisions: list[dict[str, Any]],
) -> dict[str, Any]:
    comparisons: list[dict[str, Any]] = []
    for index, left in enumerate(recipes):
        for right in recipes[index + 1 :]:
            comparison = compare_recipes(
                left, right, config, policy
            )
            if comparison["classification"] == "distinct":
                continue
            comparisons.append(
                attach_review_decision(
                    comparison, decisions
                )
            )
    comparisons.sort(
        key=lambda item: (
            -float(item["overallScore"]),
            item["leftId"],
            item["rightId"],
        )
    )

    blocking = set(
        policy.get("blockingClassifications", [])
    )
    unresolved_blocking = [
        item
        for item in comparisons
        if item["classification"] in blocking
        and not item["reviewResolved"]
    ]
    summary: dict[str, int] = {
        "idempotent_duplicate": 0,
        "same_entity_update": 0,
        "probable_duplicate": 0,
        "review_required": 0,
        "possible_variant": 0,
        "resolved": 0,
        "unresolvedBlocking": len(
            unresolved_blocking
        ),
    }
    for item in comparisons:
        summary[item["classification"]] = (
            summary.get(item["classification"], 0) + 1
        )
        if item["reviewResolved"]:
            summary["resolved"] += 1
    return {
        "summary": summary,
        "comparisons": comparisons,
    }


def compile_runtime_catalog(
    recipes: list[dict[str, Any]],
    config: dict[str, Any],
    assets: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    supported_locales = list(
        config["supportedLocales"]
    )
    canonical_recipes: list[dict[str, Any]] = []
    locale_payloads: dict[
        str, dict[str, Any]
    ] = {
        locale: {
            "schemaVersion": (
                SUPPORTED_RUNTIME_SCHEMA_VERSION
            ),
            "locale": locale,
            "recipes": {},
        }
        for locale in supported_locales
    }

    for recipe in sorted(
        recipes, key=lambda item: str(item["id"])
    ):
        asset_id = recipe.get("imageAssetId")
        image_path = (
            assets.get(asset_id, {}).get("path")
            if asset_id
            else None
        )
        canonical = {
            "id": recipe["id"],
            "contentVersion": recipe[
                "contentVersion"
            ],
            "status": recipe["status"],
            "inspirationTitle": recipe[
                "inspirationTitle"
            ],
            "prepMinutes": recipe["prepMinutes"],
            "cookMinutes": recipe["cookMinutes"],
            "servings": recipe["servings"],
            "difficulty": recipe["difficulty"],
            "imageAsset": image_path,
            "contentOrigin": recipe["contentOrigin"],
            "sourceNote": recipe.get("sourceNote"),
            "ingredients": [
                {
                    "id": item["id"],
                    "quantity": item.get("quantity"),
                    "unit": item.get("unit"),
                }
                for item in recipe["ingredients"]
            ],
            "steps": [
                {
                    "id": step["id"],
                    "timerSeconds": step.get(
                        "timerSeconds"
                    ),
                }
                for step in recipe["steps"]
            ],
        }
        canonical_recipes.append(canonical)

        for locale, localized in sorted(
            recipe["locales"].items()
        ):
            locale_payloads[locale]["recipes"][
                recipe["id"]
            ] = {
                "title": localized["title"],
                "ingredientTexts": localized[
                    "ingredients"
                ],
                "stepTexts": localized["steps"],
            }

    manifest = {
        "schemaVersion": (
            SUPPORTED_RUNTIME_SCHEMA_VERSION
        ),
        "catalogVersion": config["catalogVersion"],
        "defaultLocale": config["defaultLocale"],
        "supportedLocales": supported_locales,
        "contentAsset": "assets/catalog/recipes.json",
        "localeAssets": {
            locale: (
                f"assets/catalog/locales/{locale}.json"
            )
            for locale in supported_locales
        },
    }
    return {
        "manifest.json": manifest,
        "recipes.json": {
            "schemaVersion": (
                SUPPORTED_RUNTIME_SCHEMA_VERSION
            ),
            "recipes": canonical_recipes,
        },
        **{
            f"locales/{locale}.json": payload
            for locale, payload in locale_payloads.items()
        },
    }


def build_authoring_report(
    recipes: list[dict[str, Any]],
    config: dict[str, Any],
    policy: dict[str, Any],
    decisions: list[dict[str, Any]],
    completeness: list[dict[str, Any]],
    validation_errors: list[str],
) -> dict[str, Any]:
    similarity = build_similarity_report(
        recipes, config, policy, decisions
    )
    return {
        "authoringVersion": (
            SUPPORTED_AUTHORING_VERSION
        ),
        "normalizerVersion": policy[
            "normalizerVersion"
        ],
        "catalogVersion": config.get(
            "catalogVersion"
        ),
        "recipeCount": len(recipes),
        "validation": {
            "status": (
                "PASS"
                if not validation_errors
                else "FAIL"
            ),
            "errors": sorted(validation_errors),
        },
        "localization": sorted(
            completeness,
            key=lambda item: item["recipeId"],
        ),
        "similarity": similarity,
    }
