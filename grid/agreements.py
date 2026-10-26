#!/usr/bin/env python3

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


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


def next_id(items):
    numbers = []

    for item in items:
        value = str(item.get("id", ""))

        if value.startswith("AGR-"):
            try:
                numbers.append(int(value[4:]))
            except ValueError:
                pass

    return f"AGR-{max(numbers, default=0) + 1:04d}"


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
        "evidence": []
    }

    items.append(item)
    save_state(state)

    print("AGREEMENT CREATED")
    print("ID:", item["id"])
    print("STATUS:", item["status"])


def list_all(_args):
    state = load_state()
    items = agreements(state)

    if not items:
        print("NO AGREEMENTS")
        return

    for item in items:
        print()
        print(item["id"])
        print("Parties:", item.get("parties"))
        print("Objective:", item.get("objective"))
        print("Obligation:", item.get("obligation"))
        print("Status:", item.get("status"))


def change_status(args):
    state = load_state()
    items = agreements(state)

    target = None

    for item in items:
        if item.get("id") == args.id:
            target = item
            break

    if target is None:
        print("AGREEMENT NOT FOUND:", args.id)
        return 1

    allowed = {
        "PROPOSED",
        "ACCEPTED",
        "REJECTED",
        "EXECUTED",
        "VERIFIED"
    }

    if args.status not in allowed:
        print("INVALID STATUS")
        return 1

    target["status"] = args.status

    if args.status == "ACCEPTED":
        target["accepted_at"] = now()

    elif args.status == "EXECUTED":
        target["executed_at"] = now()

    elif args.status == "VERIFIED":
        target["verified_at"] = now()

    save_state(state)

    print("UPDATED:", target["id"])
    print("STATUS:", target["status"])

    return 0


def evidence(args):
    state = load_state()
    items = agreements(state)

    for item in items:
        if item.get("id") == args.id:
            item.setdefault("evidence", []).append({
                "description": args.description,
                "recorded_at": now()
            })

            save_state(state)

            print("EVIDENCE RECORDED:", args.id)
            return 0

    print("AGREEMENT NOT FOUND:", args.id)
    return 1


def main():
    parser = argparse.ArgumentParser(
        description="Essentium Grid Agreement Manager"
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True
    )

    p = sub.add_parser("add")
    p.add_argument("--parties", required=True)
    p.add_argument("--objective", required=True)
    p.add_argument("--obligation", required=True)

    sub.add_parser("list")

    p = sub.add_parser("status")
    p.add_argument("--id", required=True)
    p.add_argument(
        "--status",
        required=True,
        choices=[
            "PROPOSED",
            "ACCEPTED",
            "REJECTED",
            "EXECUTED",
            "VERIFIED"
        ]
    )

    p = sub.add_parser("evidence")
    p.add_argument("--id", required=True)
    p.add_argument("--description", required=True)

    args = parser.parse_args()

    if args.command == "add":
        add(args)

    elif args.command == "list":
        list_all(args)

    elif args.command == "status":
        raise SystemExit(change_status(args))

    elif args.command == "evidence":
        raise SystemExit(evidence(args))


if __name__ == "__main__":
    main()
