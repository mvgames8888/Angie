#!/usr/bin/env python3
"""Validate in-scope Anchor IDLs and render a review-oriented inventory."""

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any, Iterable
from urllib.request import Request, urlopen


EXPECTED_PROGRAMS = {
    "pump.json": "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P",
    "pump_fees.json": "pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ",
    "pump_amm.json": "pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA",
}

IDL_BASE_URL = "https://raw.githubusercontent.com/pump-fun/pump-public-docs/main/idl"
MAX_IDL_BYTES = 5 * 1024 * 1024


def program_address(idl: dict[str, Any]) -> str | None:
    """Return an address from either modern or legacy Anchor IDL metadata."""
    address = idl.get("address")
    if isinstance(address, str):
        return address
    metadata = idl.get("metadata", {})
    if isinstance(metadata, dict) and isinstance(metadata.get("address"), str):
        return metadata["address"]
    return None


def flatten_accounts(accounts: Iterable[dict[str, Any]], prefix: str = ""):
    """Yield nested instruction accounts as (qualified name, account) pairs."""
    for account in accounts:
        name = str(account.get("name", "<unnamed>"))
        qualified = f"{prefix}.{name}" if prefix else name
        nested = account.get("accounts")
        if isinstance(nested, list):
            yield from flatten_accounts(nested, qualified)
        else:
            yield qualified, account


def flag(value: Any) -> bool:
    return value is True


def account_traits(account: dict[str, Any]) -> list[str]:
    traits = []
    if flag(account.get("writable")) or flag(account.get("isMut")):
        traits.append("writable")
    if flag(account.get("signer")) or flag(account.get("isSigner")):
        traits.append("signer")
    if flag(account.get("optional")) or flag(account.get("isOptional")):
        traits.append("optional")
    if "pda" in account:
        traits.append("PDA")
    address = account.get("address")
    if isinstance(address, str):
        traits.append(f"fixed `{address}`")
    return traits or ["read-only"]


def compact_json(value: Any) -> str:
    """Render Anchor type/seed metadata deterministically on one line."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def argument_summary(arguments: Any) -> list[str]:
    if not isinstance(arguments, list):
        return ["_invalid argument metadata_ (`args` is not an array)"]
    summaries = []
    for index, argument in enumerate(arguments):
        if not isinstance(argument, dict):
            summaries.append(f"argument_{index}: `{compact_json(argument)}`")
            continue
        name = str(argument.get("name", f"argument_{index}"))
        summaries.append(f"`{name}`: `{compact_json(argument.get('type'))}`")
    return summaries


def pda_summary(account: dict[str, Any]) -> str | None:
    pda = account.get("pda")
    if not isinstance(pda, dict):
        return None
    seeds = pda.get("seeds", [])
    program = pda.get("program")
    details = f"seeds={compact_json(seeds)}"
    if program is not None:
        details += f", program={compact_json(program)}"
    return details


def documentation_summary(value: Any) -> str | None:
    """Join Anchor documentation lines without silently accepting bad metadata."""
    if value is None:
        return None
    if not isinstance(value, list) or not all(isinstance(line, str) for line in value):
        return f"_invalid documentation metadata_: `{compact_json(value)}`"
    return " ".join(line.strip() for line in value if line.strip()) or None


def relations_summary(account: dict[str, Any]) -> str | None:
    """Render Anchor account relations, including malformed metadata for review."""
    relations = account.get("relations")
    if relations is None:
        return None
    if not isinstance(relations, list) or not all(
        isinstance(relation, str) for relation in relations
    ):
        return f"_invalid relation metadata_: `{compact_json(relations)}`"
    return ", ".join(f"`{relation}`" for relation in relations) or "_empty_"


def review_indicators(accounts: list[tuple[str, dict[str, Any]]]) -> list[str]:
    """Return conservative prompts for properties that need manual validation."""
    indicators = []
    signers = [name for name, account in accounts if "signer" in account_traits(account)]
    if not signers:
        indicators.append("No signer is visible in the IDL")

    for name, account in accounts:
        traits = account_traits(account)
        normalized = name.rsplit(".", 1)[-1].replace("_", "").lower()
        if "optional" in traits and "signer" in traits:
            indicators.append(f"Optional signer `{name}`")
        if normalized.endswith("program") and not any(
            trait.startswith("fixed `") for trait in traits
        ):
            indicators.append(f"Program-like account `{name}` has no fixed address in the IDL")
    return indicators


def render_idl(filename: str, idl: dict[str, Any]) -> tuple[str, int]:
    instructions = idl.get("instructions")
    if not isinstance(instructions, list):
        raise ValueError(f"{filename}: 'instructions' must be an array")

    lines = [f"## `{filename}`", ""]
    indicator_count = 0
    for instruction in instructions:
        name = str(instruction.get("name", "<unnamed>"))
        accounts = list(flatten_accounts(instruction.get("accounts", [])))
        args = argument_summary(instruction.get("args", []))
        docs = documentation_summary(instruction.get("docs"))
        signers = [n for n, a in accounts if "signer" in account_traits(a)]
        indicators = review_indicators(accounts)
        indicator_count += len(indicators)
        lines.extend((f"### `{name}`", "", f"- Arguments: **{len(args)}**"))
        if docs:
            lines.append(f"- Documentation: {docs}")
        if args:
            lines.extend(f"  - {argument}" for argument in args)
        lines.append(f"- Visible signers: {', '.join(f'`{s}`' for s in signers) or '**none**'}")
        lines.append("- Review indicators:")
        if indicators:
            lines.extend(f"  - {indicator}" for indicator in indicators)
        else:
            lines.append("  - _none from IDL metadata_")
        lines.append("- Accounts:")
        if not accounts:
            lines.append("  - _none declared_")
        for account_name, account in accounts:
            lines.append(f"  - `{account_name}` — {', '.join(account_traits(account))}")
            pda = pda_summary(account)
            if pda:
                lines.append(f"    - PDA: `{pda}`")
            relations = relations_summary(account)
            if relations:
                lines.append(f"    - Relations: {relations}")
            account_docs = documentation_summary(account.get("docs"))
            if account_docs:
                lines.append(f"    - Documentation: {account_docs}")
        lines.append("")
    return "\n".join(lines), indicator_count


def load_and_validate(directory: Path) -> list[tuple[str, dict[str, Any]]]:
    loaded = []
    for filename, expected in EXPECTED_PROGRAMS.items():
        path = directory / filename
        if not path.is_file():
            raise ValueError(f"missing required IDL: {path}")
        try:
            idl = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError(f"cannot parse {path}: {error}") from error
        if not isinstance(idl, dict):
            raise ValueError(f"{path}: root must be an object")
        actual = program_address(idl)
        if actual != expected:
            raise ValueError(
                f"{path}: expected program address {expected}, found {actual!r}"
            )
        loaded.append((filename, idl))
    return loaded


def download_idls(directory: Path, opener=urlopen) -> None:
    """Download and validate the public IDLs before atomically installing them."""
    directory.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=directory) as temporary:
        staging = Path(temporary)
        for filename in EXPECTED_PROGRAMS:
            request = Request(
                f"{IDL_BASE_URL}/{filename}",
                headers={"User-Agent": "pump-devnet-idl-inventory/1.0"},
            )
            try:
                with opener(request, timeout=30) as response:
                    payload = response.read(MAX_IDL_BYTES + 1)
            except OSError as error:
                raise ValueError(f"could not download {filename}: {error}") from error
            if len(payload) > MAX_IDL_BYTES:
                raise ValueError(f"downloaded {filename} exceeds {MAX_IDL_BYTES} bytes")
            (staging / filename).write_bytes(payload)

        # Validate the complete set before replacing any existing local IDL.
        load_and_validate(staging)
        for filename in EXPECTED_PROGRAMS:
            (staging / filename).replace(directory / filename)


def inventory(directory: Path) -> str:
    sections = [
        "# Anchor IDL attack-surface inventory",
        "",
        "> Generated metadata for manual security review. Indicators below are not findings.",
        "",
    ]
    rendered = []
    provenance = []
    indicator_count = 0
    instruction_count = 0
    for filename, idl in load_and_validate(directory):
        digest = hashlib.sha256((directory / filename).read_bytes()).hexdigest()
        provenance.append(f"- `{filename}` — SHA-256 `{digest}`")
        section, count = render_idl(filename, idl)
        rendered.append(section)
        indicator_count += count
        instruction_count += len(idl["instructions"])
    sections.extend(
        (
            "## Summary",
            "",
            f"- Instructions inventoried: **{instruction_count}**",
            f"- Manual-review indicators: **{indicator_count}**",
            "",
            "### Input provenance",
            "",
            *provenance,
            "",
        )
    )
    sections.extend(rendered)
    return "\n".join(sections).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("idl_directory", nargs="?", type=Path, default=Path("idl"))
    parser.add_argument(
        "--download",
        action="store_true",
        help="download the three public IDLs from pump-fun/pump-public-docs first",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        if args.download:
            download_idls(args.idl_directory)
        report = inventory(args.idl_directory)
    except ValueError as error:
        parser.error(str(error))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
