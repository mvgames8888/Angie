# Removing one Native Converter disables migrations for other converters

## Status and severity

**Novel candidate — Low severity.** The issue is reproducible against the
supplied source snapshot and was not found by searching the bundled prior-audit
reports. It is an availability failure triggered by an otherwise supported
administrative operation; recovery requires another administrator transaction.

## Root cause

`MigrationManager.configureNativeConverters` supports mapping multiple
`(network, NativeConverter)` entries to one `VaultBridgeToken`. The configuration
is keyed per converter, but the underlying ERC-20 allowance is keyed only by
`(MigrationManager, VaultBridgeToken)`.

When an administrator overrides or unsets one entry, the function unconditionally
sets the old vbToken's allowance to zero. It does not check whether another live
entry uses the same token pair. That other entry remains authorized in
`nativeConvertersConfiguration`, yet its migration fails when
`VaultBridgeToken.completeMigration` attempts to transfer the underlying asset
from `MigrationManager`.

## Reproduction

Run from the repository root. The PoC reads an extracted worktree when present
and otherwise reads `MigrationManager.sol` directly from
`vault-bridge-main.zip.txt`:

```console
$ python3 pocs/shared-migration-allowance/poc.py
PoC reproduced: removing converter A disabled still-authorized converter B
```

The PoC models the exact approval and configuration semantics and asserts that
the vulnerable statements still exist in the supplied Solidity source. It:

1. configures converters A and B on different networks for the same vbToken;
2. successfully completes a migration through B;
3. unsets only A, which clears their shared allowance;
4. proves B remains configured; and
5. proves B can no longer complete a migration because its allowance is zero.

No public network is contacted.

## Impact

A routine removal or rotation of one chain's Native Converter can unexpectedly
halt completion of backing migrations from every other configured chain using
the same vbToken. Cross-chain messages for those converters revert until an
administrator notices the shared allowance was revoked and restores it. The
funds are not stolen, and the administrator can recover by reconfiguring a live
entry, which limits severity.

## Prior-audit review

The bundled reports were searched for `configureNativeConverters`,
`forceApprove`, shared/revoked allowances, overrides, and unsetting tokens. The
reports describe the full allowance granted to each vbToken, but no prior
finding identifies the mismatch between per-converter configuration and the
shared ERC-20 allowance.

## Recommendation

Track the number of configurations using each `(underlyingToken, vbToken)` pair.
Grant approval when the count changes from zero to one and revoke it only when
the count reaches zero. When overriding an entry with the same pair, avoid
changing the allowance. Add a regression test with two converters sharing one
vbToken, then unset each converter independently and verify migrations through
the remaining converter still succeed.
