from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from recipe_authoring_lib import (
    AuthoringError,
    build_authoring_report,
    compile_runtime_catalog,
    load_asset_manifest,
    load_json,
    load_policy,
    load_recipe_files,
    load_review_decisions,
    validate_asset_files,
    validate_asset_usage,
    validate_authoring_recipe,
    validate_config,
    write_json,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "authoring" / "catalog.json"


def _read_sources(
    config: dict, include_fixtures: bool
) -> list[tuple[Path, dict]]:
    directories = [
        ROOT / str(config["productionSource"])
    ]
    if include_fixtures:
        directories.append(
            ROOT / str(config["fixtureSource"])
        )
    return load_recipe_files(directories)


def _runtime_path(
    output_dir: Path, relative: str
) -> Path:
    return output_dir / relative


def _compare_output(
    output_dir: Path,
    compiled: dict[str, object],
) -> list[str]:
    drift: list[str] = []
    for relative, payload in compiled.items():
        path = _runtime_path(output_dir, relative)
        expected = (
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
                sort_keys=False,
            )
            + "\n"
        )
        if not path.exists():
            drift.append(
                f"Missing generated file: "
                f"{path.relative_to(ROOT)}"
            )
            continue
        actual = path.read_text(encoding="utf-8")
        if actual != expected:
            drift.append(
                f"Generated catalog drift: "
                f"{path.relative_to(ROOT)}"
            )
    return drift


def run(
    *,
    config_path: Path,
    output_dir: Path,
    report_path: Path,
    include_fixtures: bool,
    check: bool,
) -> int:
    try:
        config = load_json(config_path)
        config_errors = validate_config(config)
        assets = load_asset_manifest(
            ROOT / str(config["assetManifest"])
        )
        policy = load_policy(
            ROOT / str(config["similarityPolicy"])
        )
        decisions = load_review_decisions(
            ROOT / str(config["reviewDecisions"])
        )
        source_files = _read_sources(
            config, include_fixtures
        )
    except (AuthoringError, KeyError) as exc:
        print(
            f"Authoring setup FAILED: {exc}",
            file=sys.stderr,
        )
        return 1

    recipes: list[dict] = []
    validation_errors = (
        list(config_errors)
        + validate_asset_files(assets, ROOT)
    )
    completeness: list[dict] = []
    ids: set[str] = set()
    for path, recipe in source_files:
        recipe_id = recipe.get("id")
        if isinstance(recipe_id, str):
            if recipe_id in ids:
                validation_errors.append(
                    "Duplicate authoring recipe id: "
                    f"{recipe_id}"
                )
            ids.add(recipe_id)
        errors, locale_report = (
            validate_authoring_recipe(
                recipe, config, assets
            )
        )
        validation_errors.extend(
            f"{path.relative_to(ROOT)}: {error}"
            for error in errors
        )
        completeness.append(locale_report)
        recipes.append(recipe)

    validation_errors.extend(
        validate_asset_usage(recipes, assets)
    )

    report = build_authoring_report(
        recipes,
        config,
        policy,
        decisions,
        completeness,
        validation_errors,
    )
    write_json(report_path, report)

    if validation_errors:
        print(
            "Recipe authoring validation FAILED",
            file=sys.stderr,
        )
        for error in sorted(validation_errors):
            print(f"- {error}", file=sys.stderr)
        return 1

    unresolved = report["similarity"]["summary"][
        "unresolvedBlocking"
    ]
    if unresolved:
        print(
            "Recipe similarity gate BLOCKED: "
            f"{unresolved} unresolved blocking "
            "comparison(s)",
            file=sys.stderr,
        )
        blocking = set(
            policy["blockingClassifications"]
        )
        for comparison in report["similarity"][
            "comparisons"
        ]:
            if (
                comparison["classification"]
                in blocking
                and not comparison["reviewResolved"]
            ):
                print(
                    f"- {comparison['leftId']} <-> "
                    f"{comparison['rightId']}: "
                    f"{comparison['classification']} "
                    f"score="
                    f"{comparison['overallScore']}",
                    file=sys.stderr,
                )
        return 2

    compiled = compile_runtime_catalog(
        recipes, config, assets
    )
    if check:
        drift = _compare_output(
            output_dir, compiled
        )
        if drift:
            print(
                "Recipe catalog generation check FAILED",
                file=sys.stderr,
            )
            for error in drift:
                print(f"- {error}", file=sys.stderr)
            return 3
        print(
            "Recipe authoring PASS: "
            f"{len(recipes)} recipe(s), "
            "catalog generation is up to date"
        )
        return 0

    for relative, payload in compiled.items():
        write_json(
            _runtime_path(output_dir, relative),
            payload,
        )
    destination = (
        output_dir.relative_to(ROOT)
        if output_dir.is_relative_to(ROOT)
        else output_dir
    )
    print(
        "Recipe authoring PASS: compiled "
        f"{len(recipes)} recipe(s) -> "
        f"{destination}"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Compile recipe authoring JSON into "
            "the F1 runtime catalog."
        )
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "assets" / "catalog",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=(
            ROOT
            / "build"
            / "authoring"
            / "recipe_authoring_report.json"
        ),
    )
    parser.add_argument(
        "--include-fixtures",
        action="store_true",
    )
    parser.add_argument(
        "--check",
        action="store_true",
    )
    args = parser.parse_args()
    return run(
        config_path=args.config.resolve(),
        output_dir=args.output_dir.resolve(),
        report_path=args.report.resolve(),
        include_fixtures=args.include_fixtures,
        check=args.check,
    )


if __name__ == "__main__":
    raise SystemExit(main())
