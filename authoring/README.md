# Recipe authoring workspace

This directory is the editorial source layer. Flutter never reads these files directly.

## Flow

User/reference material -> editorial normalization -> one authoring JSON -> similarity review -> compiler -> F1 runtime catalog -> validator -> app preview.

Raw copied source prose should not be committed here. Keep raw material transient; commit only normalized culinary facts and fresh app editorial wording.

## Directories

- `recipes/`: production authoring records. Empty until F3.
- `fixtures/`: synthetic non-production records used by F2 tests/preview.
- `templates/`: copyable starting points.
- `schema/`: authoring contract reference.
- `config/`: similarity/normalization policy.
- `assets/manifest.json`: small rights-aware asset registry.
- `reviews/decisions.json`: fingerprint-bound human decisions for duplicate/variant cases.
- `inbox/`: local transient source material; ignored by Git except its README.

## Commands

```bash
python3 tool/compile_recipe_catalog.py --check
python3 tool/review_recipe_similarity.py path/to/candidate.json
python3 tool/build_recipe_preview.py
```

To regenerate the production runtime package after an approved authoring change:

```bash
python3 tool/compile_recipe_catalog.py
python3 tool/validate_recipe_catalog.py
```

Published production recipes must provide all six supported locales. Draft candidates need at least the default English locale while they are being edited/reviewed.
