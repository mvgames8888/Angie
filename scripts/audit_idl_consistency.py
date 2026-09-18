#!/usr/bin/env python3
"""Check internal Anchor IDL references and suspicious PDA seed metadata."""

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.inventory_idls import flatten_accounts, load_and_validate


def root_account(path: Any) -> str | None:
    if not isinstance(path, str) or not path:
        return None
    return path.split(".", 1)[0]


def analyze_instruction(filename: str, instruction: dict[str, Any]) -> list[dict[str, Any]]:
    findings = []
    accounts = list(flatten_accounts(instruction.get("accounts", [])))
    names = {name.split(".", 1)[0] for name, _ in accounts}
    instruction_name = str(instruction.get("name", "<unnamed>"))
    for qualified_name, account in accounts:
        for relation in account.get("relations", []):
            if relation not in names:
                findings.append(
                    {
                        "kind": "missing_relation_target",
                        "idl": filename,
                        "instruction": instruction_name,
                        "account": qualified_name,
                        "target": relation,
                    }
                )
        pda = account.get("pda")
        if not isinstance(pda, dict):
            continue
        seeds = pda.get("seeds", [])
        values = seeds + ([pda["program"]] if "program" in pda else [])
        for value in values:
            if isinstance(value, dict) and value.get("kind") == "account":
                root = root_account(value.get("path"))
                if root not in names:
                    findings.append(
                        {
                            "kind": "missing_pda_path_root",
                            "idl": filename,
                            "instruction": instruction_name,
                            "account": qualified_name,
                            "path": value.get("path"),
                        }
                    )
        if (
            isinstance(seeds, list)
            and len(seeds) == 3
            and seeds[1] == seeds[2]
            and isinstance(seeds[1], dict)
            and seeds[1].get("kind") == "account"
        ):
            findings.append(
                {
                    "kind": "duplicate_ata_program_and_mint_seed",
                    "idl": filename,
                    "instruction": instruction_name,
                    "account": qualified_name,
                    "duplicated_path": seeds[1].get("path"),
                }
            )
    return findings


def analyze(directory: Path) -> dict[str, Any]:
    findings = []
    instruction_count = 0
    for filename, idl in load_and_validate(directory):
        for instruction in idl["instructions"]:
            instruction_count += 1
            findings.extend(analyze_instruction(filename, instruction))
    counts: dict[str, int] = {}
    for finding in findings:
        counts[finding["kind"]] = counts.get(finding["kind"], 0) + 1
    return {
        "idls_checked": 3,
        "instructions_checked": instruction_count,
        "finding_counts": counts,
        "findings": findings,
        "interpretation": "metadata consistency only; findings are not runtime vulnerabilities",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("idl_directory", nargs="?", type=Path, default=Path("idl"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.dumps(analyze(args.idl_directory), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
