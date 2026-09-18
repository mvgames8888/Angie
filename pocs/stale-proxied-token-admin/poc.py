#!/usr/bin/env python3
"""Executable model of the stale wrapped-token proxy-admin exploit."""

from dataclasses import dataclass
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[2]
BRIDGE = ROOT / "agglayer-contracts-main/contracts/AgglayerBridge.sol"
PROXY = ROOT / "agglayer-contracts-main/contracts/lib/TokenWrappedTransparentProxy.sol"


def source_text(path: Path) -> str:
    if path.exists():
        return path.read_text()
    archive = ROOT / "agglayer-contracts-main.zip"
    archived_path = "agglayer-contracts-main/" + path.relative_to(ROOT / "agglayer-contracts-main").as_posix()
    with ZipFile(archive) as source_archive:
        return source_archive.read(archived_path).decode()


@dataclass
class WrappedTokenProxy:
    admin: str
    implementation: str = "honest"
    attacker_balance: int = 0

    def upgrade_to(self, caller: str, implementation: str) -> None:
        assert caller == self.admin, "only the EIP-1967 proxy admin may upgrade"
        self.implementation = implementation

    def attacker_mint(self, amount: int) -> None:
        assert self.implementation == "malicious"
        self.attacker_balance += amount


@dataclass
class Bridge:
    proxied_tokens_manager: str
    pending_proxied_tokens_manager: str | None = None
    canonical_reserves: int = 1_000_000

    def deploy_wrapped_token(self) -> WrappedTokenProxy:
        # Mirrors TokenWrappedTransparentProxy.constructor(): the admin is copied
        # into the proxy's own EIP-1967 slot at deployment time.
        return WrappedTokenProxy(admin=self.proxied_tokens_manager)

    def transfer_manager(self, caller: str, replacement: str) -> None:
        assert caller == self.proxied_tokens_manager
        self.pending_proxied_tokens_manager = replacement

    def accept_manager(self, caller: str) -> None:
        assert caller == self.pending_proxied_tokens_manager
        self.proxied_tokens_manager = caller
        self.pending_proxied_tokens_manager = None

    def bridge_forged_wrapped_tokens(self, token: WrappedTokenProxy, amount: int) -> None:
        assert token.attacker_balance >= amount
        token.attacker_balance -= amount
        assert self.canonical_reserves >= amount
        self.canonical_reserves -= amount


def assert_model_matches_source() -> None:
    proxy_source = source_text(PROXY)
    bridge_source = source_text(BRIDGE)
    assert "_changeAdmin(IAgglayerBridge(msg.sender).getProxiedTokensManager())" in proxy_source
    assert "proxiedTokensManager = pendingProxiedTokensManager;" in bridge_source
    accept_body = bridge_source.split("function acceptProxiedTokensManagerRole", 1)[1].split("}", 1)[0]
    assert "changeAdmin" not in accept_body


def exploit() -> None:
    assert_model_matches_source()
    old_manager = "compromised-old-manager"
    new_manager = "replacement-manager"
    bridge = Bridge(proxied_tokens_manager=old_manager)
    wrapped_token = bridge.deploy_wrapped_token()

    bridge.transfer_manager(old_manager, new_manager)
    bridge.accept_manager(new_manager)
    assert bridge.proxied_tokens_manager == new_manager

    # The advertised role transfer did not touch the already-deployed proxy.
    assert wrapped_token.admin == old_manager
    wrapped_token.upgrade_to(old_manager, "malicious")

    # A malicious token implementation can mint arbitrary wrapped assets. The
    # bridge burns them normally and releases canonical liquidity remotely.
    stolen = bridge.canonical_reserves
    wrapped_token.attacker_mint(stolen)
    bridge.bridge_forged_wrapped_tokens(wrapped_token, stolen)
    assert bridge.canonical_reserves == 0
    print(f"exploit reproduced: stale admin drained {stolen} reserve units")


if __name__ == "__main__":
    exploit()
