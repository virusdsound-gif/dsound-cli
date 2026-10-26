#!/usr/bin/env python3
"""
Essentium Grid Report
---------------------
Human-readable summary of the agreement ledger.

Reads:
  - essentium_state.json   (current agreements + statuses)
  - essentium_ledger.json  (hash-chained history)

Shows:
  - counts by status (PROPOSED / ACCEPTED / EXECUTED / VERIFIED / REJECTED)
  - pending items (not yet executed or verified)
  - per-agreement one-line summary
  - ledger integrity check (via ledger.verify_chain)
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

try:
    from ledger import verify_chain, load_chain
except ImportError:
    def verify_chain():
        return True, None
    def load_chain():
        return {"entries": []}


GRID = Path(__file__).resolve().parent
STATE_FILE = GRID / "essentium_state.json"
LEDGER_FILE = GRID / "essentium_ledger.json"

ORDER = ["PROPOSED", "ACCEPTED", "EXECUTED", "VERIFIED", "REJECTED"]
PENDING = {"PROPOSED", "ACCEPTED"}


def load_state():
    if not STATE_FILE.exists():
        return {}
    with STATE_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Grid state must be a JSON object")
    return data


def agreements(state):
    return state.get("agreements", [])


def bar(n, total, width=20):
    if total <= 0:
        return ""
    filled = int(round(width * n / total))
    return "#" * filled + "." * (width - filled)


def summary(state):
    items = agreements(state)
    counts = {k: 0 for k in ORDER}
    for item in items:
        s = item.get("status", "PROPOSED")
        counts[s] = counts.get(s, 0) + 1

    total = len(items)

    print("=" * 60)
    print("  ESSENTIUM GRID — AGREEMENT REPORT")
    print("=" * 60)
    print(f"  Total agreements: {total}")
    print()

    if total == 0:
        print("  (no agreements yet — run: ag new \"parties\" \"objective\" \"obligation\")")
    else:
        for k in ORDER:
            n = counts.get(k, 0)
            print(f"  {k:<9} {n:>3}  {bar(n, total)}")

    print()
    return items, counts, total


def pending(items):
    print("-" * 60)
    print("  PENDING (not yet executed / verified)")
    print("-" * 60)

    rows = [i for i in items if i.get("status") in PENDING]

    if not rows:
        print("  (none — everything is executed or closed)")
        print()
        return

    for item in rows:
        wt = len(item.get("witnesses", []))
        req = item.get("witnesses_required", 1)
        print(f"  {item['id']}  [{item.get('status')}]  witnesses {wt}/{req}")
        print(f"     parties:   {item.get('parties')}")
        print(f"     objective: {item.get('objective')}")
    print()


def all_items(items):
    print("-" * 60)
    print("  ALL AGREEMENTS")
    print("-" * 60)

    if not items:
        print("  (none)")
        print()
        return

    for item in items:
        ev = len(item.get("evidence", []) or [])
        wt = len(item.get("witnesses", []) or [])
        req = item.get("witnesses_required", 1)
        print(f"  {item['id']}  [{item.get('status')}]")
        print(f"     parties:    {item.get('parties')}")
        print(f"     objective:  {item.get('objective')}")
        print(f"     obligation: {item.get('obligation')}")
        print(f"     witnesses:  {wt}/{req}    evidence: {ev}")
        print()


def ledger_status():
    print("-" * 60)
    print("  LEDGER")
    print("-" * 60)

    chain = load_chain()
    entries = chain.get("entries", [])
    ok, bad = verify_chain()

    print(f"  entries:      {len(entries)}")

    if entries:
        print(f"  last hash:    {entries[-1]['hash'][:32]}...")
        print(f"  last event:   {entries[-1]['event']}  ({entries[-1]['agreement']})")

    if ok:
        print("  integrity:    OK — chain intact")
    else:
        print(f"  integrity:    TAMPERED — first bad entry at index {bad}")

    if LEDGER_FILE.exists():
        mtime = datetime.fromtimestamp(
            LEDGER_FILE.stat().st_mtime, tz=timezone.utc
        ).isoformat()
        print(f"  last write:   {mtime}")

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Essentium Grid Report")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    state = load_state()
    items, counts, total = summary(state)

    if args.json:
        chain = load_chain()
        ok, bad = verify_chain()
        print(json.dumps({
            "total": total,
            "counts": counts,
            "ledger_ok": ok,
            "ledger_bad_index": bad,
            "ledger_entries": len(chain.get("entries", [])),
            "agreements": items,
        }, indent=2, ensure_ascii=False))
        return

    pending(items)
    all_items(items)
    ledger_status()


if __name__ == "__main__":
    main()
