# Candidate eligibility decision

## Decision

The legacy `pump::migrate` duplicate-seed issue is **not the finding to submit
for a reward**. It is confirmed as an IDL metadata defect, but there is no
evidence of an unauthorized state transition, loss, freeze, or successful
value-extracting transaction. Its demonstrated effect is limited to clients
potentially deriving unusable account addresses and failing before execution.

Submitting it now would conflict with this workspace's acceptance gate and is
unlikely to meet the supplied smart-contract impact guidance. It should remain
closed unless a separate Devnet test proves that the deployed handler accepts a
wrong vault or causes measurable financial harm.

The documented quote-math inconsistency has the same disposition for reward
purposes: its current consequence is an expected atomic slippage failure, not a
successful loss-producing transaction.

## Reward-oriented queue

Only the following unresolved candidates currently have a plausible route to
eligible financial impact:

| Priority | Candidate | Required result before submission |
| --- | --- | --- |
| P1 | AMM cashback recipient substitution | A controlled user A's cashback is successfully transferred to a token account owned by controlled user B. |
| P1 | Creator-fee destination substitution | Accrued creator fees are successfully redirected to an unrelated controlled account. |
| P1 | Token-2022 accounting mismatch | A successful trade produces repeatable net extraction or unauthorized loss after comparing actual vault deltas. |
| P1 | Donation-relay confused deputy | The Fees PDA signature moves value or credits state to an unrelated controlled relay configuration. |

These are hypotheses, not findings. None can be represented as reward-eligible
until its confirmation condition succeeds on an in-scope Devnet deployment,
its negative control behaves safely, and the result is repeatable.

## Go/no-go checklist

A candidate is a **go** for private submission only if every answer is yes:

1. Did it execute against one of the three in-scope Devnet program addresses?
2. Were every wallet, mint, pool, account, token, and unit of value controlled by
   the researcher?
3. Did a transaction succeed and produce an unauthorized balance/state change,
   or did it permanently freeze/waste controlled value in a way representative
   of real user impact?
4. Does a negative control demonstrate that the safe account combination does
   not produce the same unauthorized outcome?
5. Is the behavior repeatable and pinned to captured Program/ProgramData hashes
   and RPC slots?
6. Is there an Anchor/CLI PoC, transaction signature, logs, pre/post state,
   remediation, and video?
7. Is the issue still in scope and apparently unreported after checking the live
   Cantina program immediately before submission?

Any “no” means **do not submit yet**. No audit process can guarantee a payout:
Cantina/Pump.fun determines eligibility and reward, and the researcher must also
be first to report a previously unknown issue.

## Current blocker

The execution environment cannot reach the official Devnet RPC: the configured
HTTPS proxy rejects CONNECT with `403`, while bypassing it leaves DNS
unavailable. Therefore the four P1 confirmation conditions cannot be honestly
evaluated here. An environment with official Devnet RPC access plus
researcher-controlled funded states is required; no mainnet fallback is
acceptable.
