#!/usr/bin/env python3
"""Dablixx Presence Audit: read-only inventory with SHA-256 hashes."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.home() / "workspace" / "dsound-cli"
OUT = ROOT / "dablixx_presence_output"

SKIP = {
    ".git", "node_modules", ".venv", "venv", "__pycache__",
    "secrets", "private", "sealed", "seals", "backups",
}
AUDIO = {".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg", ".opus"}
LYRICS = {".lrc", ".srt", ".vtt"}
DOCS = {".md", ".txt", ".json", ".csv"}

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    if not ROOT.is_dir():
        raise SystemExit(f"Project directory missing: {ROOT}")

    records = []
    for p in ROOT.rglob("*"):
        if not p.is_file() or any(part in SKIP for part in p.relative_to(ROOT).parts):
            continue
        suffix = p.suffix.lower()
        name = p.name.lower()

        if suffix in AUDIO:
            kind = "audio_file"
        elif suffix in LYRICS:
            kind = "lyric_subtitle_file"
        elif suffix in DOCS and (
            any(word in name for word in ("track", "music", "lyric",
                                           "artist", "dablixx", "catalog"))
            or name in {"readme.md", "full_tree.txt", "project_tree.txt"}
        ):
            kind = "candidate_record"
        else:
            continue

        try:
            records.append({
                "path": str(p.relative_to(ROOT)),
                "kind": kind,
                "bytes": p.stat().st_size,
                "sha256": digest(p),
                "presence": "FILE_PRESENT",
            })
        except OSError as e:
            records.append({
                "path": str(p.relative_to(ROOT)),
                "kind": kind,
                "presence": "READ_ERROR",
                "reason": type(e).__name__,
            })

    records.sort(key=lambda x: x["path"])
    counts = {
        key: sum(r["kind"] == key and r["presence"] == "FILE_PRESENT"
                 for r in records)
        for key in ("audio_file", "lyric_subtitle_file", "candidate_record")
    }

    report = {
        "program": "Dablixx Presence Audit",
        "version": "1.0.0",
        "status": "PRESENCE_INVENTORY_COMPLETED",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(ROOT),
        "counts": counts,
        "records": records,
        "limitations": [
            "File presence does not prove authorship or identity.",
            "This inventory does not analyze audio or interpret lyrics.",
            "Only the listed file types and candidate record names are inventoried.",
            "A zero count means no matching file was found by this scan, "
            "not proof that the underlying work does not exist.",
            "Existing project files are read-only; output is written separately."
        ]
    }

    OUT.mkdir(parents=True, exist_ok=True)
    data = json.dumps(report, ensure_ascii=False, indent=2).encode()
    (OUT / "presence_report.json").write_bytes(data + b"\n")

    receipt = {
        "entrypoint": "dablixx_presence.py:main",
        "return_value": 0,
        "result_line": "PRESENCE_INVENTORY_COMPLETED",
        "report_sha256": hashlib.sha256(data).hexdigest(),
        "counts": counts,
    }
    receipt_bytes = json.dumps(
        receipt, sort_keys=True, separators=(",", ":")
    ).encode()
    receipt["receipt_sha256"] = hashlib.sha256(receipt_bytes).hexdigest()
    (OUT / "presence_receipt.json").write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
    )

    print("DABL IXX: PRESENCE INVENTORY COMPLETED")
    print(f"Audio files present: {counts['audio_file']}")
    print(f"Lyrics/subtitle files present: {counts['lyric_subtitle_file']}")
    print(f"Candidate records present: {counts['candidate_record']}")
    print(f"Report: {OUT / 'presence_report.json'}")
    print(f"Receipt: {OUT / 'presence_receipt.json'}")
    print("No existing project files were intentionally modified.")

if __name__ == "__main__":
    main()
