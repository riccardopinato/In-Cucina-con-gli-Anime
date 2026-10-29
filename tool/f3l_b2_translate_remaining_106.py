#!/usr/bin/env python3
"""Translate the remaining 106 verified Italian F3L candidate descriptions.

CI-only utility: emits 106 source-bound machine translations per requested
locale, never human reviewed, never production assets. GitHub job logs expose
one JSON item per record for deterministic retrieval/reconciliation.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from f3l_translation_gate import digest, source_recipes
from f3l_translate_drafts import MODEL_MAP, translate_all

HISTORICAL_SHA = "954fb9ddc47ff90f7678b4677a4f12dab4633b6c0afa883c25ec8b417f19cd1c"
PRE_MIGRATION_SHA = "d18d492b0db2148aed213610ffd1ff98bcff925a66cf4444a8a4da9b51576227"
ALREADY_MIGRATED = {59, 73, 74, 81, 88, 124}
PARTS = ((51, 78), (79, 106), (107, 134), (135, 162))


def load_pending(root: Path) -> list[tuple[str, str]]:
    source = json.loads((root / "authoring/f3k_it_hardening_51_162.json").read_text(encoding="utf-8"))
    if digest(source) != PRE_MIGRATION_SHA:
        raise ValueError("Italian source baseline changed before bulk translation")
    all_recipes = {x["id"]: x for x in source_recipes(source)}
    pending: list[tuple[str, str]] = []
    for start, end in PARTS:
        pack_path = root / "docs/f3l_editorial/italian_proposals" / f"{start:03d}_{end:03d}.json"
        pack = json.loads(pack_path.read_text(encoding="utf-8"))
        if pack["sourceBaselineSha256"] != HISTORICAL_SHA or pack["range"] != [start, end]:
            raise ValueError(f"Wrong original candidate provenance: {pack_path}")
        for n, record in enumerate(pack["proposals"], start):
            rid = f"recipe_{n:06d}"
            if record["recipeId"] != rid or record["reviewStatus"] != "CANDIDATE_NOT_APPROVED":
                raise ValueError(f"Candidate missing/not pending: {rid}")
            if n in ALREADY_MIGRATED:
                continue
            candidate = record["proposedDescriptionIT"]
            if not isinstance(candidate, str) or len(candidate.strip()) < 75:
                raise ValueError(f"Candidate missing substantive description: {rid}")
            if candidate == all_recipes[rid]["description"]:
                raise ValueError(f"New description identical to old source: {rid}")
            pending.append((rid, candidate))
    if len(pending) != 106 or len(set(rid for rid, _ in pending)) != 106:
        raise ValueError("Expected exactly 106 distinct remaining Italian candidates")
    return pending


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", choices=MODEL_MAP, required=True)
    parser.add_argument("--batch-size", type=int, default=6)
    args = parser.parse_args()
    pending = load_pending(Path.cwd())
    originals = [description for _, description in pending]
    out = None
    for model_index, model in enumerate(MODEL_MAP[args.locale]):
        prefix = ">>pt_BR<< " if args.locale == "pt" and model_index == 1 else ""
        out = translate_all(
            originals if out is None else list(out.values()),
            model, batch_size=args.batch_size, max_length=512, prefix=prefix
        ) if out is None else {
            src: translated
            for src, translated in zip(
                out.keys(),
                _translate_second_pass(out, model, args.batch_size, prefix)
            )
        }
    if out is None or len(out) != 106:
        raise ValueError("Incomplete model translation")
    print("F3L_B2_106_BEGIN " + args.locale, flush=True)
    for rid, candidate in pending:
        text = out[candidate]
        if not isinstance(text, str) or len(text.strip()) < 40 or text.strip() == candidate.strip():
            raise ValueError(f"Missing, too short or untranslated candidate: {rid} {args.locale}")
        print("F3L_B2_TRANSLATED_ITEM " + json.dumps(
            {"locale": args.locale, "id": rid, "text": text, "reviewStatus": "machine_draft"},
            ensure_ascii=False, separators=(",", ":")
        ), flush=True)
    print("F3L_B2_106_END " + args.locale, flush=True)


def _translate_second_pass(mapping: dict[str, str], model: str, batch_size: int, prefix: str) -> list[str]:
    second = translate_all(list(mapping.values()), model, batch_size=batch_size, max_length=512, prefix=prefix)
    return [second[item] for item in mapping.values()]


if __name__ == "__main__":
    main()
