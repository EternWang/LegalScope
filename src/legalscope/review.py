"""Offline preparation and validation for a new case reference comparison.

This module makes no network calls and does not implement the historical judge.
Model answers and the identity map are private experiment outputs.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
from statistics import mean


REFERENCE_FIELDS = ("scoring_prompt", "citation_basis", "supported_proposition", "review_constraints")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encoded(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def jsonl(rows) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows).encode("utf-8")


def read_rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def nonempty(value, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be nonempty text")
    return value


def keyed(rows: list[dict], key: str) -> dict:
    result = {}
    for row in rows:
        value = nonempty(row.get(key), key)
        if value in result:
            raise ValueError(f"Duplicate {key}: {value}")
        result[value] = row
    return result


def prepare(prompts, references, responses, models, selection, run_id, variant,
            patches=None):
    """Return blinded packets, a separate private index, and coverage metadata.

    An explicit model roster and selection make missing responses detectable.
    Patches replace citation text only, with an exact before-value check.
    Extra source fields (including old scores) never enter evaluator packets.
    """
    nonempty(run_id, "run_id")
    nonempty(variant, "variant")
    if not models or len(set(models)) != len(models):
        raise ValueError("A nonempty, unique model roster is required")
    if not selection or len(set(selection)) != len(selection):
        raise ValueError("A nonempty, unique selection is required")
    for value in models:
        nonempty(value, "model")
    by_prompt = keyed(prompts, "review_id")
    by_ref = keyed(references, "review_id")
    if set(by_prompt) != set(by_ref):
        raise ValueError("Prompt and reference IDs differ")
    for rid, prompt in by_prompt.items():
        ref = by_ref[rid]
        for key in ("document_id", "issue_id"):
            if nonempty(prompt.get(key), key) != nonempty(ref.get(key), key):
                raise ValueError(f"Case/issue join mismatch for {rid}")
        nonempty(prompt.get("prompt"), "prompt")
        for key in REFERENCE_FIELDS:
            nonempty(ref.get(key), key)
    if not set(selection) <= set(by_prompt):
        raise ValueError("Unknown selected review ID")
    patched = {}
    for patch in patches or []:
        rid = patch.get("review_id")
        if rid not in selection or rid in patched:
            raise ValueError("Patch ID must be selected and unique")
        if patch.get("before") != by_ref[rid]["citation_basis"]:
            raise ValueError(f"Patch does not match the historical reference: {rid}")
        patched[rid] = nonempty(patch.get("after"), "patch after")
    answers = {}
    for row in responses:
        rid = row.get("review_id")
        model = row.get("model")
        if rid not in by_prompt or model not in models:
            raise ValueError("Unknown response review ID or model")
        pair = (rid, model)
        if pair in answers:
            raise ValueError("Duplicate response pair")
        answers[pair] = nonempty(row.get("response"), "response")
    expected = {(rid, model) for rid in selection for model in models}
    if not expected <= set(answers):
        raise ValueError("Missing selected model responses")
    packets, index = [], []
    for rid, model in sorted(expected):
        response_id = digest(encoded([run_id, variant, rid, model]))
        reference = {key: by_ref[rid][key] for key in REFERENCE_FIELDS}
        if rid in patched:
            reference["citation_basis"] = patched[rid]
        packets.append({"response_id": response_id, "prompt": by_prompt[rid]["prompt"],
                        "response": answers[(rid, model)], "reference": reference})
        index.append({"response_id": response_id, "review_id": rid, "model": model,
                      "variant": variant})
    packets.sort(key=lambda r: r["response_id"])
    index.sort(key=lambda r: r["response_id"])
    metadata = {"run_id": run_id, "variant": variant, "prompt_count": len(selection),
                "model_count": len(models), "packet_count": len(packets),
                "citation_patch_count": len(patched), "review_ids": sorted(selection),
                "model_roster": models, "network_calls": 0,
                "rubric_selection_required": True,
                "scope": "Offline inputs for a new experiment; not the historical scoring pipeline. "
                         "Model identity metadata and previous scores are excluded from packets; "
                         "response text is unchanged and may itself identify a model."}
    return packets, index, metadata


def validate_results(results, index):
    """Reject partial, duplicated, unknown or invalid results before aggregation."""
    by_id = keyed(index, "response_id")
    scored = keyed(results, "response_id")
    if not by_id or set(by_id) != set(scored):
        raise ValueError("Result IDs must exactly cover the complete index")
    groups = defaultdict(list)
    seen = set()
    for sid, row in scored.items():
        for dimension in ("A", "B", "C"):
            value = row.get(dimension)
            if type(value) is not int or not 0 <= value <= 4:
                raise ValueError(f"{dimension} must be an integer from 0 to 4")
        nonempty(row.get("notes"), "notes")
        entry = by_id[sid]
        key = tuple(nonempty(entry.get(k), k) for k in ("variant", "model", "review_id"))
        if key in seen:
            raise ValueError("Duplicate indexed model/prompt/variant")
        seen.add(key)
        groups[key[:2]].append(row)
    output = []
    for (variant, model), rows in sorted(groups.items()):
        scores = {name: mean(r[d] for r in rows) * 25
                  for name, d in (("citation", "A"), ("constraint", "B"), ("argument", "C"))}
        output.append({"variant": variant, "model": model, "n": len(rows), **scores,
                       "case_mean": mean(scores.values())})
    return output


def write_bundle(destination: Path, packets, index, metadata, source_hashes):
    # A fresh directory prevents a preparation run from overwriting past results.
    files = {"packets.jsonl": jsonl(packets), "identity_map.private.jsonl": jsonl(index)}
    manifest = {**metadata, "input_sha256": source_hashes,
                "files": {name: digest(body) for name, body in files.items()}}
    destination.mkdir(parents=True, exist_ok=False)
    for name, body in files.items():
        (destination / name).write_bytes(body)
    (destination / "manifest.json").write_bytes(encoded(manifest))
    return manifest


def load_index(bundle: Path):
    manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
    for name in ("packets.jsonl", "identity_map.private.jsonl"):
        if digest((bundle / name).read_bytes()) != manifest["files"][name]:
            raise ValueError("Bundle hash mismatch")
    index = read_rows(bundle / "identity_map.private.jsonl")
    if len(index) != manifest["packet_count"]:
        raise ValueError("Bundle count mismatch")
    return index


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    build = commands.add_parser("prepare")
    for name in ("prompts", "references", "responses", "models", "selection"):
        build.add_argument("--" + name, required=True, type=Path)
    build.add_argument("--citation-patch", type=Path)
    build.add_argument("--run-id", required=True)
    build.add_argument("--variant", required=True)
    build.add_argument("--out-dir", type=Path, required=True)
    check = commands.add_parser("validate")
    check.add_argument("--bundle", type=Path, required=True)
    check.add_argument("--results", type=Path, required=True)
    check.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "prepare":
        paths = {name: getattr(args, name) for name in
                 ("prompts", "references", "responses", "models", "selection")}
        patches = read_rows(args.citation_patch) if args.citation_patch else None
        if args.citation_patch:
            paths["citation_patch"] = args.citation_patch
        values = prepare(read_rows(args.prompts), read_rows(args.references),
                         read_rows(args.responses), json.loads(args.models.read_text("utf-8-sig")),
                         json.loads(args.selection.read_text("utf-8-sig")), args.run_id, args.variant, patches)
        result = write_bundle(args.out_dir, *values,
                              {name: digest(path.read_bytes()) for name, path in paths.items()})
        print(json.dumps({"packet_count": result["packet_count"], "network_calls": 0}))
    else:
        output = validate_results(read_rows(args.results), load_index(args.bundle))
        with args.output.open("x", encoding="utf-8") as handle:
            json.dump(output, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        print(json.dumps({"model_summaries": len(output)}))


if __name__ == "__main__":
    main()
