# Pump.fun Devnet audit workspace

This repository contains a small, dependency-free utility for inventorying the
public Anchor IDLs that are in scope for the Pump.fun Cantina program. It does
**not** interact with mainnet or production services.

## Safety and scope

Only these Devnet programs are accepted by the tool:

| IDL | Expected program address |
| --- | --- |
| `pump.json` | `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P` |
| `pump_fees.json` | `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ` |
| `pump_amm.json` | `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA` |

Do not test against mainnet, access user data, cause denial of service, or move
funds that you do not own. A generated inventory is an audit aid, not a
vulnerability report.

## Generate the inventory

Download the three public IDLs from the official `pump-fun/pump-public-docs`
repository and generate the inventory in one command:

```bash
python3 scripts/inventory_idls.py --download --output audit/attack-surface.md
```

The downloader uses the three `raw.githubusercontent.com` URLs corresponding to
the in-scope links. Downloads are limited to 5 MiB per file, staged in a
temporary directory, and checked as a complete set before replacing local
files. For a fully offline run, manually place the files in `idl/` and omit
`--download`.

The checked-in result is [`audit/attack-surface.md`](audit/attack-surface.md),
and the corresponding static triage and Devnet validation queue are documented
in [`audit/STATIC_ANALYSIS.md`](audit/STATIC_ANALYSIS.md).

The command fails closed when an IDL is missing, malformed, or declares an
unexpected program address. It inventories writable and signer accounts,
optional accounts, PDA metadata, fixed addresses, declarative relations, and
instruction/account documentation. It also raises
manual-review indicators for instructions with no visible signer, optional
signers, and program-like accounts without a fixed address in the IDL. These
indicators need constraint and runtime validation; they are not proof of an
exploit. Reports also include the complete argument types, PDA seed metadata,
and SHA-256 digest of every input IDL so a later proof of concept can identify
the exact interface that was reviewed.

Run the offline test suite with:

```bash
python3 -m unittest discover -s tests -v
```

Check the internally published `buy_exact_sol_in` quote formulas with:

```bash
python3 scripts/audit_quote_math.py --limit 64
```

The assumptions and remaining runtime questions are recorded in
[`audit/MATH_REVIEW.md`](audit/MATH_REVIEW.md).

Before executing or reporting a candidate, apply the Devnet-only safety,
severity, evidence, and submission gates in [`audit/SCOPE.md`](audit/SCOPE.md).

Generate exact instruction discriminators, account order, and mutation indices
for the controlled P1 experiments with:

```bash
python3 -m scripts.candidate_vectors --output audit/candidate-vectors.json
```

The vectors contain no keys or transactions; they bind an external Devnet test
runner to the reviewed IDL hashes and make accidental account-index changes
visible before signing.

Check relation/PDA references and known associated-token seed anomalies with:

```bash
python3 -m scripts.audit_idl_consistency
```

The current interpretation is recorded in
[`audit/IDL_INTEGRITY.md`](audit/IDL_INTEGRITY.md).

The submission decision matrix is in
[`audit/ELIGIBILITY.md`](audit/ELIGIBILITY.md); notably, IDL/client failures and
atomic quote failures are closed unless a separate Devnet proof demonstrates
eligible financial impact.

## Capture deployed Devnet evidence

With access to the official Solana Devnet RPC, capture the executable and
ProgramData accounts without sending any transaction:

```bash
python3 -m scripts.capture_devnet --output evidence/devnet
```

The command first verifies the canonical Solana Devnet genesis hash, then checks
the Upgradeable Loader owner and executable flag, derives each ProgramData
address from the loader state, and records the genesis hash,
finalized RPC slots, addresses, and SHA-256 hashes in `manifest.json`. This is a
read-only operation; it does not create a keypair or submit a transaction. The
manifest also decodes the ProgramData deployment slot, upgrade authority (or
immutability), metadata length, and ELF length instead of treating arbitrary
loader-owned bytes as valid ProgramData.

## Suggested review order

1. Authorization and PDA seed/domain separation.
2. Token mint, token-program, vault, fee-recipient, and authority constraints.
3. Bonding-curve and AMM arithmetic, rounding, slippage, and reserve updates.
4. Fee collection and sharing, including confused-deputy paths.
5. Lifecycle transitions such as completion, migration, initialization, and
   account closure.

Any candidate finding should be reproduced only on Devnet with wallets and
tokens controlled by the researcher. A Cantina submission should include the
test script, environment, exact transaction/signature, impact, remediation,
and a video showing the controlled reproduction.
