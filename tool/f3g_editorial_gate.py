from __future__ import annotations

from typing import Any


_ALLOWED_RELATIONS = {
    "verified_appearance",
    "recurring_association",
    "inspired",
    "unverified",
}
_ALLOWED_CULINARY = {"verified", "corrected", "review_required"}
_ALLOWED_ANIME = {"verified", "partial", "unverified"}


def _non_empty(value: Any, minimum: int = 1) -> bool:
    return isinstance(value, str) and len(value.strip()) >= minimum


def validate_f3g_recipe(
    recipe: dict[str, Any],
    config: dict[str, Any],
) -> list[str]:
    """Enforce the rich F3G editorial contract for published recipes.

    The normal authoring validator still owns structural/schema validation.
    This gate intentionally focuses on editorial completeness and on preventing
    unverified anime claims from being shipped as factual appearances.
    """
    if recipe.get("status") != "published":
        return []

    recipe_id = str(recipe.get("id", "<unknown>"))
    errors: list[str] = []

    references = recipe.get("animeReferences")
    if not isinstance(references, list) or not references:
        errors.append(f"{recipe_id}: published recipe requires animeReferences")
        references = []

    for index, reference in enumerate(references):
        if not isinstance(reference, dict):
            errors.append(f"{recipe_id}: animeReferences[{index}] must be an object")
            continue
        work_title = reference.get("workTitle")
        relation = reference.get("relation")
        if not _non_empty(work_title):
            errors.append(
                f"{recipe_id}: animeReferences[{index}].workTitle is required"
            )
        if relation not in _ALLOWED_RELATIONS:
            errors.append(
                f"{recipe_id}: animeReferences[{index}].relation is invalid"
            )
        if relation == "unverified":
            errors.append(
                f"{recipe_id}: published recipe cannot expose an unverified "
                "anime relation; use inspired until factual evidence exists"
            )

    verification = recipe.get("editorialVerification")
    if not isinstance(verification, dict):
        errors.append(
            f"{recipe_id}: published recipe requires editorialVerification"
        )
    else:
        culinary_status = verification.get("culinaryStatus")
        anime_status = verification.get("animeStatus")
        if culinary_status not in _ALLOWED_CULINARY:
            errors.append(f"{recipe_id}: culinaryStatus is invalid")
        elif culinary_status == "review_required":
            errors.append(
                f"{recipe_id}: culinary review is still required before publication"
            )
        if anime_status not in _ALLOWED_ANIME:
            errors.append(f"{recipe_id}: animeStatus is invalid")
        if not _non_empty(verification.get("culinaryNote"), 20):
            errors.append(f"{recipe_id}: culinaryNote is too short")
        if not _non_empty(verification.get("animeNote"), 20):
            errors.append(f"{recipe_id}: animeNote is too short")

        factual_relations = {
            ref.get("relation")
            for ref in references
            if isinstance(ref, dict)
        } & {"verified_appearance"}
        if factual_relations and anime_status != "verified":
            errors.append(
                f"{recipe_id}: verified_appearance requires animeStatus=verified"
            )

    locales = recipe.get("locales")
    if not isinstance(locales, dict):
        errors.append(f"{recipe_id}: locales object is required")
        return errors

    for locale in config.get("supportedLocales", []):
        localized = locales.get(locale)
        if not isinstance(localized, dict):
            errors.append(
                f"{recipe_id}: published F3G recipe missing locale {locale}"
            )
            continue

        if not _non_empty(localized.get("description"), 80):
            errors.append(
                f"{recipe_id}/{locale}: description must be at least 80 characters"
            )
        if not _non_empty(localized.get("animeContext"), 60):
            errors.append(
                f"{recipe_id}/{locale}: animeContext must be at least 60 characters"
            )

        steps = localized.get("steps")
        if not isinstance(steps, dict) or not steps:
            errors.append(f"{recipe_id}/{locale}: localized steps are required")
            continue

        total_chars = 0
        for step_id, text in steps.items():
            if not _non_empty(text, 30):
                errors.append(
                    f"{recipe_id}/{locale}: step {step_id} must contain "
                    "at least 30 characters of usable instruction"
                )
            if isinstance(text, str):
                total_chars += len(text.strip())
        if total_chars < 250:
            errors.append(
                f"{recipe_id}/{locale}: preparation is too terse "
                f"({total_chars} chars; minimum 250)"
            )

    return errors
