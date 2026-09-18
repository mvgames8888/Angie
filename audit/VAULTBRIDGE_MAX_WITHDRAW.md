# VaultBridgeToken zero-liquidity view revert

## Status

The local model and source-shape verifier are implemented. Validation against
the actual contest source remains pending because neither
`vault-bridge-main.zip.txt` nor an extracted `vault-bridge-main/` tree is
present in this checkout. The PoC fails closed when that evidence is absent.

## Candidate finding

When the internal reserve cannot cover the owner's full balance and the yield
vault reports `maxWithdraw(address(this)) == 0`, `_simulateWithdraw` passes zero
as the denominator of `Math.mulDiv`. Consequently, `maxWithdraw(owner)` and
`maxRedeem(owner)` revert even though assets held in `reservedAssets` remain
directly withdrawable.

This is an availability and ERC-4626 integration issue, not a claim of lost or
permanently frozen funds.

## Reproduction

Place the supplied archive at the repository root, then run:

```bash
python3 pocs/max-withdraw-zero-liquidity/poc.py
```

The script verifies that the supplied Solidity source still contains the
suspected call and zero denominator path before executing the model. It refuses
to report success if the archive is missing, malformed, does not contain the
expected source, or already includes a zero-liquidity guard.

Expected output:

```text
PoC reproduced: maxWithdraw and maxRedeem reverted while 20 reserve assets were withdrawable
```

## Recommended remediation

Handle `maxWithdraw_ == 0` before `Math.mulDiv`: return the internal reserve in
the non-forcing simulation and use the existing `AssetsTooLarge` error in the
forcing path. Also handle a non-zero `maxWithdraw_` whose `previewWithdraw`
rounds to zero, and add contract-level regression tests for both view methods
and a reserve-only state-changing withdrawal.
