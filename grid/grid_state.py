#!/usr/bin/env python3
"""
Essentium Grid State
--------------------
Single view of Grid health across all modules.

Commands:
  status      quick overview
  diagnose    deep check with problems called out
"""

import argparse
import json
import shutil
import subprocess
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
CONFIG_FILE = GRID / ".sync_config.json"
MIRROR_DIR = GRID / ".mirror"


def now():
    return datetime.now(timezone.utc).isoformat()


def load_state():
    if not STATE_FILE.exists():
        return {}
    with STATE_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def agreements(state):
    return state.get("agreements", [])


def count_by_status(items):
    counts = {}
    for it in items:
        s = it.get("status", "PROPOSED")
        counts[s] = counts.get(s, 0) + 1
    return counts


def pending(items):
    return [i for i in items if i.get("status") in ("PROPOSED", "ACCEPTED")]


def overdue(items, hours=72):
    """Agreements stuck in non-terminal state longer than N hours."""
    cutoff = datetime.now(timezone.utc).timestamp() - hours * 3600
    stuck = []
    for it in items:
        if it.get("status") in ("VERIFIED", "REJECTED"):
            continue
        ts = it.get("accepted_at") or it.get("created_at")
        if not ts:
            continue
        try:
            t = datetime.fromisoformat(ts).timestamp()
            if t < cutoff:
                stuck.append((it, round((datetime.now(timezone.utc).timestamp() - t) / 3600, 1)))
        except ValueError:
            pass
    return stuck


def file_line(label, path):
    if path.exists():
        size = path.stat().st_size
        mtime = datetime.fromtimestamp(
            path.stat().st_mtime, tz=timezone.utc
        ).isoformat(timespec="seconds")
        return f"  {label:<22} {size:>8} bytes   {mtime}"
    return f"  {label:<22} MISSING"


def git_info():
    cfg = {}
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open("r", encoding="utf-8") as f:
            cfg = json.load(f)

    if not cfg.get("remote"):
        return "  sync:                  NOT CONFIGURED (run: sy init <url>)"

    lines = [f"  sync remote:           {cfg['remote']}"]

    if not MIRROR_DIR.exists():
        lines.append("  mirror:                MISSING (run: sy push)")
        return "\n".join(lines)

    if not shutil.which("git"):
        lines.append("  git:                   NOT INSTALLED")
        return "\n".join(lines)

    r = subprocess.run(
        ["git", "status", "--short"],
        cwd=MIRROR_DIR, capture_output=True, text=True, check=False
    )
    dirty = bool(r.stdout.strip())
    lines.append(f"  mirror state:          {'DIRTY (unpushed changes)' if dirty else 'clean'}")

    r2 = subprocess.run(
        ["git", "log", "-1", "--format=%h %ci %s"],
        cwd=MIRROR_DIR, capture_output=True, text=True, check=False
    )
    if r2.returncode == 0 and r2.stdout.strip():
        lines.append(f"  last commit:           {r2.stdout.strip()}")

    return "\n".join(lines)


def cmd_status(_args):
    state = load_state()
    items = agreements(state)
    counts = count_by_status(items)
    chain = load_chain()
    entries = chain.get("entries", [])
    ok, bad = verify_chain()

    print("=" * 60)
    print("  ESSENTIUM GRID — STATUS")
    print("  " + now())
    print("=" * 60)
    print()
    print("AGREEMENTS")
    print(f"  total:                 {len(items)}")
    for k in ("PROPOSED", "ACCEPTED", "EXECUTED", "VERIFIED", "REJECTED"):
        if counts.get(k):
            print(f"  {k:<22} {counts[k]}")
    print()
    print("LEDGER")
    print(f"  entries:               {len(entries)}")
    print(f"  integrity:             {'OK' if ok else f'TAMPERED at index {bad}'}")
    print()
    print("FILES")
    print(file_line("state:", STATE_FILE))
    print(file_line("ledger:", LEDGER_FILE))
    print(file_line("sync config:", CONFIG_FILE))
    print()
    print("SYNC")
    print(git_info())
    print("=" * 60)


def cmd_diagnose(_args):
    state = load_state()
    items = agreements(state)
    counts = count_by_status(items)
    chain = load_chain()
    entries = chain.get("entries", [])
    ok, bad = verify_chain()

    problems = []
    warnings = []
    notes = []

    # 1. Files
    if not STATE_FILE.exists():
        problems.append("essentium_state.json is MISSING")
    if not LEDGER_FILE.exists():
        warnings.append("essentium_ledger.json is MISSING (no history recorded yet)")

    # 2. Ledger integrity
    if not ok:
        problems.append(f"LEDGER TAMPERED — first bad entry at index {bad}")
    else:
        notes.append(f"Ledger integrity OK ({len(entries)} entries)")

    # 3. Cross-check: every agreement should appear in the ledger
    ledger_ids = {e.get("agreement") for e in entries}
    for it in items:
        if it.get("id") not in ledger_ids:
            problems.append(f"{it.get('id')} exists in state but has NO ledger entries")

    # 4. Witness rules on non-proposed items
    for it in items:
        status = it.get("status", "PROPOSED")
        if status in ("ACCEPTED", "EXECUTED", "VERIFIED"):
            req = int(it.get("witnesses_required", 1))
            have = len(it.get("witnesses", []))
            if have < req:
                problems.append(
                    f"{it.get('id')} is {status} but only has {have}/{req} witnesses"
                )

    # 5. Verified items must have evidence
    for it in items:
        if it.get("status") == "VERIFIED" and not it.get("evidence"):
            problems.append(f"{it.get('id')} is VERIFIED but has NO evidence")

    # 6. Orphan ledger entries (agreement ids in ledger but not in state)
    state_ids = {it.get("id") for it in items}
    for e in entries:
        if e.get("agreement") not in state_ids:
            warnings.append(
                f"Ledger entry {e['index']} references {e['agreement']} "
                "which is not in state"
            )

    # 7. Stuck agreements
    stuck = overdue(items, hours=72)
    for it, hrs in stuck:
        warnings.append(
            f"{it.get('id')} has been {it.get('status')} for {hrs}h (possible stall)"
        )

    # 8. Sync
    if CONFIG_FILE.exists():
        if not MIRROR_DIR.exists():
            warnings.append("sync configured but no mirror — run: sy push")
        else:
            notes.append("sync mirror present")
    else:
        notes.append("sync not configured (optional)")

    # ---- print report ----
    print("=" * 60)
    print("  ESSENTIUM GRID — DIAGNOSE")
    print("  " + now())
    print("=" * 60)
    print()
    print(f"Agreements:   {len(items)}")
    print(f"Ledger:       {len(entries)} entries")
    print(f"Integrity:    {'OK' if ok else 'TAMPERED'}")
    print()

    if not problems and not warnings:
        print("  ALL GOOD — no problems, no warnings.")
    if problems:
        print(f"  PROBLEMS ({len(problems)}):")
        for p in problems:
            print(f"    ✗ {p}")
        print()
    if warnings:
        print(f"  WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"    ! {w}")
        print()
    if notes:
        print("  NOTES:")
        for n in notes:
            print(f"    · {n}")

    print()
    print("=" * 60)

    if problems:
        raise SystemExit(1)


def main():
    parser = argparse.ArgumentParser(description="Essentium Grid State")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", aliases=["st"])
    sub.add_parser("diagnose", aliases=["diag", "d"])
    args = parser.parse_args()

    if args.command in ("status", "st"):
        cmd_status(args)
    elif args.command in ("diagnose", "diag", "d"):
        cmd_diagnose(args)


if __name__ == "__main__":
    main()
