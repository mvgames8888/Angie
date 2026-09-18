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

## Static review status

The three required IDLs are now present and their program addresses have been
validated. The reproducible inventory is in `audit/attack-surface.md`, and the
triaged static review is in `audit/STATIC_ANALYSIS.md`. The review did not
confirm a vulnerability; its prioritized hypotheses still require controlled
Devnet validation.

The highest-priority hypotheses and their explicit confirmation/rejection gates
are tracked in `audit/CANDIDATES.md`. The leading check is AMM cashback recipient
ownership because the destination is not declaratively constrained and the AMM
IDL lacks the recipient-specific error exposed by the Pump IDL. This remains an
unconfirmed asymmetry, not a finding.

`audit/candidate-vectors.json` pins the reviewed IDL hashes, instruction
discriminators, exact account order, and mutation indices for the four P1
experiments. It is a handoff artifact for an external Devnet runner, not a
transaction or proof of impact.

The IDL consistency pass found three duplicated `mint` seed entries in legacy
`pump::migrate` associated-token PDA metadata. `audit/IDL_INTEGRITY.md` records
them as client-metadata defects. This item is closed and must not be submitted
because no unauthorized runtime effect has been shown. The reward-oriented
decision and go/no-go gate are in `audit/ELIGIBILITY.md`.

The documented `buy_exact_sol_in` reverse quote also has reproducible
under-delivery counterexamples when protocol and creator fees round separately.
`audit/MATH_REVIEW.md` records the bounded result and explains why an atomic
slippage failure is not, by itself, an eligible security finding. It is archived
behind the value-moving candidates under the gate in `audit/SCOPE.md`.

No executable or ProgramData account dumps are present yet. Claims about the
deployed bytecode, upgrade authority, runtime constraints, or handler arithmetic
remain out of scope until those artifacts are captured and hashed.
