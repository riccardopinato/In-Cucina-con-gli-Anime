#!/usr/bin/env python3
"""Produce source-bound, non-publishable MarianMT drafts for 101 Italian copy enrichments."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from f3l_translation_gate import digest, source_recipes
from f3l_translate_drafts import MODEL_MAP, translate_all

BEFORE = "ec302126b6578f52fb931cce03a06457660031b058a038360a4e289e684240c3"
AFTER = "deb77a9375fb0d6ce7fd92af3e2affda89124ce0f39e76f9215c367986e4aa67"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", required=True, choices=MODEL_MAP)
    a = parser.parse_args()
    source = json.loads(Path("authoring/f3k_it_hardening_51_162.json").read_text(encoding="utf-8"))
    ledger = json.loads(Path("tool/f3l_b2_2_101_description_enrichment.json").read_text(encoding="utf-8"))
    current_sha = digest(source)
    if current_sha not in (BEFORE, AFTER) or ledger["sourceSha256Before"] != BEFORE:
        raise ValueError("Unexpected Italian source SHA; no unapproved MT")
    rows = {r["id"]: r for r in source_recipes(source)}
    items = ledger["appendItalianByRecipeId"]
    if len(items) != 101 or len(set(items)) != 101:
        raise ValueError("Expected precisely 101 content edits")
    for rid, sentence in items.items():
        if rid not in rows or len(sentence.split()) < 12:
            raise ValueError(f"Invalid source-specific enrichment {rid}")
        if current_sha == BEFORE and len(rows[rid]["description"].split()) >= 45:
            raise ValueError(f"Cannot append to already-compliant recipe {rid}")
        if current_sha == AFTER and not rows[rid]["description"].endswith(sentence):
            raise ValueError(f"Already enriched source sentence does not match ledger {rid}")
    first = list(items.values())
    result = None
    for ix, model in enumerate(MODEL_MAP[a.locale]):
        prefix = ">>pt_BR<< " if a.locale == "pt" and ix == 1 else ""
        translated = translate_all(first if result is None else result.values(), model,
                                   batch_size=6, max_length=256, prefix=prefix)
        result = translated if result is None else {it: translated[tr] for it, tr in result.items()}
    if result is None or len(result) != 101:
        raise ValueError("Incomplete Marian output")
    print("F3L_101_LOCALE_BEGIN " + a.locale, flush=True)
    for rid, sentence in items.items():
        trans = result[sentence]
        if not isinstance(trans, str) or len(trans.strip()) < 30 or trans.strip() == sentence.strip():
            raise ValueError(f"Missing/untranslated sentence {a.locale}/{rid}")
        print("F3L_101_TRANSLATION " + json.dumps(
            {"locale": a.locale, "id": rid, "italian": sentence,
             "translation": trans, "status": "machine_draft_not_publishable"},
            ensure_ascii=False, separators=(",", ":")), flush=True)
    print("F3L_101_LOCALE_END " + a.locale, flush=True)


if __name__ == "__main__":
    main()
