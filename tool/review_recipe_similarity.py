from __future__ import annotations

import argparse
import sys
from pathlib import Path

from recipe_authoring_lib import (
    AuthoringError,
    attach_review_decision,
    compare_recipes,
    load_asset_manifest,
    load_json,
    load_policy,
    load_recipe_files,
    load_review_decisions,
    validate_asset_files,
    validate_authoring_recipe,
    validate_config,
    write_json,
)

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Compare one recipe candidate against "
            "the current authoring catalog."
        )
    )
    parser.add_argument("candidate", type=Path)
    parser.add_argument(
        "--report",
        type=Path,
        default=(
            ROOT
            / "build"
            / "authoring"
            / "candidate_similarity_report.json"
        ),
    )
    args = parser.parse_args()

    try:
        config = load_json(
            ROOT / "authoring" / "catalog.json"
        )
        setup_errors = validate_config(config)
        if setup_errors:
            raise AuthoringError(
                "; ".join(setup_errors)
            )
        assets = load_asset_manifest(
            ROOT / str(config["assetManifest"])
        )
        asset_errors = validate_asset_files(
            assets, ROOT
        )
        if asset_errors:
            raise AuthoringError(
                "; ".join(asset_errors)
            )
        policy = load_policy(
            ROOT / str(config["similarityPolicy"])
        )
        decisions = load_review_decisions(
            ROOT / str(config["reviewDecisions"])
        )
        candidate = load_json(
            args.candidate.resolve()
        )
        errors, completeness = (
            validate_authoring_recipe(
                candidate,
                config,
                assets,
                require_complete_published=False,
            )
        )
        if errors:
            raise AuthoringError(
                "; ".join(errors)
            )
        existing = [
            recipe
            for _, recipe in load_recipe_files(
                [
                    ROOT
                    / str(config["productionSource"])
                ]
            )
        ]
    except (AuthoringError, KeyError) as exc:
        print(
            f"Candidate review FAILED: {exc}",
            file=sys.stderr,
        )
        return 1

    comparisons = [
        attach_review_decision(
            compare_recipes(
                candidate,
                recipe,
                config,
                policy,
            ),
            decisions,
        )
        for recipe in existing
    ]
    comparisons = [
        item
        for item in comparisons
        if item["classification"] != "distinct"
    ]
    comparisons.sort(
        key=lambda item: (
            -float(item["overallScore"]),
            item["rightId"],
        )
    )

    blocking = set(
        policy["blockingClassifications"]
    )
    report = {
        "candidateId": candidate.get("id"),
        "candidateLocalization": completeness,
        "normalizerVersion": policy[
            "normalizerVersion"
        ],
        "comparisons": comparisons,
        "summary": {
            "matches": len(comparisons),
            "blocking": sum(
                1
                for item in comparisons
                if item["classification"]
                in blocking
                and not item["reviewResolved"]
            ),
        },
    }
    write_json(args.report.resolve(), report)

    if not comparisons:
        print(
            "Candidate similarity review: "
            "no material conflict detected"
        )
        return 0

    print(
        "Candidate similarity review: "
        f"{len(comparisons)} material comparison(s)"
    )
    for item in comparisons:
        print(
            f"- {item['rightId']}: "
            f"{item['classification']} "
            f"score={item['overallScore']} "
            f"action="
            f"{item['recommendedAction']}"
        )
    return (
        2
        if report["summary"]["blocking"]
        else 0
    )


if __name__ == "__main__":
    raise SystemExit(main())
