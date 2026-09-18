# Static IDL review

## Scope and evidence

This review uses only the three IDLs present in `idl/`; it does not claim to
describe the deployed Devnet bytecode. The generated, instruction-by-instruction
inventory is in [`attack-surface.md`](attack-surface.md). Its input hashes are:

| IDL | Program | SHA-256 | Instructions |
| --- | --- | --- | ---: |
| `pump.json` | `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P` | `d9ba3eb509ccf315baa9ac655a3bcf45506a6c477af2b16f3f5ba93a135aec29` | 47 |
| `pump_fees.json` | `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ` | `510536a37bf40222fe6c307edd81df1a3c34a8009ca7479a4033aee478feddc5` | 30 |
| `pump_amm.json` | `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA` | `a169522f756aacd6e03d32dd1ee63321a6196442e9d7e0edc9a77d1a9e30f4dc` | 32 |

The inventory covers 109 instructions and emits 136 conservative review
indicators (59 Pump, 28 Fees, and 49 AMM). An indicator means that a property
cannot be established from IDL metadata; it is not a vulnerability.

## Result

**No confirmed vulnerability was identified from the IDLs alone.** Anchor IDLs
describe the client interface and some declarative account constraints, but do
not expose handler logic, all custom constraints, arithmetic, CPI construction,
or state transitions. Consequently none of the hypotheses below passes the
candidate acceptance gate in [`STATUS.md`](STATUS.md).

## Static observations and prioritized validation

### P1 — caller-supplied token programs

Trading and fee paths expose `token_program`, `base_token_program`, or
`quote_token_program` without a fixed address in several instructions. Examples
include Pump `buy_v2`, `sell_v2`, and `migrate_v2`; AMM `buy`, `sell`, and
`buy_exact_quote_in`; and Fees `claim_social_fee_pda_v2`, `sweep_buyback`, and
`update_fee_shares_v2`.

This is not automatically unsafe: Anchor interface accounts or handler checks
may restrict the executable owner/program ID, and accepting both SPL Token and
Token-2022 may be intentional. The PDA metadata often incorporates both the
selected token program and mint into associated-token addresses, which reduces
simple account-substitution opportunities.

Devnet validation should attempt the supported Token/Token-2022 combinations
and a controlled invalid executable. Verify rejection before value movement,
then compare token balances and program state. Give special attention to mint
extensions (transfer hooks, transfer fees, permanent delegates, and withheld
fees) and to paths where reserve arithmetic could assume that requested and
received token amounts are equal.

### P1 — AMM pool and vault relationships

AMM trade, deposit, and withdrawal instructions present `pool` and token
accounts as writable non-PDA accounts. The IDL does declare relations from
`base_mint`, `quote_mint`, `pool_base_token_account`, and
`pool_quote_token_account` to `pool`; deposit/withdraw also relate `lp_mint` to
the pool. These declarations are encouraging, but the IDL cannot prove the
implementation enforces token-account mint/authority fields or computes deltas
after Token-2022 behavior.

Devnet tests should swap one account at a time (vault, mint, LP mint, user token
account, and pool), require failure, and assert unchanged balances. Boundary
tests should cover zero, one base unit, maximum accepted values, skewed
reserves, and each slippage boundary. Check constant-product/reserve and LP
supply invariants using actual pre/post token balances rather than events.

### P1 — permissionless claim and migration flows

The following instructions expose no signer in the IDL:

| Program | Instructions |
| --- | --- |
| Pump | `claim_cashback`, `claim_cashback_v2`, `collect_creator_fee`, `collect_creator_fee_v2`, `distribute_creator_fees`, `get_minimum_distributable_fee`, `migrate_bonding_curve_creator`, `set_metaplex_creator`, `sync_user_volume_accumulator` |
| AMM | `claim_cashback`, `collect_coin_creator_fee`, `migrate_pool_coin_creator`, `set_coin_creator`, `sync_user_volume_accumulator`, `transfer_creator_fees_to_pump` |
| Fees | `get_fees`, `get_fees_with_quote_mint`, `revoke_fee_sharing_authority`, `transfer_fee_sharing_authority` |

Most appear designed for permissionless crank, deterministic recipient, view,
or migration behavior. For example, claim/collection destinations are paired
with user/creator-derived accumulator or vault PDAs. However, authorization and
destination equality must be established from deployed behavior. The two Fees
authority instructions expose no accounts or arguments at all in the IDL; they
may be deprecated/no-op interface entries, but bytecode or a controlled call is
required to determine their behavior.

For each state-changing path, call it as an unrelated wallet, substitute its
recipient and state accounts independently, and repeat it. Accept a candidate
only if funds or authority can be redirected, accounting can be advanced for
the wrong principal, or the second call violates an invariant.

### P1 — cross-program migration and fee sharing

The IDLs encode fixed IDs for the Pump, AMM, and Fees programs in several modern
cross-program paths and derive cross-program PDAs from fixed program IDs. Pump
`migrate_v2` fixes the AMM program; Fees `update_fee_shares_v2` fixes Pump and
AMM; and current trading paths fix the Fees program. This provides useful
domain separation at the client schema level.

Still validate that every CPI target and event authority is checked at runtime,
especially older variants whose generic `program` account is not fixed in the
IDL. Test mismatched mint/pool/sharing-config combinations and ensure migrations
are one-way and cannot be replayed after completion.

### P2 — administrative state transitions

Initialization, authority update, configuration, disable/toggle, and buyback
instructions generally expose a signer plus a global/config/vault relation or
PDA. The handler bodies remain unavailable, so the following properties are
unresolved:

1. initialization cannot replace or reinitialize an existing config;
2. the signer equals the authority stored in the relevant state account;
3. authority transfer cannot set an unusable or unintended key;
4. basis-point totals, fee tiers, and rate limits have safe bounds;
5. repeated disable/toggle/update calls preserve state invariants; and
6. buyback destinations, indices, and vault authorities are constrained.

Use two controlled administrators and one unrelated wallet on Devnet. Exercise
each transition twice and test old/new authority behavior before and after the
transition.

### P2 — arithmetic and serialization boundaries

Amounts, reserves, fees, and slippage parameters are primarily `u64`, while fee
configuration includes vectors and defined structs. The IDL supplies types but
not formulas, intermediate widths, rounding direction, vector bounds, or
post-transfer reconciliation. Static arithmetic safety therefore cannot be
concluded.

Construct a reference model for buy/sell and deposit/withdraw calculations and
compare it with Devnet at zero/one-unit boundaries, values around fee rounding,
near-empty reserves, and the largest values accepted by transaction/account
limits. Any discrepancy must be demonstrated as extractable value or an
unauthorized state change rather than denial of service.

## Ruled out at the IDL layer

- The three top-level program addresses match the expected in-scope addresses.
- The IDLs contain no optional signer accounts.
- System Program and Associated Token Program accounts are consistently fixed
  where named; modern cross-program paths also fix the in-scope CPI programs.
- No finding should be filed solely because a generic Anchor event `program`
  account lacks a fixed ID in an older instruction. Its runtime constraint and
  actual CPI target need bytecode or Devnet validation.

## Remaining evidence required

Before reporting any candidate, capture the deployed program and ProgramData
accounts with `scripts/capture_devnet.py`, record the manifest slots/hashes and
upgrade authority, and ensure the captured program hash corresponds to the
behavior tested. Then provide a reproducible controlled-wallet Devnet test,
pre/post state, a negative control, impact, and remediation. No mainnet testing
is required or permitted by this workspace's scope.
