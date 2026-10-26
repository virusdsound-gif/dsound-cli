#!/usr/bin/env python3
"""
Essentium Grid Sync
-------------------
Mirror essentium_state.json + essentium_ledger.json to a git repo
so the ledger survives the device. Optional IPFS pin.

Usage:
  sync init <git-remote-url>      # one-time setup
  sync push                       # commit + push state & ledger
  sync pull                       # pull remote -> local
  sync status                     # show diff vs remote
  sync ipfs                       # pin ledger to IPFS (if installed)

Config is stored at grid/.sync_config.json
"""

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from ledger import verify_chain
except ImportError:
    def verify_chain():
        return True, None


GRID = Path(__file__).resolve().parent
STATE_FILE = GRID / "essentium_state.json"
LEDGER_FILE = GRID / "essentium_ledger.json"

CONFIG_FILE = GRID / ".sync_config.json"
MIRROR_DIR = GRID / ".mirror"


def now():
    return datetime.now(timezone.utc).isoformat()


def run(cmd, cwd=None, check=True):
    result = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, check=False
    )
    if check and result.returncode != 0:
        print("COMMAND FAILED:", " ".join(cmd))
        if result.stdout.strip():
            print(result.stdout.strip())
        if result.stderr.strip():
            print(result.stderr.strip())
        sys.exit(result.returncode)
    return result


def has_git():
    return shutil.which("git") is not None


def has_ipfs():
    return shutil.which("ipfs") is not None


def load_config():
    if not CONFIG_FILE.exists():
        return {}
    with CONFIG_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_config(cfg):
    with CONFIG_FILE.open("w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
        f.write("\n")


def require_config():
    cfg = load_config()
    if not cfg.get("remote"):
        print("NOT CONFIGURED. Run:")
        print("  sync init <git-remote-url>")
        sys.exit(1)
    return cfg


def ensure_mirror(cfg):
    """Clone or refresh the mirror repo."""
    if not MIRROR_DIR.exists():
        print("Cloning mirror into", MIRROR_DIR)
        run(["git", "clone", cfg["remote"], str(MIRROR_DIR)])
    return MIRROR_DIR


def cmd_init(args):
    if not has_git():
        print("ERROR: git is not installed")
        print("In Termux: pkg install git")
        sys.exit(1)

    remote = args.remote.strip()
    if not remote:
        print("REMOTE REQUIRED")
        sys.exit(1)

    cfg = {"remote": remote, "created_at": now()}
    save_config(cfg)

    if MIRROR_DIR.exists():
        shutil.rmtree(MIRROR_DIR)

    print("Cloning mirror...")
    run(["git", "clone", remote, str(MIRROR_DIR)])

    print()
    print("SYNC CONFIGURED")
    print("  remote:", remote)
    print("  mirror:", MIRROR_DIR)
    print()
    print("Next: sync push")


def ensure_git_identity(mirror):
    email = run(["git", "config", "user.email"], cwd=mirror, check=False)
    if email.returncode != 0 or not email.stdout.strip():
        run(["git", "config", "user.email", "grid@essentium.local"], cwd=mirror)
    name = run(["git", "config", "user.name"], cwd=mirror, check=False)
    if name.returncode != 0 or not name.stdout.strip():
        run(["git", "config", "user.name", "Essentium Grid"], cwd=mirror)


def cmd_push(_args):
    cfg = require_config()

    ok, bad = verify_chain()
    if not ok:
        print(f"REFUSED: ledger is TAMPERED at index {bad}")
        print("Fix the ledger before pushing.")
        sys.exit(1)

    mirror = ensure_mirror(cfg)
    ensure_git_identity(mirror)

    copied = []
    for src in (STATE_FILE, LEDGER_FILE):
        if src.exists():
            dst = mirror / src.name
            shutil.copy2(src, dst)
            copied.append(src.name)

    if not copied:
        print("NOTHING TO SYNC (no state or ledger file)")
        return

    run(["git", "add", *copied], cwd=mirror)

    diff = run(["git", "diff", "--cached", "--quiet"], cwd=mirror, check=False)
    if diff.returncode == 0:
        print("NO CHANGES — remote already up to date")
        return

    msg = f"grid sync {now()}"
    run(["git", "commit", "-m", msg], cwd=mirror)

    print("Pushing to", cfg["remote"])
    run(["git", "push"], cwd=mirror)

    print()
    print("SYNCED")
    print("  files:  ", ", ".join(copied))
    print("  commit: ", msg)


def cmd_pull(_args):
    cfg = require_config()
    mirror = ensure_mirror(cfg)

    run(["git", "pull"], cwd=mirror)

    restored = []
    for name in ("essentium_state.json", "essentium_ledger.json"):
        src = mirror / name
        if src.exists():
            dst = GRID / name
            shutil.copy2(src, dst)
            restored.append(name)

    if not restored:
        print("NOTHING TO RESTORE from remote")
        return

    ok, bad = verify_chain()
    print()
    print("PULLED")
    print("  files:", ", ".join(restored))
    if ok:
        print("  ledger: OK")
    else:
        print(f"  ledger: TAMPERED at index {bad}")


def cmd_status(_args):
    cfg = require_config()
    mirror = ensure_mirror(cfg)

    run(["git", "fetch"], cwd=mirror, check=False)

    print("=" * 60)
    print("  SYNC STATUS")
    print("=" * 60)
    print("  remote:", cfg["remote"])
    print("  mirror:", mirror)
    print()

    r = run(["git", "status", "--short"], cwd=mirror, check=False)
    if r.stdout.strip():
        print("  local changes in mirror:")
        for line in r.stdout.strip().splitlines():
            print("   ", line)
    else:
        print("  mirror is clean")

    print()

    for name in ("essentium_state.json", "essentium_ledger.json"):
        local = GRID / name
        remote = mirror / name
        if not local.exists() and not remote.exists():
            print(f"  {name}: missing both sides")
            continue
        if not remote.exists():
            print(f"  {name}: only local")
            continue
        if not local.exists():
            print(f"  {name}: only remote")
            continue
        same = local.read_bytes() == remote.read_bytes()
        print(f"  {name}: {'IN SYNC' if same else 'DIFFERS'}")

    print("=" * 60)


def cmd_ipfs(_args):
    if not has_ipfs():
        print("IPFS NOT INSTALLED")
        print("Termux: pkg install ipfs  (or skip this step)")
        sys.exit(1)

    if not LEDGER_FILE.exists():
        print("NO LEDGER FILE TO PIN")
        sys.exit(1)

    r = run(["ipfs", "add", "-Q", str(LEDGER_FILE)])
    cid = r.stdout.strip()

    print("LEDGER PINNED")
    print("  CID:", cid)
    print("  file:", LEDGER_FILE)
    print()
    print("Anyone with this CID can fetch the exact ledger bytes.")


def main():
    parser = argparse.ArgumentParser(description="Essentium Grid Sync")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init")
    p.add_argument("remote")

    sub.add_parser("push")
    sub.add_parser("pull")
    sub.add_parser("status")
    sub.add_parser("ipfs")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init(args)
    elif args.command == "push":
        cmd_push(args)
    elif args.command == "pull":
        cmd_pull(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "ipfs":
        cmd_ipfs(args)


if __name__ == "__main__":
    main()
