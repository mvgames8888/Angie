#!/usr/bin/env python3
"""Capture reproducible, read-only evidence for in-scope Solana Devnet programs."""

import argparse
import base64
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

from scripts.inventory_idls import EXPECTED_PROGRAMS


DEVNET_RPC = "https://api.devnet.solana.com"
DEVNET_GENESIS_HASH = "EtWTRABZaYq6iMfeYKouRu166VU2xqa1"
UPGRADEABLE_LOADER = "BPFLoaderUpgradeab1e11111111111111111111111"
MAX_ACCOUNT_BYTES = 20 * 1024 * 1024
BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def base58_encode(value: bytes) -> str:
    zeroes = len(value) - len(value.lstrip(b"\0"))
    number = int.from_bytes(value, "big")
    encoded = ""
    while number:
        number, remainder = divmod(number, 58)
        encoded = BASE58_ALPHABET[remainder] + encoded
    return "1" * zeroes + encoded


def rpc_call(url: str, method: str, params: list[Any], opener=urlopen) -> Any:
    payload = json.dumps(
        {"jsonrpc": "2.0", "id": method, "method": method, "params": params}
    ).encode()
    request = Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "pump-devnet-capture/1.0"},
        method="POST",
    )
    try:
        with opener(request, timeout=30) as response:
            result = json.load(response)
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"RPC {method} failed: {error}") from error
    if not isinstance(result, dict) or "error" in result or "result" not in result:
        raise ValueError(f"RPC {method} returned an error: {result!r}")
    return result["result"]


def decode_account(result: Any, address: str) -> tuple[dict[str, Any], bytes, int]:
    if not isinstance(result, dict) or not isinstance(result.get("context"), dict):
        raise ValueError(f"invalid getAccountInfo response for {address}")
    account = result.get("value")
    if not isinstance(account, dict):
        raise ValueError(f"account does not exist on Devnet: {address}")
    data = account.get("data")
    if not isinstance(data, list) or len(data) != 2 or data[1] != "base64":
        raise ValueError(f"unsupported account encoding for {address}")
    try:
        raw = base64.b64decode(data[0], validate=True)
    except (ValueError, TypeError) as error:
        raise ValueError(f"invalid account data for {address}") from error
    if len(raw) > MAX_ACCOUNT_BYTES:
        raise ValueError(f"account {address} exceeds {MAX_ACCOUNT_BYTES} bytes")
    return account, raw, int(result["context"]["slot"])


def programdata_address(program: bytes) -> str:
    if len(program) != 36 or int.from_bytes(program[:4], "little") != 2:
        raise ValueError("program account is not an UpgradeableLoader Program state")
    return base58_encode(program[4:36])


def programdata_metadata(programdata: bytes) -> dict[str, Any]:
    """Decode the bincode header of an UpgradeableLoader ProgramData account."""
    if len(programdata) < 13 or int.from_bytes(programdata[:4], "little") != 3:
        raise ValueError("account is not an UpgradeableLoader ProgramData state")
    deployment_slot = int.from_bytes(programdata[4:12], "little")
    option = programdata[12]
    if option == 0:
        upgrade_authority = None
        metadata_length = 13
    elif option == 1:
        if len(programdata) < 45:
            raise ValueError("ProgramData upgrade authority is truncated")
        upgrade_authority = base58_encode(programdata[13:45])
        metadata_length = 45
    else:
        raise ValueError(f"invalid ProgramData authority option: {option}")
    return {
        "deployment_slot": deployment_slot,
        "upgrade_authority": upgrade_authority,
        "metadata_length": metadata_length,
        "elf_length": len(programdata) - metadata_length,
    }


def capture(output: Path, rpc_url: str = DEVNET_RPC, opener=urlopen) -> dict[str, Any]:
    genesis_hash = rpc_call(rpc_url, "getGenesisHash", [], opener)
    if genesis_hash != DEVNET_GENESIS_HASH:
        raise ValueError(
            "RPC is not Solana Devnet: expected genesis hash "
            f"{DEVNET_GENESIS_HASH}, found {genesis_hash!r}"
        )
    start_slot = int(rpc_call(rpc_url, "getSlot", [{"commitment": "finalized"}], opener))
    manifest: dict[str, Any] = {
        "cluster": "devnet",
        "rpc_url": rpc_url,
        "genesis_hash": genesis_hash,
        "start_slot": start_slot,
        "programs": {},
    }
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output) as temporary:
        staging = Path(temporary)
        for filename, address in EXPECTED_PROGRAMS.items():
            result = rpc_call(
                rpc_url,
                "getAccountInfo",
                [address, {"encoding": "base64", "commitment": "finalized"}],
                opener,
            )
            account, program_bytes, slot = decode_account(result, address)
            if account.get("owner") != UPGRADEABLE_LOADER or account.get("executable") is not True:
                raise ValueError(f"{address} is not an executable upgradeable program")
            data_address = programdata_address(program_bytes)
            data_result = rpc_call(
                rpc_url,
                "getAccountInfo",
                [data_address, {"encoding": "base64", "commitment": "finalized"}],
                opener,
            )
            data_account, data_bytes, data_slot = decode_account(data_result, data_address)
            if data_account.get("owner") != UPGRADEABLE_LOADER:
                raise ValueError(f"ProgramData {data_address} has an unexpected owner")
            metadata = programdata_metadata(data_bytes)
            stem = filename.removesuffix(".json")
            (staging / f"{stem}.program.bin").write_bytes(program_bytes)
            (staging / f"{stem}.programdata.bin").write_bytes(data_bytes)
            manifest["programs"][stem] = {
                "address": address,
                "programdata_address": data_address,
                "program_slot": slot,
                "programdata_slot": data_slot,
                "program_sha256": hashlib.sha256(program_bytes).hexdigest(),
                "programdata_sha256": hashlib.sha256(data_bytes).hexdigest(),
                **metadata,
            }
        end_slot = int(rpc_call(rpc_url, "getSlot", [{"commitment": "finalized"}], opener))
        manifest["end_slot"] = end_slot
        (staging / "manifest.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        for path in staging.iterdir():
            path.replace(output / path.name)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("evidence/devnet"))
    parser.add_argument("--rpc-url", default=DEVNET_RPC)
    args = parser.parse_args()
    try:
        capture(args.output, args.rpc_url)
    except ValueError as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
