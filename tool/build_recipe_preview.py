from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "assets" / "catalog"


def run_command(command: list[str]) -> None:
    print("+ " + " ".join(command), flush=True)
    subprocess.run(
        command,
        cwd=ROOT,
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build a Flutter Web preview with "
            "synthetic authoring fixtures, then "
            "restore the production catalog."
        )
    )
    parser.add_argument(
        "--compile-only",
        action="store_true",
        help=(
            "Compile and validate the fixture "
            "catalog without invoking Flutter."
        ),
    )
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(
        prefix="anime-kitchen-preview-"
    ) as temp_dir:
        backup = Path(temp_dir) / "catalog"
        shutil.copytree(CATALOG, backup)
        try:
            run_command(
                [
                    sys.executable,
                    "tool/compile_recipe_catalog.py",
                    "--include-fixtures",
                    "--output-dir",
                    "assets/catalog",
                    "--report",
                    (
                        "build/authoring/"
                        "preview_report.json"
                    ),
                ]
            )
            run_command(
                [
                    sys.executable,
                    "tool/validate_recipe_catalog.py",
                ]
            )
            if not args.compile_only:
                run_command(
                    [
                        "flutter",
                        "build",
                        "web",
                        "--release",
                        "--base-href",
                        "/In-Cucina-con-gli-Anime/",
                    ]
                )
                print(
                    "Synthetic recipe Web preview "
                    "build PASS"
                )
            else:
                print(
                    "Synthetic recipe preview "
                    "compile PASS"
                )
        finally:
            if CATALOG.exists():
                shutil.rmtree(CATALOG)
            shutil.copytree(backup, CATALOG)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
