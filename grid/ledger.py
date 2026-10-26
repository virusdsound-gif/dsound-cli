#!/usr/bin/env python3

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


GRID = Path(__file__).resolve().parent
LEDGER_FILE = GRID / "essentium_ledger.json"


def now():
    return datetime.now(timezone.utc).isoformat()


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_chain():
    if not LEDGER_FILE.exists():
        return {"entries": []}
    with LEDGER_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or "entries" not in data:
        raise ValueError("Ledger file is malformed")
    return data


def save_chain(chain):
    temp = LEDGER_FILE.with_suffix(".json.tmp")
    with temp.open("w", encoding="utf-8") as f:
        json.dump(chain, f, indent=2, ensure_ascii=False)
        f.write("\n")
    temp.replace(LEDGER_FILE)


def last_hash(chain):
    entries = chain.get("entries", [])
    if not entries:
        return "0" * 64
    return entries[-1]["hash"]


def append(event, agreement, data):
    chain = load_chain()
    entries = chain.setdefault("entries", [])

    entry = {
        "index": len(entries),
        "at": now(),
        "event": event,
        "agreement": agreement,
        "data": data,
        "prev_hash": last_hash(chain),
    }

    payload = canon({
        "index": entry["index"],
        "at": entry["at"],
        "event": entry["event"],
        "agreement": entry["agreement"],
        "data": entry["data"],
        "prev_hash": entry["prev_hash"],
    })

    entry["hash"] = sha256(payload)
    entries.append(entry)
    save_chain(chain)
    return entry


def verify_chain():
    chain = load_chain()
    entries = chain.get("entries", [])
    prev = "0" * 64

    for i, entry in enumerate(entries):
        if entry.get("prev_hash") != prev:
            return False, i
        payload = canon({
            "index": entry["index"],
            "at": entry["at"],
            "event": entry["event"],
            "agreement": entry["agreement"],
            "data": entry["data"],
            "prev_hash": entry["prev_hash"],
        })
        if sha256(payload) != entry.get("hash"):
            return False, i
        prev = entry["hash"]

    return True, None


def show(_args=None):
    chain = load_chain()
    entries = chain.get("entries", [])
    if not entries:
        print("LEDGER EMPTY")
        return
    for e in entries:
        print(f"[{e['index']:04d}] {e['at']}  {e['event']:<10}  {e['agreement']}")
        print(f"        {e['data']}")
        print(f"        hash={e['hash'][:16]}...  prev={e['prev_hash'][:16]}...")


def check(_args=None):
    ok, bad = verify_chain()
    if ok:
        print("LEDGER OK - chain intact")
    else:
        print(f"LEDGER TAMPERED - first bad entry at index {bad}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check()
    else:
        show()
