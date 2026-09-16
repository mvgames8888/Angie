# Rotating `proxiedTokensManager` leaves the previous manager in control of existing wrapped tokens

> **Submission status: READY**, subject only to confirming that the live Cantina
> program still includes the supplied sovereign bridge contracts. The PoC now
> executes the real `TokenWrappedTransparentProxy` runtime bytecode embedded in
> the supplied `BridgeLib.sol` and proves that the former manager can update the
> EIP-1967 implementation slot after the bridge-level role rotation.

## Severity

**High** — a compromised manager that has ostensibly been replaced can upgrade any previously deployed wrapped-token proxy, mint arbitrary wrapped assets, and bridge them out to drain canonical liquidity.

## Root cause

`TokenWrappedTransparentProxy` copies the bridge's current `proxiedTokensManager` into its own EIP-1967 admin slot during construction. The proxy admin is independent storage after deployment.

The bridge's two-step `transferProxiedTokensManagerRole` / `acceptProxiedTokensManagerRole` flow only changes `proxiedTokensManager` in bridge storage. It neither changes the admins of existing token proxies nor records them for later migration. Consequently, the old manager permanently retains upgrade authority over every proxy deployed during its tenure.

## Exploit

1. A wrapped token proxy is deployed while manager A is active; A becomes its proxy admin.
2. Governance rotates the bridge role from A to manager B, for example because A is suspected to be compromised.
3. The bridge reports B as `proxiedTokensManager`, but the existing token proxy still reports A as admin.
4. A upgrades that token to a malicious implementation and mints an arbitrary balance.
5. The attacker bridges the forged wrapped tokens. The bridge treats them as authentic wrapped assets, burns them, and creates valid exits that release canonical assets on the origin network.

The EVM PoC extracts and executes the exact proxy runtime bytecode embedded in the supplied `BridgeLib.sol`. It initializes the real EIP-1967 admin and implementation slots, performs the bridge-level manager rotation independently, calls `upgradeTo(address)` as the former manager, and proves that the actual runtime writes the malicious implementation to the implementation slot:

```bash
python3 pocs/stale-proxied-token-admin/evm_poc.py
```

Expected output:

```text
EVM PoC reproduced: former manager upgraded the real supplied proxy runtime bytecode
```

The companion impact model anchors itself to the supplied Solidity sources and demonstrates how arbitrary wrapped-token minting drains all canonical reserves:

```bash
python3 pocs/stale-proxied-token-admin/poc.py
```

## Impact

Role rotation does not revoke the former manager's most security-sensitive capability. Compromise of any historical manager can therefore become a permanent bridge-liquidity theft vector. Monitoring the bridge's role-transfer events would misleadingly indicate that access was revoked.

## Recommendation

Manage all wrapped-token proxies through one dedicated `ProxyAdmin` whose ownership can be rotated atomically, or maintain an enumerable proxy registry and migrate every EIP-1967 admin before completing the bridge-level role transfer. The acceptance step should revert unless all existing proxies are controlled by the pending manager. An emergency rotation procedure should explicitly cover existing proxy admin slots.

## Duplicate review

The bundled prior-audit index was searched for `proxiedTokensManager`, proxy-admin rotation, `changeAdmin`, stale administrators, and wrapped-token admin transfer. The reports discuss the manager and general proxy trust, but do not identify that the two-step bridge role rotation leaves historical managers in control of existing token proxies.

## Validation notes

1. Both PoCs run entirely locally and can read the contracts directly from `agglayer-contracts-main.zip`; they do not require an extracted worktree, RPC, compiler, or third-party package.
2. The former manager is not treated as a currently trusted administrator: the exploit occurs only after the contract's explicit two-step role-transfer process reports that a replacement manager has accepted the role.
3. Project documentation calls this address the wrapped-token proxy manager and describes these functions as transferring that role. It does not document that every historical manager remains trusted indefinitely.
4. The live Cantina page could not be fetched in the audit environment. The supplied contract is therefore treated as in scope because it is included in the user-provided Agglayer archive; confirm the live asset list immediately before submission.
