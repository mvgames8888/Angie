#!/usr/bin/env python3
"""Reproduce MigrationManager's shared-allowance revocation locally.

This is a semantic model of the relevant ERC-20 and contract operations.  The
source assertions keep the model tied to the supplied Solidity snapshot and
fail if the vulnerable operations are changed.
"""

from dataclasses import dataclass
from pathlib import Path
from zipfile import ZipFile


UINT256_MAX = 2**256 - 1
ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "vault-bridge-main/src/primary-chain/MigrationManager.sol"


def supplied_source() -> str:
    """Read MigrationManager from an extracted tree or the supplied archive."""
    if SOURCE.exists():
        return SOURCE.read_text(encoding="utf-8")

    archive = ROOT / "vault-bridge-main.zip.txt"
    archived_source = "vault-bridge-main/src/primary-chain/MigrationManager.sol"
    with ZipFile(archive) as source_archive:
        return source_archive.read(archived_source).decode()


class InsufficientAllowance(Exception):
    pass


@dataclass(frozen=True)
class TokenPair:
    vb_token: str
    underlying: str


class ERC20:
    def __init__(self) -> None:
        self.allowances: dict[tuple[str, str], int] = {}

    def approve(self, owner: str, spender: str, amount: int) -> None:
        self.allowances[owner, spender] = amount

    def transfer_from(self, owner: str, spender: str, amount: int) -> None:
        allowance = self.allowances.get((owner, spender), 0)
        if allowance < amount:
            raise InsufficientAllowance


class MigrationManager:
    address = "migration-manager"

    def __init__(self, underlying: ERC20) -> None:
        self.underlying = underlying
        self.configuration: dict[tuple[int, str], TokenPair] = {}

    def configure(self, network: int, converter: str, pair: TokenPair | None) -> None:
        key = network, converter
        old_pair = self.configuration.get(key)
        if pair is not None:
            if old_pair is not None:
                self.underlying.approve(self.address, old_pair.vb_token, 0)
            self.configuration[key] = pair
            self.underlying.approve(self.address, pair.vb_token, UINT256_MAX)
        else:
            assert old_pair is not None
            self.underlying.approve(self.address, old_pair.vb_token, 0)
            del self.configuration[key]

    def complete_migration(self, network: int, converter: str, assets: int) -> None:
        pair = self.configuration[network, converter]
        # VaultBridgeToken.completeMigration calls transferFrom on this allowance.
        self.underlying.transfer_from(self.address, pair.vb_token, assets)


def assert_supplied_source_is_vulnerable() -> None:
    source = supplied_source()
    assert "oldTokens.underlyingToken.forceApprove(address(oldTokens.vbToken), 0);" in source
    assert "underlyingToken.forceApprove(vbToken, type(uint256).max);" in source
    assert "vbToken.completeMigration(originNetwork, shares, assets);" in source


def main() -> None:
    assert_supplied_source_is_vulnerable()
    token = ERC20()
    manager = MigrationManager(token)
    shared_pair = TokenPair("vb-token", "underlying-token")

    # Two independent converters are intentionally mapped to the same vbToken.
    manager.configure(2, "converter-a", shared_pair)
    manager.configure(3, "converter-b", shared_pair)
    manager.complete_migration(3, "converter-b", 100)

    # Removing only A revokes the single ERC-20 allowance shared by A and B.
    manager.configure(2, "converter-a", None)
    assert manager.configuration[3, "converter-b"] == shared_pair
    assert token.allowances[manager.address, shared_pair.vb_token] == 0

    try:
        manager.complete_migration(3, "converter-b", 100)
    except InsufficientAllowance:
        print("PoC reproduced: removing converter A disabled still-authorized converter B")
    else:
        raise AssertionError("migration unexpectedly succeeded with zero allowance")


if __name__ == "__main__":
    main()
