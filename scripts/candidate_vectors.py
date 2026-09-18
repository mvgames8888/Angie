#!/usr/bin/env python3
"""Generate exact IDL account-order vectors for controlled Devnet candidate tests."""

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from scripts.inventory_idls import EXPECTED_PROGRAMS, load_and_validate


CANDIDATES = {
    "C-01": {
        "idl": "pump_amm.json",
        "instruction": "claim_cashback",
        "mutations": ["user_wsol_token_account"],
        "control": "destination is a non-associated quote-mint token account owned by user A",
        "attack": "replace only the destination with a quote-mint token account owned by user B",
    },
    "C-02-pump-native": {
        "idl": "pump.json",
        "instruction": "collect_creator_fee",
        "mutations": ["creator"],
        "control": "creator is the wallet used to derive creator_vault",
        "attack": "replace creator while keeping the funded creator_vault constant",
    },
    "C-02-pump-token": {
        "idl": "pump.json",
        "instruction": "collect_creator_fee_v2",
        "mutations": ["creator", "creator_token_account"],
        "control": "creator and destination token account have the intended owner relationship",
        "attack": "substitute an unrelated creator/destination pair",
    },
    "C-02-amm-token": {
        "idl": "pump_amm.json",
        "instruction": "collect_coin_creator_fee",
        "mutations": ["coin_creator", "coin_creator_token_account"],
        "control": "coin creator and destination token account match",
        "attack": "substitute an unrelated creator/destination pair",
    },
    "C-04": {
        "idl": "pump_fees.json",
        "instruction": "crank_donation_fee_pda",
        "mutations": ["mint_whitelist", "epoch_tracker", "debouncer", "debouncer_ata"],
        "control": "all relay accounts belong to researcher-controlled configuration A",
        "attack": "replace one relay account at a time, then all four, with configuration B",
    },
}


def instruction_by_name(idl: dict[str, Any], name: str) -> dict[str, Any]:
    matches = [item for item in idl.get("instructions", []) if item.get("name") == name]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one instruction named {name!r}, found {len(matches)}")
    return matches[0]


def generate_vectors(directory: Path) -> dict[str, Any]:
    loaded = dict(load_and_validate(directory))
    vectors: dict[str, Any] = {
        "cluster": "devnet",
        "transaction_policy": "researcher-controlled accounts and funds only",
        "idls": {},
        "candidates": {},
    }
    for filename in EXPECTED_PROGRAMS:
        vectors["idls"][filename] = {
            "program_address": EXPECTED_PROGRAMS[filename],
            "sha256": hashlib.sha256((directory / filename).read_bytes()).hexdigest(),
        }

    for candidate, specification in CANDIDATES.items():
        filename = specification["idl"]
        instruction = instruction_by_name(loaded[filename], specification["instruction"])
        accounts = instruction.get("accounts")
        discriminator = instruction.get("discriminator")
        if not isinstance(accounts, list) or not all(
            isinstance(account, dict) and isinstance(account.get("name"), str)
            for account in accounts
        ):
            raise ValueError(f"{filename}:{instruction.get('name')}: invalid accounts")
        if not isinstance(discriminator, list) or len(discriminator) != 8 or not all(
            isinstance(value, int) and 0 <= value <= 255 for value in discriminator
        ):
            raise ValueError(f"{filename}:{instruction.get('name')}: invalid discriminator")
        names = [account["name"] for account in accounts]
        missing = [name for name in specification["mutations"] if name not in names]
        if missing:
            raise ValueError(f"{candidate}: mutation accounts absent from IDL: {missing}")
        vectors["candidates"][candidate] = {
            "program_address": EXPECTED_PROGRAMS[filename],
            "idl": filename,
            "idl_instruction": instruction["name"],
            "discriminator": discriminator,
            "accounts": [
                {
                    "index": index,
                    "name": account["name"],
                    "writable": account.get("writable") is True,
                    "signer": account.get("signer") is True,
                }
                for index, account in enumerate(accounts)
            ],
            "mutation_indices": {name: names.index(name) for name in specification["mutations"]},
            "negative_control": specification["control"],
            "candidate_attempt": specification["attack"],
            "required_assertion": "failed attempts are atomic; successful attempts record all balance and state deltas",
        }
    return vectors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("idl_directory", nargs="?", type=Path, default=Path("idl"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.dumps(generate_vectors(args.idl_directory), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
