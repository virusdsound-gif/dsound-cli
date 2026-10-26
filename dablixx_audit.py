#!/usr/bin/env python3
"""
Dablixx Oosha Identity & Music Audit
Read-only audit scaffold for Essentium / Django Sound.

- Does not edit existing project files.
- Writes its report and receipt only to a dedicated output directory.
- Does not claim audio analysis or identity verification without evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROGRAM_NAME = "Dablixx Oosha Identity & Music Audit"
PROGRAM_VERSION = "1.0.0"

EXPECTED_IDENTITIES = {
    "Django Sound": {
        "frequency_hz": 0.7,
        "layer": "Royal Silence Root",
        "role": "label/root",
    },
    "Dablixx Oosha": {
        "frequency_hz": 99.9,
        "layer": "Pain Alchemy",
        "role": "artist",
    },
    "KNG DRIZZ": {
        "frequency_hz": 200,
        "layer": "Spirit Bridge",
        "role": "artist",
    },
    "Vivian": {
        "frequency_hz": 369,
        "layer": "Tesla Return Gate / neutral fortress",
        "role": "protection concept",
    },
}

SYMBOLIC_RELATIONSHIPS = [
    {
        "identity": "Femi IBIDUN OLAMIDE",
        "artist": "KNG DRIZZ",
        "relationship": "symbolic twin framework",
        "status": "user-provided symbolic record; not independently verified",
    },
    {
        "identity": "Femi IBIDUN Olamilekan",
        "artist": "Dablixx Oosha",
        "relationship": "symbolic twin framework",
        "status": "user-provided symbolic record; not independently verified",
    },
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(data: Any) -> bytes:
    return json.dumps(
        data, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def safe_read_text(path: Path, limit: int = 2_000_000) -> str | None:
    """Read a small text file only; never write to the source."""
    try:
        if not path.is_file() or path.stat().st_size > limit:
            return None
        return path.read_text(encoding="utf-8", errors="replace")
    except (OSError, PermissionError):
        return None


def find_candidate_docs(root: Path) -> list[dict[str, str]]:
    """Search only a small set of documentation/data files, excluding secrets and dependencies."""
    allowed_names = {
        "README.md",
        "FULL_TREE.txt",
        "PROJECT_TREE.txt",
        "music_catalogue.json",
        "music_catalog.json",
        "tracks.json",
        "lyrics_index.json",
        "artist_profiles.json",
    }
    ignored_dirs = {
        ".git", "node_modules", ".venv", "venv", "__pycache__",
        "backups", "sealed", "seals", "secrets", "private",
    }
    results: list[dict[str, str]] = []
    try:
        for path in root.rglob("*"):
            if any(part in ignored_dirs for part in path.parts):
                continue
            if path.name not in allowed_names:
                continue
            content = safe_read_text(path)
            if content is None:
                continue
            results.append({
                "path": str(path.relative_to(root)),
                "sha256": sha256_bytes(content.encode("utf-8")),
                "bytes": str(len(content.encode("utf-8"))),
                "status": "read-only file inspected",
            })
            if len(results) >= 100:
                break
    except (OSError, PermissionError):
        pass
    return sorted(results, key=lambda item: item["path"])


def load_evidence_file(path: Path | None) -> tuple[dict[str, Any], str | None]:
    if path is None:
        return {}, None
    try:
        raw = path.read_bytes()
        parsed = json.loads(raw.decode("utf-8"))
        if not isinstance(parsed, dict):
            raise ValueError("JSON root must be an object")
        return parsed, sha256_bytes(raw)
    except Exception as exc:
        return {}, f"Could not load evidence JSON: {type(exc).__name__}: {exc}"


def audit(root: Path, evidence_path: Path | None) -> dict[str, Any]:
    evidence, evidence_error = load_evidence_file(evidence_path)
    docs = find_candidate_docs(root)

    evidence_tracks = evidence.get("tracks", [])
    if not isinstance(evidence_tracks, list):
        evidence_tracks = []

    track_results = []
    for index, track in enumerate(evidence_tracks, start=1):
        if not isinstance(track, dict):
            track_results.append({
                "item": index,
                "status": "INCOMPLETE",
                "reason": "Track entry must be a JSON object.",
            })
            continue
        required = ("title", "artist", "source")
        missing = [key for key in required if not str(track.get(key, "")).strip()]
        has_lyrics = bool(str(track.get("lyrics_excerpt", "")).strip())
        has_audio_ref = bool(str(track.get("audio_file", "")).strip())
        track_results.append({
            "item": index,
            "title": str(track.get("title", "")).strip() or None,
            "artist": str(track.get("artist", "")).strip() or None,
            "source": str(track.get("source", "")).strip() or None,
            "lyrics_evidence_present": has_lyrics,
            "audio_reference_present": has_audio_ref,
            "status": "INCOMPLETE" if missing else (
                "EVIDENCE PROVIDED — NOT INDEPENDENTLY VERIFIED"
            ),
            "missing_fields": missing,
            "note": "Lyrics excerpts and audio references are evidence pointers, not proof of authorship.",
        })

    README_text = ""
    for item in docs:
        if item["path"].lower() == "readme.md":
            content = safe_read_text(root / item["path"])
            README_text = content or ""
            break

    doc_mentions = {
        "Dablixx Oosha": "dablixx" in README_text.lower(),
        "99.9 Hz": "99.9" in README_text,
        "Pain Alchemy": "pain alchemy" in README_text.lower(),
        "KNG DRIZZ": "kng drizz" in README_text.lower(),
        "200 Hz": "200" in README_text,
        "Django Sound": "django sound" in README_text.lower(),
        "0.7 Hz": "0.7" in README_text,
        "369 Hz / Vivian": "369" in README_text and "vivian" in README_text.lower(),
    }

    issues = []
    if not evidence_tracks:
        issues.append("No track-level evidence supplied; catalogue and lyrical fingerprint remain unverified.")
    if not docs:
        issues.append("No candidate documentation/data files were found within the scanned project.")
    if evidence_error:
        issues.append(evidence_error)

    return {
        "program": PROGRAM_NAME,
        "version": PROGRAM_VERSION,
        "run_status": "AUDIT_COMPLETED",
        "execution_mode": "local read-only audit",
        "generated_at_utc": utc_now(),
        "project_root": str(root.resolve()),
        "python_version": platform.python_version(),
        "identity_assignments": EXPECTED_IDENTITIES,
        "symbolic_relationships": SYMBOLIC_RELATIONSHIPS,
        "repository_documentation_checks": doc_mentions,
        "candidate_files_read_only_inspected": docs,
        "track_evidence_results": track_results,
        "evidence_file": str(evidence_path.resolve()) if evidence_path else None,
        "evidence_file_sha256": evidence.get("_source_sha256") if evidence else None,
        "issues": issues,
        "limitations": [
            "Frequency values are symbolic project assignments; this program does not measure audio frequency.",
            "A listed symbolic relationship is not proof of literal identity or biological twinship.",
            "This scaffold does not infer lyrics, artist authorship, or catalogue completeness.",
            "No existing project, protected, or sealed file is changed.",
            "Repository documentation presence is not runtime verification.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only Dablixx Oosha music/identity audit with SHA-256 receipt."
    )
    parser.add_argument(
        "--root", default=".",
        help="Project directory to inspect (default: current directory).",
    )
    parser.add_argument(
        "--evidence", default=None,
        help="Optional JSON file containing track evidence.",
    )
    parser.add_argument(
        "--out", default="dablixx_audit_output",
        help="Dedicated output directory (default: ./dablixx_audit_output).",
    )
    args = parser.parse_args()

    root = Path(args.root).expanduser()
    if not root.exists() or not root.is_dir():
        print(f"ERROR: project root is not a directory: {root}", file=sys.stderr)
        return 2

    evidence_path = Path(args.evidence).expanduser() if args.evidence else None
    if evidence_path and not evidence_path.is_file():
        print(f"ERROR: evidence file not found: {evidence_path}", file=sys.stderr)
        return 2

    output_dir = Path(args.out).expanduser()
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"ERROR: cannot create output directory: {exc}", file=sys.stderr)
        return 2

    report = audit(root.resolve(), evidence_path)
    report_bytes = json.dumps(report, ensure_ascii=False, indent=2).encode("utf-8")
    report_hash = sha256_bytes(report_bytes)

    receipt = {
        "program": PROGRAM_NAME,
        "version": PROGRAM_VERSION,
        "entrypoint": "dablixx_audit.py:main",
        "input": {
            "project_root": str(root.resolve()),
            "evidence_file": str(evidence_path.resolve()) if evidence_path else None,
        },
        "return_value": 0,
        "result_line": "AUDIT_COMPLETED",
        "report_sha256": report_hash,
        "generated_at_utc": utc_now(),
    }
    receipt["receipt_sha256"] = sha256_bytes(canonical_json(receipt))

    report_path = output_dir / "audit_report.json"
    receipt_path = output_dir / "run_receipt.json"

    try:
        report_path.write_bytes(report_bytes + b"\n")
        receipt_path.write_text(
            json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except OSError as exc:
        print(f"ERROR: cannot write audit output: {exc}", file=sys.stderr)
        return 2

    print("DABL IXX AUDIT: AUDIT_COMPLETED")
    print(f"Report:  {report_path.resolve()}")
    print(f"Receipt: {receipt_path.resolve()}")
    print(f"Report SHA-256: {report_hash}")
    print(f"Tracks reviewed: {len(report['track_evidence_results'])}")
    print("Protected source files: not modified by this program.")
    print("Note: completion means the audit ran; it does not mean all claims were verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

