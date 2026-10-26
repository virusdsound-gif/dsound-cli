#!/usr/bin/env python3

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

CANDIDATES = [
    Path("grid/essentium_state.json"),
    Path("essentium_state.json"),
    Path.home() / "workspace/dsound-cli/grid/essentium_state.json",
    Path.home() / "workspace/dsound-cli/essentium_state.json",
]

ANCHOR_ID = "heritage.israel_oludotun_ransome_kuti"


def now():
    return datetime.now(timezone.utc).isoformat()


def find_state():
    for path in CANDIDATES:
        if path.is_file():
            return path
    return None


def main():
    state = find_state()

    if state is None:
        print("NO_STATE_FOUND")
        print("No existing Essentium state JSON was found.")
        return 2

    try:
        with state.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"STATE_READ_ERROR: {e}")
        return 3

    if not isinstance(data, dict):
        print("STATE_FORMAT_ERROR")
        return 4

    backup = state.with_name(
        state.name + ".bak_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    shutil.copy2(state, backup)

    nodes = data.setdefault("cultural_heritage_nodes", [])

    anchor = {
        "id": ANCHOR_ID,
        "type": "cultural_heritage_node",
        "status": "SEALED_REFERENCE",
        "name": "Rev. Canon Israel Oludotun Ransome-Kuti",
        "relationship": "father_of_fela_anikulapo_kuti",
        "role": "education_and_cultural_heritage_anchor",
        "scope": "Essentium cultural layer",
        "connection_type": "cultural_reference",
        "essentium_links": [
            "Fela Anikulapo Kuti",
            "Fela Shrine / New Afrika Shrine",
            "Uzama (Shallipopi)",
            "Django Sound",
            "KNG DRIZZ",
            "Essentium Grid"
        ],
        "boundary": {
            "personal_genealogy_claim": False,
            "bloodline_claim": False,
            "endorsement_claim": False,
            "ownership_claim": False,
            "historical_identity_merge": False
        },
        "updated_at": now()
    }

    replaced = False
    for i, node in enumerate(nodes):
        if isinstance(node, dict) and node.get("id") == ANCHOR_ID:
            nodes[i] = anchor
            replaced = True
            break

    if not replaced:
        nodes.append(anchor)

    audit = data.setdefault("grid_audit", [])
    audit.append({
        "event": "HERITAGE_ANCHOR_UPSERT",
        "target": ANCHOR_ID,
        "timestamp": now(),
        "mutation_scope": "cultural_heritage_nodes_only",
        "mirrortrace": "UNCHANGED",
        "existing_records_deleted": 0
    })

    temp = state.with_suffix(state.suffix + ".tmp")
    with temp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    temp.replace(state)

    print("ESSENTIUM HERITAGE ANCHOR: OK")
    print(f"State: {state}")
    print(f"Backup: {backup}")
    print(f"Node: {ANCHOR_ID}")
    print("MirrorTrace: UNCHANGED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
