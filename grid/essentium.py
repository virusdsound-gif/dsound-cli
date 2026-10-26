#!/usr/bin/env python3
"""Essentium Grid — unified. One file, one state, one hash, one maintainer.

  python3 essentium.py --check      validate only
  python3 essentium.py --export     write state + public exports
  python3 essentium.py --verify     recompute hash from state file
  python3 essentium.py --survived   print continuity brief
  python3 essentium.py --audit      print scope-bounded audit receipt
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE = ROOT / "essentium_state.json"
PUB_JSON = ROOT / "essentium_public.json"
PUB_MD = ROOT / "essentium_public.md"

SCHEMA = "essentium-grid/2.0"
MAINTAINER = {
    "id": "contributor.maintainer",
    "name": "Ibidun Olamide",
    "handle": "KNG DRIZZ",
    "label": "DJANGO Sound",
    "role": "maintainer",
    "joined": "2026-10-07",
}

BOUNDARY = {
    "ownership_claim": False,
    "endorsement_claim": False,
    "operational_control": False,
    "genealogy_claim": False,
    "party_to_agreement": False,
    "identity_merge": False,
}

SOURCES = {
    "veal": "Michael E. Veal, Fela: The Life and Times of an African Musical Icon (Temple University Press, 2000)",
    "moore": "Carlos Moore, Fela: This Bitch of a Life (1982; later editions)",
    "johnson": "Cheryl Johnson-Odim and Nina Emma Mba, For Women and the Nation: Funmilayo Ransome-Kuti of Nigeria (University of Illinois Press, 1997)",
    "oxford": "Cheryl Johnson-Odim, 'Ransome-Kuti, Funmilayo', Oxford Research Encyclopedia of African History (2018), doi:10.1093/acrefore/9780190277734.013.269",
    "shrine_site": "felakuti.com/legacy/new-afrika-shrine (family-operated site)",
    "nut": "Nigeria Union of Teachers — official history and founding records",
    "awu": "Abeokuta Women's Union — historical records, 1940s",
    "self": "Django Sound — primary self-record, maintained by Ibidun Olamide (KNG DRIZZ)",
}


def _cite(text, sid):
    if sid not in SOURCES:
        raise KeyError(sid)
    return {"claim": text, "source_id": sid, "source": SOURCES[sid],
            "verification_status": "UNVERIFIED"}


def _cont(work, continues_as, status, sid):
    if sid not in SOURCES:
        raise KeyError(sid)
    return {"work": work, "continues_as": list(continues_as), "status": status,
            "source_id": sid, "source": SOURCES[sid],
            "verification_status": "UNVERIFIED"}


def _node(nid, name, role, location, basis, cont, **extra):
    body = {
        "id": nid, "type": "cultural_heritage_node", "status": "SEALED_REFERENCE",
        "name": name, "role": role, "location": location,
        "connection_type": "cultural_reference",
        "historical_basis": basis, "continuity": cont,
        "verified_by": None, "verification_status": "UNVERIFIED",
        "boundary": dict(BOUNDARY),
    }
    body.update(extra)
    return body


NODES = [
    _node(
        "heritage.israel_oludotun_ransome_kuti",
        "Israel Oludotun Ransome-Kuti",
        "educator, Anglican clergyman, father of Fela Anikulapo Kuti",
        "Abeokuta / Nigeria",
        [
            _cite("Nigerian educator and Anglican clergyman; first president of the Nigeria Union of Teachers.", "veal"),
            _cite("Father of Fela Anikulapo Kuti; husband of Funmilayo Ransome-Kuti.", "veal"),
        ],
        _cont("education and teacher organising",
              ["Nigeria Union of Teachers", "schools he founded and led"],
              "institutional_lineage", "nut"),
    ),
    _node(
        "heritage.funmilayo_ransome_kuti",
        "Funmilayo Ransome-Kuti",
        "educator, women's rights leader, anti-colonial organiser",
        "Abeokuta, Nigeria",
        [
            _cite("Led the Abeokuta Women's Union and the campaign that deposed the Alake over colonial taxation.", "johnson"),
            _cite("Mother of Fela, Beko, Olikoye, and Dolupo Ransome-Kuti.", "oxford"),
            _cite("Born Frances Abigail Olufunmilayo Thomas, 25 October 1900, Abeokuta; died 13 April 1978.", "oxford"),
        ],
        _cont("women's anti-colonial organising and women's suffrage",
              ["Abeokuta Women's Union legacy", "Nigerian women's rights movement"],
              "movement_lineage", "johnson"),
    ),
    _node(
        "heritage.fela_anikulapo_kuti",
        "Fela Anikulapo Kuti",
        "Afrobeat bandleader, composer, political critic",
        "Lagos, Nigeria",
        [
            _cite("Opened the Afrika Shrine in Lagos in the early 1970s as a performance, political, and ritual space.", "veal"),
            _cite("Kalakuta Republic was raided and burned by the military in February 1977.", "veal"),
            _cite("Died 2 August 1997 in Lagos.", "veal"),
        ],
        _cont("Afrobeat, political critique, ritual performance",
              ["New Afrika Shrine", "Femi Kuti", "Seun Kuti", "Egypt 80 and Positive Force"],
              "living_institution", "veal"),
    ),
    _node(
        "heritage.new_afrika_shrine",
        "New Afrika Shrine",
        "living cultural institution",
        "Ikeja, Lagos, Nigeria",
        [
            _cite("Opened in 2000 by the Kuti family, led by Yeni Anikulapo-Kuti and Femi Kuti.", "shrine_site"),
            _cite("Family site: about four times the original, capacity about 2,500.", "shrine_site"),
            _cite("Family site: Femi plays Thursdays and Sundays when not on tour; most nights have no entrance fee.", "shrine_site"),
        ],
        _cont("Afrobeat as a living venue and community institution",
              ["Felabration (annual, October)", "Thursday and Sunday residencies", "ongoing community programming"],
              "active", "shrine_site"),
        founded="2000",
        founded_by=["Femi Kuti", "Yeni Anikulapo-Kuti"],
        references="Fela Anikulapo Kuti",
        relationship="living_cultural_institution",
    ),
    _node(
        "current.django_sound",
        "Django Sound / KNG DRIZZ",
        "current carrier of the continuity chain",
        "Nigeria",
        [
            _cite("Django Sound is the current label and production vehicle, maintained by Ibidun Olamide (KNG DRIZZ).", "self"),
            _cite("The work continues the Ransome-Kuti lineage of institution-building through music and cultural production.", "self"),
        ],
        _cont(
            "music production and label operation",
            [
                "Django Sound releases",
                "KNG DRIZZ catalogue",
                "ongoing cultural production in the Ransome-Kuti lineage",
            ],
            "active",
            "self",
        ),
    ),
]


def digest(state):
    payload = {
        "sources": state["sources"],
        "nodes": state["cultural_heritage_nodes"],
        "agreement_layer": state["agreement_layer"],
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()


def check(state):
    errs, ids = [], set()
    if state["agreement_layer"].get("shrine_is_party"):
        errs.append("shrine_is_party must stay false")
    for n in state["cultural_heritage_nodes"]:
        i = n.get("id")
        if i in ids:
            errs.append(f"duplicate id {i}")
        ids.add(i)
        if n.get("status") != "SEALED_REFERENCE":
            errs.append(f"{i}: status must be SEALED_REFERENCE")
        if n.get("boundary") != BOUNDARY:
            errs.append(f"{i}: boundary drifted")
        if n.get("verification_status") != "UNVERIFIED" or n.get("verified_by") is not None:
            errs.append(f"{i}: cannot self-verify")
        basis = n.get("historical_basis") or []
        if not basis:
            errs.append(f"{i}: missing historical_basis")
        for b in basis:
            if b.get("source_id") not in SOURCES or not b.get("source"):
                errs.append(f"{i}: bad source in historical_basis")
            if b.get("verification_status") != "UNVERIFIED":
                errs.append(f"{i}: claim verified without a human check")
        c = n.get("continuity") or {}
        if not c:
            errs.append(f"{i}: missing continuity block")
            continue
        if c.get("source_id") not in SOURCES or not c.get("source"):
            errs.append(f"{i}: bad source in continuity")
        if c.get("verification_status") != "UNVERIFIED":
            errs.append(f"{i}: continuity verified without a human check")
        if not c.get("continues_as"):
            errs.append(f"{i}: continuity.continues_as is empty")
    return errs


def build_state():
    return {
        "schema": SCHEMA,
        "name": "Essentium Grid",
        "role": "infrastructure",
        "anchor_reference": "heritage.new_afrika_shrine",
        "rule": "Nothing enters without a source. Nothing leaves claiming more than the source supports.",
        "purity": "Explicit relationship is not inferred relationship. A heritage node is not a party.",
        "resurrection_note": "The grid resurrects nothing. It records what already survived.",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "sources": SOURCES,
        "contributors": [dict(MAINTAINER)],
        "proposals": [
            {"id": "proposal.001", "title": "Add New Afrika Shrine node",
             "status": "CLOSED", "note": "Enacted. Reference only. Shrine is not a party."},
            {"id": "proposal.002", "title": "Add continuity layer to all heritage nodes",
             "status": "CLOSED", "note": "Enacted. Records what survived, not what was claimed."},
            {"id": "proposal.003", "title": "Unify anchor + grid into single file",
             "status": "CLOSED", "note": "Enacted. One file owns essentium_state.json."},
            {"id": "proposal.004", "title": "Add current work as fifth sealed node",
             "status": "CLOSED", "note": "Enacted. Django Sound / KNG DRIZZ recorded as current carrier."},
        ],
        "cultural_heritage_nodes": NODES,
        "agreement_layer": {
            "note": "Agreements live elsewhere. This file cannot create one.",
            "shrine_is_party": False,
        },
    }


def public_rows(nodes):
    return [{
        "id": n["id"], "name": n["name"], "role": n["role"], "location": n["location"],
        "verification_status": "UNVERIFIED",
        "sources": [{"claim": b["claim"], "source": b["source"]} for b in n["historical_basis"]],
        "continuity": {
            "work": n["continuity"]["work"],
            "continues_as": n["continuity"]["continues_as"],
            "status": n["continuity"]["status"],
            "source": n["continuity"]["source"],
        },
        "boundary": n["boundary"],
    } for n in nodes]


def to_markdown(rows, content_hash, updated_at):
    out = [
        "# Essentium Grid — public reference",
        "",
        "Infrastructure index. Not an affiliation with the New Afrika Shrine or the Kuti family.",
        "Claims stay UNVERIFIED until a person checks the cited source.",
        "",
        "The grid does not resurrect anyone. It records what already survived.",
        "",
        f"- content_hash: `{content_hash[:16]}`",
        f"- maintainer: {MAINTAINER['name']} ({MAINTAINER['handle']}) — {MAINTAINER['label']}",
        f"- updated_at: {updated_at}",
        "",
    ]
    for n in rows:
        out += [
            f"## {n['name']}",
            "",
            f"- id: {n['id']}",
            f"- role: {n['role']}",
            f"- location: {n['location']}",
            "- status: UNVERIFIED",
            "- boundary: no ownership, no endorsement, no control, no genealogy, not a party",
            "",
            "### Work",
        ]
        for b in n["sources"]:
            out.append(f"- {b['claim']}")
            out.append(f"  - source: {b['source']}")
        out += [
            "",
            "### Continuity",
            f"- work: {n['continuity']['work']}",
            f"- status: {n['continuity']['status']}",
            "- continues as:",
        ]
        for c in n["continuity"]["continues_as"]:
            out.append(f"  - {c}")
        out += [f"- source: {n['continuity']['source']}", ""]
    return "\n".join(out) + "\n"


def _fail(errs, code=1):
    print("refusing:", file=sys.stderr)
    for e in errs:
        print(f"- {e}", file=sys.stderr)
    return code


def cmd_check(state):
    errs = check(state)
    if errs:
        return _fail(errs)
    h = digest(state)
    print(f"ok — {len(state['cultural_heritage_nodes'])} nodes — {h[:16]}")
    return 0


def cmd_export(state):
    errs = check(state)
    if errs:
        return _fail(errs)

    h = digest(state)
    state["content_hash"] = h
    rows = public_rows(state["cultural_heritage_nodes"])

    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    PUB_JSON.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    PUB_MD.write_text(to_markdown(rows, h, state["updated_at"]), encoding="utf-8")

    print(f"wrote {STATE.name}")
    print(f"wrote {PUB_JSON.name} ({len(rows)} nodes)")
    print(f"wrote {PUB_MD.name}")
    print(f"content_hash: {h[:16]}")
    print("verification_status: UNVERIFIED")
    print("shrine_is_party: false")
    return 0


def cmd_verify():
    if not STATE.is_file():
        print(f"missing: {STATE}", file=sys.stderr)
        return 1
    s = json.loads(STATE.read_text(encoding="utf-8"))
    stored = s.get("content_hash", "")
    rec = digest(s)
    print(f"schema:      {s.get('schema')}")
    print(f"nodes:       {len(s.get('cultural_heritage_nodes', []))}")
    print(f"stored:      {stored[:16]}")
    print(f"recomputed:  {rec[:16]}")
    print("status:      MATCH" if stored == rec else "status:      DRIFT DETECTED")
    print(f"shrine_is_party: {s.get('agreement_layer', {}).get('shrine_is_party')}")
    return 0 if stored == rec else 2


def cmd_survived(state):
    print("WHAT SURVIVED")
    print("=" * 60)
    print(f"maintainer: {MAINTAINER['name']} ({MAINTAINER['handle']}) — {MAINTAINER['label']}")
    print("=" * 60)
    for n in state["cultural_heritage_nodes"]:
        c = n["continuity"]
        print(f"\n{n['name']}")
        print(f"  role:   {n['role']}")
        print(f"  work:   {c['work']}")
        print(f"  status: {c['status']}")
        print("  still running as:")
        for item in c["continues_as"]:
            print(f"    - {item}")
    print()
    print("=" * 60)
    print("The grid resurrects nothing. It records what already survived.")
    print("=" * 60)
    return 0


def cmd_audit(state):
    errs = check(state)
    if errs:
        return _fail(errs)
    h = digest(state)
    print("ESSENTIUM GRID — AUDIT RECEIPT")
    print("=" * 60)
    print(f"schema:              {SCHEMA}")
    print(f"nodes:               {len(state['cultural_heritage_nodes'])}")
    print(f"content_hash:        {h[:16]}")
    print(f"maintainer:          {MAINTAINER['name']} ({MAINTAINER['handle']}) — {MAINTAINER['label']}")
    print(f"shrine_is_party:     {state['agreement_layer']['shrine_is_party']}")
    print("boundary:            ownership=false endorsement=false control=false")
    print("                     genealogy=false party=false identity_merge=false")
    print("verification_status: UNVERIFIED (all claims)")
    print("=" * 60)
    print("scope: state mutation + heritage-node registration only.")
    print("not claimed: truth of any claim, endorsement, or MirrorTrace receipt.")
    print("=" * 60)
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="Essentium Grid — unified")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true")
    g.add_argument("--export", action="store_true")
    g.add_argument("--verify", action="store_true")
    g.add_argument("--survived", action="store_true")
    g.add_argument("--audit", action="store_true")
    args = p.parse_args(argv)

    if args.verify:
        return cmd_verify()

    state = build_state()
    if args.check:
        return cmd_check(state)
    if args.export:
        return cmd_export(state)
    if args.survived:
        return cmd_survived(state)
    if args.audit:
        return cmd_audit(state)

    p.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
