# Investigation status

## Current conclusion

No vulnerability is confirmed. Do **not** submit the inventory tooling or the
items below as a finding. A report requires a reproducible Devnet transaction
and measurable unauthorized state or balance change.

## Evidence acquisition

The audit requires these exact public inputs:

- `pump.json` for `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`
- `pump_fees.json` for `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ`
- `pump_amm.json` for `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA`
- the executable account data for each program from Solana Devnet
- the current upgrade-authority/program-data metadata

The repository tool records SHA-256 hashes for the IDLs. Binary account data,
RPC slot, cluster genesis hash, program-data address, and executable-data hash
must also be recorded before testing so results remain reproducible if a
deployment is upgraded.

## Candidate acceptance gate

A candidate moves into a private Cantina draft only when all are true:

1. The affected address and transaction use Devnet.
2. All wallets, tokens, and accounts used by the researcher are controlled by
   the researcher.
3. A clean pre-state and post-state demonstrate an unauthorized change or
   financial invariant violation.
4. A negative control shows that the expected safe variant does not cause the
   same result.
5. The result is repeatable from an Anchor test or documented Solana CLI
   commands.
6. Impact does not rely on denial of service, social engineering, real user
   data, or production exploitation.

## Review queue after acquisition

1. Confirm every external program and sysvar account is constrained to its
   intended address at runtime, not merely named as such in the IDL.
2. Confirm mint, vault, pool, bonding-curve, creator, and fee-recipient accounts
   are related by explicit constraints rather than independently attacker
   selectable.
3. Recompute buy/sell and deposit/withdraw outcomes across boundary values and
   compare on-chain deltas with slippage limits and reserve invariants.
4. Exercise initialization, migration, completion, fee collection, authority
   update, and account-close transitions twice to detect replay or stale-state
   paths.
5. Test Token Program versus Token-2022 substitutions only where the IDL allows
   a caller-supplied token program.

## Environment limitation observed

This execution environment currently rejects outbound HTTPS requests to both
GitHub and Solana Devnet with `403 Forbidden` at the CONNECT proxy. Therefore,
no claim about the current IDLs or deployed bytecode has been made from this
environment. Copying the three JSON files and Devnet account dumps into the
workspace is sufficient to resume static and offline binary analysis without
that network path.
