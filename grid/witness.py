#!/usr/bin/env python3

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

try:
    from ledger import append as ledger_append
except ImportError:
    def ledger_append(*_a, **_k):
        pass


GRID = Path(__file__).resolve().parent
STATE_FILE = GRID / "essentium_state.json"


def now():
    return datetime.now(timezone.utc).isoformat()


def load_state():
    if not STATE_FILE.exists():
        return {}
    with STATE_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Grid state must be a JSON object")
    return data


def save_state(state):
    temp = STATE_FILE.with_suffix(".json.tmp")
    with temp.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write("\n")
    temp.replace(STATE_FILE)


def agreements(state):
    return state.setdefault("agreements", [])


def find(items, id_):
    id_ = id_.upper()
    if not id_.startswith("AGR-"):
        id_ = f"AGR-{int(id_):04d}"
    for item in items:
        if item.get("id") == id_:
            return item
    return None


def can_accept(item):
    required = int(item.get("witnesses_required", 1))
    have = len(item.get("witnesses", []))
    if required == 0:
        return True, "no witnesses required"
    if have >= required:
        return True, f"{have}/{required} witnesses"
    return False, f"needs {required} witness(es), has {have}"


def sign(args):
    state = load_state()
    item = find(agreements(state), args.id)
    if item is None:
        print("AGREEMENT NOT FOUND:", args.id)
        return 1
    if item.get("status") != "PROPOSED":
        print(f"CANNOT WITNESS: status is {item.get('status')}, must be PROPOSED")
        return 1

    name = args.name.strip()
    if not name:
        print("WITNESS NAME REQUIRED")
        return 1

    proposer = item.get("parties", "")
    if name.lower() in proposer.lower():
        print(f"REFUSED: '{name}' is already part of the proposing parties")
        return 1

    witnesses = item.setdefault("witnesses", [])
    for w in witnesses:
        if w.get("name", "").lower() == name.lower():
            print(f"ALREADY WITNESSED by {name}")
            return 1

    witnesses.append({"name": name, "at": now()})
    item.setdefault("history", []).append(
        {"from": "PROPOSED", "to": "PROPOSED", "at": now(), "note": f"witnessed by {name}"}
    )
    save_state(state)
    ledger_append("WITNESS", item["id"], {"name": name})

    req = item.get("witnesses_required", 1)
    print("WITNESS SIGNED:", name)
    print("AGREEMENT:    ", item["id"])
    print(f"WITNESS COUNT: {len(witnesses)} / {req}")
    return 0


def list_witnesses(args):
    state = load_state()
    item = find(agreements(state), args.id)
    if item is None:
        print("AGREEMENT NOT FOUND:", args.id)
        return 1
    witnesses = item.get("witnesses", [])
    print(item["id"], "[" + item.get("status", "?") + "]")
    print("Parties:", item.get("parties"))
    if not witnesses:
        print("Witnesses: NONE")
        return 0
    print(f"Witnesses ({len(witnesses)}):")
    for w in witnesses:
        print(f"  - {w['name']}  at {w['at']}")
    return 0


def require(args):
    state = load_state()
    item = find(agreements(state), args.id)
    if item is None:
        print("AGREEMENT NOT FOUND:", args.id)
        return 1
    n = int(args.count)
    item["witnesses_required"] = n
    save_state(state)
    print(f"{item['id']} now requires {n} witness(es) before ACCEPTED")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Essentium Grid Witness (two-key)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("sign", aliases=["s"])
    p.add_argument("id")
    p.add_argument("name")

    p = sub.add_parser("list", aliases=["ls"])
    p.add_argument("id")

    p = sub.add_parser("require", aliases=["req"])
    p.add_argument("id")
    p.add_argument("count")

    args = parser.parse_args()

    if args.command in ("sign", "s"):
        raise SystemExit(sign(args))
    elif args.command in ("list", "ls"):
        raise SystemExit(list_witnesses(args))
    elif args.command in ("require", "req"):
        raise SystemExit(require(args))


if __name__ == "__main__":
    main()
