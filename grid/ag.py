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

try:
    from witness import can_accept
except ImportError:
    def can_accept(_item):
        return True, "witness module not loaded"


GRID = Path(__file__).resolve().parent
STATE_FILE = GRID / "essentium_state.json"

TRANSITIONS = {
    "PROPOSED": {"ACCEPTED", "REJECTED"},
    "ACCEPTED": {"EXECUTED", "REJECTED"},
    "REJECTED": set(),
    "EXECUTED": {"VERIFIED"},
    "VERIFIED": set(),
}

SHORT = {
    "p": "PROPOSED",
    "a": "ACCEPTED",
    "r": "REJECTED",
    "e": "EXECUTED",
    "v": "VERIFIED",
}


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


def next_id(items):
    nums = []
    for item in items:
        v = str(item.get("id", ""))
        if v.startswith("AGR-"):
            try:
                nums.append(int(v[4:]))
            except ValueError:
                pass
    return f"AGR-{max(nums, default=0) + 1:04d}"


def find(items, id_):
    id_ = id_.upper()
    if not id_.startswith("AGR-"):
        id_ = f"AGR-{int(id_):04d}"
    for item in items:
        if item.get("id") == id_:
            return item
    return None


def add(args):
    state = load_state()
    items = agreements(state)
    item = {
        "id": next_id(items),
        "parties": args.parties,
        "objective": args.objective,
        "obligation": args.obligation,
        "status": "PROPOSED",
        "created_at": now(),
        "accepted_at": None,
        "executed_at": None,
        "verified_at": None,
        "evidence": [],
        "witnesses": [],
        "witnesses_required": 1,
        "history": [{"from": None, "to": "PROPOSED", "at": now()}],
    }
    items.append(item)
    save_state(state)
    ledger_append("CREATED", item["id"], {
        "parties": item["parties"],
        "objective": item["objective"],
        "obligation": item["obligation"],
    })
    print("AGREEMENT CREATED")
    print("ID:", item["id"])
    print("STATUS:", item["status"])
    print("NOTE: needs 1 witness before ACCEPTED -> agw sign", item["id"], "\"Name\"")


def list_all(_args):
    state = load_state()
    items = agreements(state)
    if not items:
        print("NO AGREEMENTS")
        return
    for item in items:
        print()
        print(item["id"], "[" + item.get("status", "?") + "]")
        print("  Parties:   ", item.get("parties"))
        print("  Objective: ", item.get("objective"))
        print("  Obligation:", item.get("obligation"))
        ev = item.get("evidence") or []
        wt = item.get("witnesses") or []
        req = item.get("witnesses_required", 1)
        if ev:
            print("  Evidence:  ", len(ev), "entry(ies)")
        print("  Witnesses: ", len(wt), f"/ {req} required")


def change_status(item, new_status):
    current = item.get("status", "PROPOSED")

    if new_status == "ACCEPTED":
        ok, reason = can_accept(item)
        if not ok:
            print("CANNOT ACCEPT:", reason)
            print(f"Run: agw sign {item['id']} \"Witness Name\"")
            return 1

    allowed = TRANSITIONS.get(current, set())
    if new_status not in allowed:
        print(f"ILLEGAL TRANSITION: {current} -> {new_status}")
        print(f"Allowed from {current}: {sorted(allowed) or 'NONE (terminal)'}")
        return 1

    item["status"] = new_status
    if new_status == "ACCEPTED":
        item["accepted_at"] = now()
    elif new_status == "EXECUTED":
        item["executed_at"] = now()
    elif new_status == "VERIFIED":
        item["verified_at"] = now()

    item.setdefault("history", []).append(
        {"from": current, "to": new_status, "at": now()}
    )
    ledger_append("STATUS", item["id"], {"from": current, "to": new_status})
    print("UPDATED:", item["id"])
    print("STATUS:", item["status"])
    return 0


def status(args):
    state = load_state()
    items = agreements(state)
    item = find(items, args.id)
    if item is None:
        print("AGREEMENT NOT FOUND:", args.id)
        return 1
    new_status = SHORT.get(args.status.lower())
    if new_status is None:
        new_status = args.status.upper()
    rc = change_status(item, new_status)
    if rc == 0:
        save_state(state)
    return rc


def evidence(args):
    state = load_state()
    items = agreements(state)
    item = find(items, args.id)
    if item is None:
        print("AGREEMENT NOT FOUND:", args.id)
        return 1
    item.setdefault("evidence", []).append(
        {"description": args.description, "recorded_at": now()}
    )
    save_state(state)
    ledger_append("EVIDENCE", item["id"], {"description": args.description})
    print("EVIDENCE RECORDED:", item["id"])
    return 0


def verify(args):
    state = load_state()
    items = agreements(state)
    item = find(items, args.id)
    if item is None:
        print("AGREEMENT NOT FOUND:", args.id)
        return 1
    if not item.get("evidence"):
        print("CANNOT VERIFY: no evidence recorded")
        print(f"Run: ag ev {item['id']} \"your evidence\"")
        return 1
    rc = change_status(item, "VERIFIED")
    if rc == 0:
        ledger_append("SEALED", item["id"], {"status": "VERIFIED"})
        save_state(state)
    return rc


def main():
    parser = argparse.ArgumentParser(description="Essentium Grid Agreement Manager")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add", aliases=["new"])
    p.add_argument("parties")
    p.add_argument("objective")
    p.add_argument("obligation")

    sub.add_parser("list", aliases=["ls"])

    p = sub.add_parser("status", aliases=["st"])
    p.add_argument("id")
    p.add_argument("status")

    p = sub.add_parser("evidence", aliases=["ev"])
    p.add_argument("id")
    p.add_argument("description")

    p = sub.add_parser("verify", aliases=["vf"])
    p.add_argument("id")

    args = parser.parse_args()

    if args.command in ("add", "new"):
        add(args)
    elif args.command in ("list", "ls"):
        list_all(args)
    elif args.command in ("status", "st"):
        raise SystemExit(status(args))
    elif args.command in ("evidence", "ev"):
        raise SystemExit(evidence(args))
    elif args.command in ("verify", "vf"):
        raise SystemExit(verify(args))


if __name__ == "__main__":
    main()
