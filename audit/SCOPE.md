# Program scope and submission gate

## Source and freshness

This file records the Cantina program text supplied by the researcher on
2026-09-18. The live Cantina page could not be independently refreshed from
this environment because the web endpoint returned `401 Unauthorized`. Program
terms can change, so the live Instructions and Scope tabs must be checked again
immediately before testing and submission.

## Smart-contract boundary

Only the Devnet deployments at these addresses are in scope for the contract
review:

| Program | Devnet address |
| --- | --- |
| Pump | `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P` |
| Pump Fees | `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ` |
| Pump AMM | `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA` |

Do not reproduce a contract candidate on mainnet. Use only researcher-owned
wallets, mints, pools, token accounts, and funds. Stop after the minimum proof
of impact and do not access another user's data or assets.

## Reward and impact interpretation

The supplied program header advertises a maximum reward of **$500,000**. The
separate Web & Mobile asset-group table supplied later lists Critical up to
$50,000, High up to $25,000, Medium up to $10,000, and discretionary Low/Info.
Those Web & Mobile caps must not be applied to a smart-contract candidate. The
live Smart Contracts asset-group payout table must be rechecked before relying
on any amount.

For smart-contract triage, prioritize demonstrated financial impact:

- **Critical:** loss, waste, or permanent freeze affecting roughly 20%–100% of
  total bonding-curve/AMM TVL, or comparable systemic impact.
- **High:** roughly 0.5%–20% of total TVL, or substantial harm to users.
- **Medium:** smaller loss affecting individual users or pools, or a repeatable
  value-extracting inefficiency such as exploitable slippage arithmetic.
- **Low/Informational:** best practices, documentation mismatches, and failed
  transactions without measurable impact are at most discretionary.

Reward size is not evidence of severity. Severity must follow the reproducible
impact and likelihood, not the theoretical maximum.

## Submission requirements

A contract candidate remains private and unsubmitted until the package includes:

1. a clear vulnerability description and real-world impact;
2. an Anchor `.ts`/`.rs` test or equivalent Solana CLI reproduction;
3. a video demonstrating the impact;
4. environment and exact Devnet deployment details;
5. controlled test wallets/accounts and any mocked data needed to reproduce;
6. pre-state, post-state, transaction signature, logs, program hashes, and RPC
   slots;
7. a negative control and repeatability evidence; and
8. a remediation recommendation.

Submit promptly after confirmation (the supplied terms request within 24 hours
if possible), do not disclose publicly, and remain available for verification.

## Exclusions relevant to this audit

Do not elevate any of the following without direct eligible impact:

- denial of service or brute force;
- a known dependency issue without a working in-scope proof;
- a UI-only or content-spoofing issue without a sensitive action;
- assumptions requiring MITM, physical access, or a compromised device;
- generic TLS/email configuration issues;
- third-party behavior without a demonstrated Pump-owned impact; or
- data access or exfiltration beyond the minimum authorized proof.
