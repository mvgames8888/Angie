# Private candidate queue

This file records hypotheses for controlled Devnet validation. **Nothing here
is a confirmed or reportable vulnerability.** Do not test these hypotheses on
mainnet or with accounts, tokens, or funds belonging to other users.

## C-01 — AMM cashback recipient substitution

**Priority:** P1
**State:** blocked on Devnet evidence and a researcher-controlled cashback state

`pump_amm::claim_cashback` is permissionless and accepts
`user_wsol_token_account` as a writable, non-PDA account. Its documentation says
the account may be non-associated but must be a token account of `quote_mint`
owned by `user`. In contrast, the Pump IDL exposes the explicit
`InvalidCashbackRecipient` error, while the AMM error list does not expose an
equivalent error. This asymmetry is only a lead: custom validation can use a
generic error or a check that is invisible in an IDL.

### Controlled validation

1. Create a researcher-controlled user **A**, unrelated researcher-controlled
   user **B**, and their wSOL token accounts on Devnet.
2. Produce cashback accrual for A through the intended in-scope Devnet flow.
3. Record A's accumulator, both token balances, relevant vault balance, RPC
   slot, and the captured program hash.
4. Negative control: claim A's cashback to a non-associated token account owned
   by A. This should succeed according to the IDL documentation.
5. Recreate equivalent accrual for A. Invoke `claim_cashback` with `user=A` but
   B's wSOL token account as `user_wsol_token_account`, signed only by the
   transaction payer because the instruction declares no signer.
6. Record the transaction logs and all post-state balances even if it fails.

**Confirmation condition:** the second call succeeds and moves A's accrued
cashback to an account owned by B.
**Rejection condition:** the program rejects the owner mismatch before changing
the accumulator or balances.
**Required negative control:** an A-owned non-associated account succeeds under
otherwise identical conditions.

Do not report a generic-error difference, the lack of a signer, or the IDL
shape. Only an unauthorized balance transfer demonstrated on Devnet is a
finding.

## C-02 — creator-fee destination substitution

**Priority:** P1
**State:** blocked on Devnet evidence and researcher-controlled creator fees

Pump `collect_creator_fee`/`collect_creator_fee_v2` and AMM
`collect_coin_creator_fee` expose no signer. Their vaults are creator-derived,
but legacy/native destinations are plain writable accounts and the AMM token
destination is not represented as a PDA. Permissionless collection can be
intentional; the security property is that the destination must belong to the
creator encoded by the vault seeds or state.

Validate with a researcher-created coin/pool and accrued creator fees. First
collect to the creator's intended destination, then recreate fees and substitute
an unrelated researcher-owned system/token account while holding all other
accounts constant. Reject this candidate if the substitution fails atomically.
Confirm only if value reaches the unrelated account and quantify the repeatable
loss.

## C-03 — Token-2022 transfer-accounting mismatch

**Priority:** P1
**State:** requires supported-mint setup on Devnet

Several v2 trade paths accept caller-supplied token interface programs and the
IDL explicitly contains quote-token-program validation errors. This makes a
fake-program substitution less promising than transfer-accounting differences
from supported Token-2022 extensions.

Create only researcher-owned mints and test supported combinations with transfer
fees and transfer hooks. Compare requested amounts, actual vault deltas, reserve
fields, fees, and slippage checks for buy/sell round trips. Confirm only when a
repeatable mismatch permits net extraction or unauthorized loss; failures,
rounding dust, and denial of service are not sufficient.

## C-04 — donation-relay CPI account substitution

**Priority:** P1
**State:** requires a researcher-controlled donation PDA and relay state

Fees `crank_donation_fee_pda` is a public crank that signs for a
`donation_fee_pda` and invokes the fixed donation-relay program. The donation
PDA and its ATA are seed constrained, but `mint_whitelist`, `epoch_tracker`,
`debouncer`, and `debouncer_ata` are caller-supplied; the latter three are
writable. The IDL cannot show whether the Fees handler or relay relates those
accounts to the donation mint/config before the signed CPI.

Create two entirely researcher-controlled relay configurations A and B on
Devnet. Fund only donation PDA A, then invoke its crank while substituting B's
whitelist/tracker/debouncer tuple one account at a time and finally as a complete
tuple. Compare the donation vault, relay recipient, tracker, and debouncer state
against a normal A-only control.

**Confirmation condition:** the Fees PDA signature authorizes value movement or
state credit for an unrelated relay configuration.
**Rejection condition:** each mixed configuration fails atomically, while the
all-A control succeeds.

This candidate concerns a possible confused-deputy boundary, not the mere
presence of caller-supplied CPI accounts. Do not interact with relay state or
funds not created by the researcher.

## C-05 — reverse quote under-delivers at split-fee rounding boundaries

**Priority:** P3 / archive unless financial impact is demonstrated
**State:** documented-formula counterexample; no eligible impact established

The `buy_exact_sol_in` reverse formula combines protocol and creator basis
points before applying one ceiling. The forward formula instead ceilings both
fee components separately and may reduce `net_sol` by one to remain within the
budget. That correction also consumes the reverse formula's single-unit
cushion, causing fewer tokens than requested in many small-value cases.

The offline grid in `audit/MATH_REVIEW.md` found 342,165 counterexamples among
903,168 bounded cases. This is not reportable on its own: the instruction's
`min_tokens_out` should cause an atomic failure. Validate whether official
clients use the published reverse quote, whether the deployed calculation
matches it, and whether any successful transaction can lose value or create a
repeatable skim. Otherwise classify it as documentation/UX only.

The current program gate in `audit/SCOPE.md` makes a failed transaction or
client quote mismatch Low/Informational at most. Do not spend Devnet funds on
this candidate until the value-moving P1 candidates have been resolved.

## Evidence blocker

The local capture attempt on 2026-09-18 failed before reading any account
because the environment's HTTPS proxy returned `403 Forbidden` for the official
Devnet RPC. No fallback cluster was used. Run the read-only capture from an
environment that can reach `https://api.devnet.solana.com`, then preserve the
generated manifest and binaries before executing any candidate test.
