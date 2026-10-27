#!/usr/bin/env python3
"""Advisory, source-bound editorial triage; never approves a translation."""
from __future__ import annotations
import argparse
import collections
import json
import re
from pathlib import Path

from f3l_translation_gate import inspect,source_recipes

DECIMAL = re.compile(r"(?<![\w])\d+(?:[.,]\d+)?(?![\d])")
# Japanese food names should stay recognizable and not be silently replaced by
# generic 'meat', 'sauce', or 'noodles'. This is a review hint, not a legal name gate.
STABLE_FOOD_TERMS = ("chashu", "miso", "mirin", "sake", "dashi", "anko", "kinako", "menma", "yuzu", "nori", "togarashi", "mochi", "udon", "ramen", "soba", "tempura", "daikon", "kabocha", "wasabi")

def normalized_numbers(text):
    # Match the whole number even when the unit is directly attached (400ml, 20g).
    # Avoid accidentally matching 40 inside 400 or 2 inside 20.
    return [x.replace(",", ".") for x in DECIMAL.findall(text)]

def inspect_copy(source, pack):
    issues=[]
    rows = source_recipes(source)
    for it, target in zip(rows,pack.get("recipes",[])):
        rid=it["id"]
        if target.get("id") != rid: continue
        for ix, (src, dst) in enumerate(zip(it["steps"],target.get("steps",[]))):
            ref=src["instruction"]
            output=dst.get("instruction","")
            src_numbers=collections.Counter(normalized_numbers(ref))
            dst_numbers=collections.Counter(normalized_numbers(output))
            missing=src_numbers-dst_numbers
            if missing:
                issues.append({"severity":"high","recipe":rid,"field":f"step_{ix+1}","reason":"numeric_tokens_missing_or_reworded","tokens":list(missing.elements())})
            required=[t for t in STABLE_FOOD_TERMS if re.search(r"\b"+re.escape(t)+r"\b",ref,re.I)]
            absent=[t for t in required if not re.search(r"\b"+re.escape(t)+r"\b",output,re.I)]
            if absent:
                issues.append({"severity":"medium","recipe":rid,"field":f"step_{ix+1}","reason":"japanese_culinary_term_not_visible","terms":absent})
        for ix,(src,dst) in enumerate(zip(it["ingredients"],target.get("ingredients",[]))):
            required=[t for t in STABLE_FOOD_TERMS if re.search(r"\b"+re.escape(t)+r"\b",src["name"],re.I)]
            missing=[t for t in required if not re.search(r"\b"+re.escape(t)+r"\b",dst.get("name",""),re.I)]
            if missing:
                issues.append({"severity":"medium","recipe":rid,"field":f"ingredient_{ix+1}","reason":"japanese_food_term_not_visible","terms":missing})
    return issues

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",default="authoring/f3k_it_hardening_51_162.json")
    ap.add_argument("--pack",required=True)
    ap.add_argument("--report",required=True)
    ns=ap.parse_args()
    source=json.loads(Path(ns.source).read_text(encoding="utf-8"))
    pack=json.loads(Path(ns.pack).read_text(encoding="utf-8"))
    errors=inspect(source,pack)
    warnings=inspect_copy(source,pack)
    output={"locale":pack.get("locale"),"structuralErrors":errors,"reviewWarnings":warnings,"highPriorityCount":sum(x["severity"]=="high" for x in warnings),"needsNativeEditorialReview":True}
    out=Path(ns.report);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in output.items() if k not in ("structuralErrors","reviewWarnings")},ensure_ascii=False))
    if errors: raise SystemExit(1)

if __name__=="__main__":main()