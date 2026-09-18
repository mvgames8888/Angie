#!/usr/bin/env python3
"""Reproduce VaultBridgeToken view reverts at zero yield-vault liquidity."""

from pathlib import Path
from zipfile import BadZipFile, ZipFile


ROOT = Path(__file__).resolve().parents[2]
SOURCE = "vault-bridge-main/src/primary-chain/VaultBridgeToken.sol"


class EvidenceError(RuntimeError):
    """Raised when the supplied Solidity evidence cannot be verified."""


class DivisionByZero(Exception):
    """Model Solidity's Math.mulDiv zero-denominator revert."""


def supplied_source(root: Path = ROOT) -> str:
    extracted = root / SOURCE
    if extracted.is_file():
        return extracted.read_text(encoding="utf-8")

    archive_path = root / "vault-bridge-main.zip.txt"
    if not archive_path.is_file():
        raise EvidenceError(
            f"missing source evidence: provide {archive_path} or {root / SOURCE}"
        )
    try:
        with ZipFile(archive_path) as archive:
            return archive.read(SOURCE).decode("utf-8")
    except (BadZipFile, KeyError, UnicodeDecodeError) as error:
        raise EvidenceError(f"cannot read {SOURCE} from {archive_path}: {error}") from error


def vulnerable_function(source: str) -> str:
    marker = "function _simulateWithdraw"
    if marker not in source:
        raise EvidenceError(f"source does not contain {marker}")
    function = source.split(marker, 1)[1].split("function withdraw", 1)[0]
    required_fragments = (
        "$.yieldVault.maxWithdraw(address(this))",
        "burnedYieldVaultShares, maxWithdraw_",
        "return $.reservedAssets;",
    )
    missing = [fragment for fragment in required_fragments if fragment not in function]
    if missing:
        raise EvidenceError(f"source does not match vulnerable path; missing {missing!r}")
    if "if (maxWithdraw_ == 0)" in function:
        raise EvidenceError("source already contains a zero-liquidity guard")
    return function


def mul_div(x: int, y: int, denominator: int) -> int:
    if denominator == 0:
        raise DivisionByZero
    return x * y // denominator


class VaultModel:
    def __init__(
        self, supply: int, owner_shares: int, reserve: int, max_vault_withdraw: int
    ) -> None:
        self.supply = supply
        self.owner_shares = owner_shares
        self.reserve = reserve
        self.max_vault_withdraw = max_vault_withdraw

    def max_withdraw(self) -> int:
        assets = self.owner_shares
        if self.reserve >= assets:
            return assets

        remaining_assets = assets - self.reserve
        max_withdraw = min(remaining_assets, self.max_vault_withdraw)
        burned_shares = 0  # ERC-4626 previewWithdraw(0)
        mul_div(self.supply - self.reserve, burned_shares, max_withdraw)
        return self.reserve + max_withdraw

    def max_redeem(self) -> int:
        return self.max_withdraw()

    def withdraw_from_reserve(self, assets: int) -> None:
        if not 0 < assets <= min(self.reserve, self.owner_shares):
            raise ValueError("withdrawal exceeds available reserve or owner balance")
        self.reserve -= assets
        self.owner_shares -= assets
        self.supply -= assets


def reproduce(root: Path = ROOT) -> None:
    vulnerable_function(supplied_source(root))
    vault = VaultModel(100, 100, 20, 0)

    for name, view in (("maxWithdraw", vault.max_withdraw), ("maxRedeem", vault.max_redeem)):
        try:
            view()
        except DivisionByZero:
            continue
        raise AssertionError(f"{name} unexpectedly returned instead of dividing by zero")

    vault.withdraw_from_reserve(20)
    assert (vault.owner_shares, vault.reserve, vault.supply) == (80, 0, 80)


def main() -> int:
    try:
        reproduce()
    except EvidenceError as error:
        print(f"Evidence error: {error}")
        return 2
    print(
        "PoC reproduced: maxWithdraw and maxRedeem reverted while "
        "20 reserve assets were withdrawable"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
