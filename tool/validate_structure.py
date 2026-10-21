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
    ROOT / "docs" / "GOLDEN_REUSE_MANIFEST.txt",
    ROOT / "lib" / "main.dart",
    ROOT / "lib" / "core" / "theme" / "app_theme.dart",
    ROOT / "lib" / "features" / "recipes" / "data" / "empty_recipe_catalog_repository.dart",
]

missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
if missing:
    raise SystemExit(f"Missing required files: {', '.join(missing)}")

arb_dir = ROOT / "lib" / "l10n"
arb_files = sorted(arb_dir.glob("app_*.arb"))
if len(arb_files) != 6:
    raise SystemExit(f"Expected 6 ARB files, found {len(arb_files)}")

key_sets = {}
for path in arb_files:
    payload = json.loads(path.read_text(encoding="utf-8"))
    key_sets[path.name] = {key for key in payload if not key.startswith("@")}

template = key_sets["app_en.arb"]
for name, keys in key_sets.items():
    if keys != template:
        raise SystemExit(f"{name} localization keys do not match app_en.arb")

for forbidden in ("calcifer_bacon", "ichiraku_ramen", "ponyo_ramen", "totoro_bento"):
    for path in (ROOT / "lib").rglob("*.dart"):
        if forbidden in path.read_text(encoding="utf-8").lower():
            raise SystemExit(f"Bootstrap contains recipe data marker {forbidden}: {path}")

print("Structure validation PASS")
