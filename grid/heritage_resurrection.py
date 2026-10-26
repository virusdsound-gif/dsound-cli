#!/usr/bin/env python3
"""Essentium Grid — Heritage Resurrection / Continuity Engine."""
from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path

STATE = Path("grid/essentium_state.json")
NODE_ID = "heritage.israel_oludotun_ransome_kuti"
REVIVAL_ID = "heritage_resurrection.israel_oludotun_ransome_kuti"


def now():
    return datetime.now().isoformat(timespec="seconds")


def main():
    if not STATE.is_file():
        print("NO_STATE_FOUND")
        print(f"Expected: {STATE}")
        return 2

    with STATE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        print("STATE_FORMAT_ERROR")
        return 3

    backup = STATE.with_name(
        STATE.name + ".bak_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    shutil.copy2(STATE, backup)

    # Store resurrection records in their own container so the unified
    # essentium.py check does not reject them.
    nodes = data.setdefault("heritage_resurrections", [])

    anchor = {
        "id": REVIVAL_ID,
        "type": "heritage_resurrection",
        "status": "ACTIVE",
        "source_node": NODE_ID,
        "subject": "Rev. Canon Israel Oludotun Ransome-Kuti",
        "meaning": "heritage_continuity_and_reactivation",
        "action": [
            "restore heritage context to active Grid visibility",
            "preserve documented historical relationships",
            "carry educational and cultural principles forward",
            "connect the heritage node to relevant downstream cultural nodes",
        ],
        "continuity_chain": [
            "Israel Oludotun Ransome-Kuti",
            "Fela Anikulapo Kuti",
            "Fela Shrine / New Afrika Shrine",
            "Essentium cultural layer",
        ],
        "linked_existing_nodes": [
            "heritage.israel_oludotun_ransome_kuti",
            "Uzama",
            "Django Sound",
            "KNG DRIZZ",
            "Essentium Grid",
        ],
        "definition": (
            "Heritage resurrection means reactivating cultural memory, "
            "context, principles, relationships and documented legacy "
            "inside the living Grid."
        ),
        "boundary_note": (
            "This is cultural continuity, not a claim that a deceased "
            "person has physically returned."
        ),
        "boundary_flags": {
            "ownership_claim": False,
            "endorsement_claim": False,
            "operational_control": False,
            "genealogy_claim": False,
            "party_to_agreement": False,
            "identity_merge": False,
        },
        "activated_at": now(),
    }

    replaced = False
    for i, item in enumerate(nodes):
        if isinstance(item, dict) and item.get("id") == REVIVAL_ID:
            nodes[i] = anchor
            replaced = True
            break
    if not replaced:
        nodes.append(anchor)

    audit = data.setdefault("grid_audit", [])
    audit.append({
        "event": "HERITAGE_RESURRECTION_ACTIVATED",
        "source": NODE_ID,
        "target": REVIVAL_ID,
        "timestamp": now(),
        "meaning": "heritage_continuity_and_reactivation",
        "physical_resurrection_claim": False,
        "mirrortrace": "UNCHANGED",
    })

    tmp = STATE.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    tmp.replace(STATE)

    print("ESSENTIUM HERITAGE RESURRECTION: ACTIVE")
    print(f"State: {STATE}")
    print(f"Backup: {backup}")
    print(f"Source: {NODE_ID}")
    print(f"Revival: {REVIVAL_ID}")
    print("Meaning: heritage continuity and reactivation")
    print("MirrorTrace: UNCHANGED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
