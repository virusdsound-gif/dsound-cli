#!/usr/bin/env python3
"""
Ledger compaction (safe).

- Keeps the head (most recent N entries) in essentium_ledger.json
- Moves older entries into essentium_ledger_archive.json
- Writes a checkpoint entry that chains archive head -> live head
- verify_chain() still works across both files

Never deletes a hash. Never rewrites a past entry.
"""

import argparse
import json
from pathlib import Path

try:
    from ledger import verify_chain, canon, sha256, load_chain, save_chain
except ImportError:
    import sys
    print("Run from the grid/ directory (needs ledger.py)")
    sys.exit(1)


GRID = Path(__file__).resolve().parent
LIVE = GRID / "essentium_ledger.json"
ARCHIVE = GRID / "essentium_ledger_archive.json"
CHECKPOINTS = GRID / "essentium_ledger_checkpoints.json"

KEEP = 200


def load_json(p, default):
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def write_json(p, data):
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", type=int, default=KEEP)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ok, bad = verify_chain()
    if not ok:
        print(f"REFUSED: ledger tampered at index {bad}")
        return 1

    live = load_json(LIVE, {"entries": []})
    entries = live.get("entries", [])

    if len(entries) <= args.keep:
        print(f"NOTHING TO DO — {len(entries)} entries <= keep={args.keep}")
        return 0

    head = entries[-args.keep:]
    tail = entries[:-args.keep]

    archive = load_json(ARCHIVE, {"entries": []})
    archive["entries"].extend(tail)

    checkpoint = {
        "at": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "archived_count": len(tail),
        "archive_head_hash": tail[-1]["hash"] if tail else None,
        "live_head_hash_before": head[0]["prev_hash"] if head else None,
        "live_head_hash_after": head[0]["hash"] if head else None,
    }

    cps = load_json(CHECKPOINTS, {"checkpoints": []})
    cps["checkpoints"].append(checkpoint)

    if args.dry_run:
        print(f"DRY RUN — would archive {len(tail)}, keep {len(head)}")
        print(f"checkpoint: {checkpoint}")
        return 0

    write_json(ARCHIVE, archive)
    write_json(LIVE, {"entries": head})
    write_json(CHECKPOINTS, cps)

    print(f"COMPACTED — archived {len(tail)}, kept {len(head)}")
    print(f"archive:     {ARCHIVE.name}")
    print(f"checkpoints: {CHECKPOINTS.name}")

    ok, bad = verify_chain()
    if not ok:
        print(f"WARNING: post-compact verify says tampered at {bad}")
        return 1
    print("VERIFY OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
