#!/usr/bin/env python3
"""Source-bound F3L witnessed-error regression. Not human/native editorial approval."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from f3l_translation_gate import digest, inspect

LOCALES=("en","es","fr","de","pt")
EXPECTED_SOURCE="d18d492b0db2148aed213610ffd1ff98bcff925a66cf4444a8a4da9b51576227"
WITNESSED={
 "en":(r"door to light boil",r"chicken buns",r"gaskets",r"onipollot",r"semolated sugar",r"it snows the egg white",r"egg white to repel"),
 "es":(r"ligera marca",r"bocadillos de pollo",r"huevo golpeado",r"látigo",r"despídelos",r"se tiemble",r"se tiemblen",r"se represente",r"zócalo"),
 "fr":(r"blancs d.oie",r"rayons x",r"hérisson de wasabi",r"striscioli",r"stricholine",r"joints",r"lâchez du sucre",r"se raser aux bords"),
 "de":(r"weißweine",r"nähen sie den frischen eigelb",r"kleine röhre",r"dichtungen",r"seehühnchen",r"schweineschalen",r"zwiebelgras",r"springt die garnelen"),
 "pt":(r"ela neva a branca",r"grampe o gengibre",r"consumo bruto",r"atum de raio",r"chicote",r"se afiar nas bordas",r"enrolo de wasabi",r"onipollot"),
}
TERMS={"en":("pasteur","raw","74"),"es":("pasteur","crudo","74"),"fr":("pasteuris","crue","74"),"de":("pasteuris","roh","74"),"pt":("pasteur","cru","74")}
IDS=("recipe_000055","recipe_000074","recipe_000134","recipe_000146","recipe_000160","recipe_000162")

def check(source, packs):
    issues=[]
    if digest(source)!=EXPECTED_SOURCE:issues.append("Italian editorial source fingerprint drift")
    src={r["id"]:r for r in source["recipes"]}
    for rid in IDS:
        if src[rid]["targetContentVersion"]!=(4 if rid=="recipe_000074" else 3):issues.append(f"{rid}: expected approved source version mismatch")
    if src["recipe_000089"]["targetContentVersion"]!=3:issues.append("recipe_000089 historical version changed")
    if "pastorizzat" not in src["recipe_000162"]["ingredients"][3]["name"].lower():issues.append("Italian yuzu unpasteurized")
    ref=next(x for x in src["recipe_000074"]["animeReview"]["references"] if x["workTitle"]=="One Piece")
    if ref.get("episode")!="966" or "one-piece.com" not in ref.get("evidenceSource",""):issues.append("One Piece provenance not source-specific")
    for locale in LOCALES:
        pack=packs[locale]
        issues.extend(f"{locale}: {e}" for e in inspect(source,pack))
        if pack.get("reviewStatus")!="machine_draft_not_publishable" or not pack.get("editorialStaging",{}).get("noAutomaticPublication"):issues.append(f"{locale}: lost publication quarantine")
        if len(pack.get("recipes",[]))!=112 or len(pack.get("reusableComponents",{}))!=10:issues.append(f"{locale}: coverage")
        if any(x.get("reviewStatus")!="machine_draft" or x.get("reviewEvidence") for x in pack.get("recipes",[])):issues.append(f"{locale}: unverified review claims")
        loc={r["id"]:r for r in pack["recipes"]}
        for rid in ("recipe_000055","recipe_000134","recipe_000146","recipe_000162"):
            if not any("pasteur" in str(v).lower() or "raw" in str(v).lower() or "cru" in str(v).lower() or "roh" in str(v).lower() for v in [loc[rid].get("description","")]):issues.append(f"{locale}/{rid}: safety context missing")
        chicken=loc["recipe_000055"]["steps"][4]["instruction"]
        if "74" not in chicken:issues.append(f"{locale}: safe poultry core temperature missing")
        yuzu=loc["recipe_000162"]["steps"][4]["instruction"]
        if not re.search(r"pasteur",yuzu,re.I):issues.append(f"{locale}: pasteurized egg-white instruction missing")
        text_values=[]
        for row in pack["recipes"]:
            text_values.extend((row["title"],row["description"],row.get("animeContext","")))
            text_values.extend(s["instruction"] for s in row["steps"])
            text_values.extend(i["name"] for i in row["ingredients"])
        whole="\n".join(text_values)
        for pattern in WITNESSED[locale]:
            if re.search(pattern,whole,re.I):issues.append(f"{locale}: witnessed false friend still present: {pattern}")
    return issues

def load(root=Path(".")):
    source=json.loads((root/"authoring/f3k_it_hardening_51_162.json").read_text(encoding="utf-8"))
    packs={l:json.loads((root/"authoring/f3l_review_drafts"/f"f3l_{l}_51_162_review_draft.json").read_text(encoding="utf-8")) for l in LOCALES}
    return source,packs

def main():
    issues=check(*load())
    print(json.dumps({"result":"PASS" if not issues else "FAIL","witnessedIssues":len(issues),"machineDrafts":560,"nativeSignoffs":0,"releaseApproved":False,"errors":issues[:50]},ensure_ascii=False,indent=2))
    if issues:sys.exit(1)
if __name__=="__main__":main()
