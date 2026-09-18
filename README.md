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

The command fails closed when an IDL is missing, malformed, or declares an
unexpected program address. It inventories writable and signer accounts,
optional accounts, PDA metadata, and fixed addresses. It also raises
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

## Capture deployed Devnet evidence

With access to the official Solana Devnet RPC, capture the executable and
ProgramData accounts without sending any transaction:

```bash
python3 -m scripts.capture_devnet --output evidence/devnet
```

The command verifies the Upgradeable Loader owner and executable flag, derives
each ProgramData address from the loader state, and records the genesis hash,
finalized RPC slots, addresses, and SHA-256 hashes in `manifest.json`. This is a
read-only operation; it does not create a keypair or submit a transaction.

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
