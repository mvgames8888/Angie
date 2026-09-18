# IDL metadata consistency review

**Disposition: CLOSED / DO NOT SUBMIT as a security finding.**

## Result

The offline consistency check reviewed all 109 instructions and found no missing
relation targets and no PDA account paths whose root account is absent. It found
three suspicious associated-token PDA declarations, all in legacy
`pump::migrate`:

| Account | Declared ATA seeds |
| --- | --- |
| `associated_bonding_curve` | `bonding_curve`, `mint`, `mint` |
| `pool_authority_mint_account` | `pool_authority`, `mint`, `mint` |
| `pool_base_token_account` | `pool`, `mint`, `mint` |

An associated-token address normally uses owner, token-program ID, and mint.
The declarations repeat `mint` in both the token-program and mint positions,
whereas `migrate_v2` uses separate `base_token_program` and `base_mint` paths.

## Impact assessment

This is a reproducible **IDL metadata defect**, not a demonstrated smart-contract
vulnerability. A client that auto-resolves these accounts from the legacy IDL
may derive unusable addresses and fail to construct `migrate`. A caller can
still supply accounts explicitly, and the metadata does not prove that the
deployed handler accepts an incorrect vault or loses funds. Under the current
program gate, transaction-construction failure without financial impact is not
an eligible finding.

Do not submit this by itself. Retain it as a warning for any legacy migration
test: derive the canonical ATA with `(owner, Tokenkeg, mint)`, pass it explicitly,
and separately verify the handler's owner/mint checks on Devnet.

Run the deterministic check with:

```bash
python3 -m scripts.audit_idl_consistency
```
