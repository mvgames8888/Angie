# Anchor IDL attack-surface inventory

> Generated metadata for manual security review. Indicators below are not findings.

## Summary

- Instructions inventoried: **109**
- Manual-review indicators: **136**

### Input provenance

- `pump.json` — SHA-256 `d9ba3eb509ccf315baa9ac655a3bcf45506a6c477af2b16f3f5ba93a135aec29`
- `pump_fees.json` — SHA-256 `510536a37bf40222fe6c307edd81df1a3c34a8009ca7479a4033aee478feddc5`
- `pump_amm.json` — SHA-256 `a169522f756aacd6e03d32dd1ee63321a6196442e9d7e0edc9a77d1a9e30f4dc`

## `pump.json`

### `add_quote_control_mint`

- Arguments: **2**
  - `quote_mint`: `"pubkey"`
  - `initial_virtual_quote_reserves`: `"u64"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `authority` — writable, signer
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `quote_control` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[113,117,111,116,101,45,99,111,110,116,114,111,108]}]`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `add_quote_mint`

- Arguments: **1**
  - `quote_mint`: `"pubkey"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `global` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `authority` — writable, signer
    - Relations: `global`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `admin_cto`

- Arguments: **3**
  - `is_holder_reward`: `{"option":"bool"}`
  - `creator_fee_bps`: `{"option":"u64"}`
  - `new_creator`: `{"option":"pubkey"}`
- Visible signers: `admin_set_creator_authority`
- Review indicators:
  - Program-like account `quote_token_program` has no fixed address in the IDL
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `admin_set_creator_authority` — writable, signer
    - Relations: `global`
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `mint` — read-only
  - `quote_mint` — read-only
  - `quote_token_program` — read-only
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"kind":"account","path":"mint"}]`
  - `current_creator` — read-only
    - Documentation: Not declared writable: a pre-creator (legacy) curve stores the zero key, which is the system program, whose write lock the runtime always demotes. Callers MUST still pass this account as writable whenever it is a wallet, so the outgoing creator can be paid from its vaults; otherwise the instruction fails with `CtoCreatorAccountNotWritable`. A creator that is not a system-owned wallet (a program, a sysvar, a pump-fees or other program-owned account) is skipped, its vault balances stay collectable, and it may be passed read-only.
  - `current_creator_quote_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"current_creator"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"account","path":"associated_token_program"}`
  - `creator_vault` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,45,118,97,117,108,116]},{"kind":"account","path":"current_creator"}]`
  - `creator_vault_quote_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"creator_vault"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"account","path":"associated_token_program"}`
  - `holder_creator_vault` — writable
    - Documentation: `["creator-vault", find_program_address(["holder-rewards", mint], pump)]`. The sweep destination on the holder path of a fee-shared coin, ignored otherwise. Re-derived in the handler before it is written to; kept out of the seeds constraints to stay under the sBPF stack frame.
  - `holder_creator_vault_quote_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"holder_creator_vault"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"account","path":"associated_token_program"}`
  - `pump_amm` — fixed `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA`
  - `amm_global_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108,95,99,111,110,102,105,103]}], program={"kind":"account","path":"pump_amm"}`
  - `pool_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[112,111,111,108,45,97,117,116,104,111,114,105,116,121]},{"kind":"account","path":"mint"}]`
  - `pool` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[112,111,111,108]},{"kind":"const","value":[0,0]},{"kind":"account","path":"pool_authority"},{"kind":"account","path":"mint"},{"kind":"account","path":"quote_mint"}], program={"kind":"account","path":"pump_amm"}`
  - `pump_amm_event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}], program={"kind":"account","path":"pump_amm"}`
  - `coin_creator_vault_authority` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,95,118,97,117,108,116]},{"kind":"account","path":"current_creator"}], program={"kind":"account","path":"pump_amm"}`
  - `coin_creator_vault_ata` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"coin_creator_vault_authority"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"account","path":"associated_token_program"}`
  - `sharing_config` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[115,104,97,114,105,110,103,45,99,111,110,102,105,103]},{"kind":"account","path":"mint"}], program={"kind":"account","path":"pump_fees"}`
  - `pump_fees` — fixed `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ`
  - `pump_fees_event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}], program={"kind":"account","path":"pump_fees"}`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `admin_set_idl_authority`

- Arguments: **1**
  - `idl_authority`: `"pubkey"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `authority` — signer
    - Relations: `global`
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `idl_account` — writable
  - `system_program` — fixed `11111111111111111111111111111111`
  - `program_signer` — PDA
    - PDA: `seeds=[]`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `admin_update_token_incentives`

- Arguments: **5**
  - `start_time`: `"i64"`
  - `end_time`: `"i64"`
  - `seconds_in_a_day`: `"i64"`
  - `day_number`: `"u64"`
  - `pump_token_supply_per_day`: `"u64"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `token_program` has no fixed address in the IDL
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `authority` — writable, signer
    - Relations: `global`
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `global_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]}]`
  - `mint` — read-only
  - `global_incentive_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"global_volume_accumulator"},{"kind":"account","path":"token_program"},{"kind":"account","path":"mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `token_program` — read-only
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `buy`

- Arguments: **3**
- Documentation: Buys tokens from a bonding curve.
  - `amount`: `"u64"`
  - `max_sol_cost`: `"u64"`
  - `track_volume`: `{"defined":{"name":"OptionBool"}}`
- Visible signers: `user`
- Review indicators:
  - Program-like account `token_program` has no fixed address in the IDL
- Accounts:
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `fee_recipient` — writable
  - `mint` — read-only
  - `bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"kind":"account","path":"mint"}]`
  - `associated_bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"bonding_curve"},{"kind":"account","path":"token_program"},{"kind":"account","path":"mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `associated_user` — writable
  - `user` — writable, signer
  - `system_program` — fixed `11111111111111111111111111111111`
  - `token_program` — read-only
  - `creator_vault` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,45,118,97,117,108,116]},{"account":"BondingCurve","kind":"account","path":"bonding_curve.creator"}]`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`
  - `global_volume_accumulator` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]}]`
  - `user_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[117,115,101,114,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]},{"kind":"account","path":"user"}]`
  - `fee_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,95,99,111,110,102,105,103]},{"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}], program={"kind":"account","path":"fee_program"}`
  - `fee_program` — fixed `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ`

### `buy_exact_quote_in_v2`

- Arguments: **2**
  - `spendable_quote_in`: `"u64"`
  - `min_tokens_out`: `"u64"`
- Visible signers: `user`
- Review indicators:
  - Program-like account `base_token_program` has no fixed address in the IDL
  - Program-like account `quote_token_program` has no fixed address in the IDL
- Accounts:
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `base_mint` — read-only
  - `quote_mint` — read-only
  - `base_token_program` — read-only
  - `quote_token_program` — read-only
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `fee_recipient` — writable
  - `associated_quote_fee_recipient` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"fee_recipient"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `buyback_fee_recipient` — writable
  - `associated_quote_buyback_fee_recipient` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"buyback_fee_recipient"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"kind":"account","path":"base_mint"}]`
  - `associated_base_bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"bonding_curve"},{"kind":"account","path":"base_token_program"},{"kind":"account","path":"base_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `associated_quote_bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"bonding_curve"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `user` — writable, signer
  - `associated_base_user` — writable
  - `associated_quote_user` — writable
    - Documentation: canonical SPL associated-token PDA. Validated in handlers via `validate_user_quote_token_account` for non-legacy mints; ignored for legacy (SOL) trades.
  - `creator_vault` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,45,118,97,117,108,116]},{"account":"BondingCurve","kind":"account","path":"bonding_curve.creator"}]`
  - `associated_creator_vault` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"creator_vault"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `sharing_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[115,104,97,114,105,110,103,45,99,111,110,102,105,103]},{"kind":"account","path":"base_mint"}], program={"kind":"const","value":[12,53,255,169,5,90,142,86,141,168,247,188,7,86,21,39,76,241,201,44,164,31,64,0,156,81,106,164,20,194,124,112]}`
    - Documentation: seeds; the account is intentionally not deserialized here because it may be uninitialized for mints that have not created a fee sharing config. Handlers must check `data_is_empty()` / owner before reading.
  - `global_volume_accumulator` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]}]`
  - `user_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[117,115,101,114,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]},{"kind":"account","path":"user"}]`
  - `associated_user_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"user_volume_accumulator"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `fee_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,95,99,111,110,102,105,103]},{"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}], program={"kind":"account","path":"fee_program"}`
  - `fee_program` — fixed `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`

### `buy_exact_sol_in`

- Arguments: **3**
- Documentation: Given a budget of spendable SOL, buy at least min_tokens_out tokens. Fees are deducted from spendable_sol_in. # Quote formulas Where: - total_fee_bps = protocol_fee_bps + creator_fee_bps (creator_fee_bps is 0 if no creator) - floor(a/b) = a / b (integer division) - ceil(a/b) = (a + b - 1) / b SOL → tokens quote To calculate tokens_out for a given spendable_sol_in: 1. net_sol = floor(spendable_sol_in * 10_000 / (10_000 + total_fee_bps)) 2. fees = ceil(net_sol * protocol_fee_bps / 10_000) + ceil(net_sol * creator_fee_bps / 10_000) (creator_fee_bps is 0 if no creator) 3. if net_sol + fees > spendable_sol_in: net_sol = net_sol - (net_sol + fees - spendable_sol_in) 4. tokens_out = floor((net_sol - 1) * virtual_token_reserves / (virtual_sol_reserves + net_sol - 1)) Reverse quote (tokens → SOL) To calculate spendable_sol_in for a desired number of tokens: 1. net_sol = ceil(tokens * virtual_sol_reserves / (virtual_token_reserves - tokens)) + 1 2. spendable_sol_in = ceil(net_sol * (10_000 + total_fee_bps) / 10_000) Rent Separately make sure the instruction's payer has enough SOL to cover rent for: - creator_vault: rent.minimum_balance(0) - user_volume_accumulator: rent.minimum_balance(UserVolumeAccumulator::LEN)
  - `spendable_sol_in`: `"u64"`
  - `min_tokens_out`: `"u64"`
  - `track_volume`: `{"defined":{"name":"OptionBool"}}`
- Visible signers: `user`
- Review indicators:
  - Program-like account `token_program` has no fixed address in the IDL
- Accounts:
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `fee_recipient` — writable
  - `mint` — read-only
  - `bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"kind":"account","path":"mint"}]`
  - `associated_bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"bonding_curve"},{"kind":"account","path":"token_program"},{"kind":"account","path":"mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `associated_user` — writable
  - `user` — writable, signer
  - `system_program` — fixed `11111111111111111111111111111111`
  - `token_program` — read-only
  - `creator_vault` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,45,118,97,117,108,116]},{"account":"BondingCurve","kind":"account","path":"bonding_curve.creator"}]`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`
  - `global_volume_accumulator` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]}]`
  - `user_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[117,115,101,114,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]},{"kind":"account","path":"user"}]`
  - `fee_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,95,99,111,110,102,105,103]},{"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}], program={"kind":"account","path":"fee_program"}`
  - `fee_program` — fixed `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ`

### `buy_v2`

- Arguments: **2**
  - `amount`: `"u64"`
  - `max_sol_cost`: `"u64"`
- Visible signers: `user`
- Review indicators:
  - Program-like account `base_token_program` has no fixed address in the IDL
  - Program-like account `quote_token_program` has no fixed address in the IDL
- Accounts:
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `base_mint` — read-only
  - `quote_mint` — read-only
  - `base_token_program` — read-only
  - `quote_token_program` — read-only
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `fee_recipient` — writable
  - `associated_quote_fee_recipient` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"fee_recipient"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `buyback_fee_recipient` — writable
  - `associated_quote_buyback_fee_recipient` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"buyback_fee_recipient"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"kind":"account","path":"base_mint"}]`
  - `associated_base_bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"bonding_curve"},{"kind":"account","path":"base_token_program"},{"kind":"account","path":"base_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `associated_quote_bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"bonding_curve"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `user` — writable, signer
  - `associated_base_user` — writable
  - `associated_quote_user` — writable
    - Documentation: canonical SPL associated-token PDA. Validated in handlers via `validate_user_quote_token_account` for non-legacy mints; ignored for legacy (SOL) trades.
  - `creator_vault` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,45,118,97,117,108,116]},{"account":"BondingCurve","kind":"account","path":"bonding_curve.creator"}]`
  - `associated_creator_vault` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"creator_vault"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `sharing_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[115,104,97,114,105,110,103,45,99,111,110,102,105,103]},{"kind":"account","path":"base_mint"}], program={"kind":"const","value":[12,53,255,169,5,90,142,86,141,168,247,188,7,86,21,39,76,241,201,44,164,31,64,0,156,81,106,164,20,194,124,112]}`
    - Documentation: seeds; the account is intentionally not deserialized here because it may be uninitialized for mints that have not created a fee sharing config. Handlers must check `data_is_empty()` / owner before reading.
  - `global_volume_accumulator` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]}]`
  - `user_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[117,115,101,114,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]},{"kind":"account","path":"user"}]`
  - `associated_user_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"user_volume_accumulator"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `fee_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,95,99,111,110,102,105,103]},{"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}], program={"kind":"account","path":"fee_program"}`
  - `fee_program` — fixed `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`

### `claim_cashback`

- Arguments: **0**
- Visible signers: **none**
- Review indicators:
  - No signer is visible in the IDL
- Accounts:
  - `user` — writable
  - `user_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[117,115,101,114,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]},{"kind":"account","path":"user"}]`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`

### `claim_cashback_v2`

- Arguments: **0**
- Documentation: Pays out the user's accrued cashback. For a token quote, `associated_quote_user` may be any token account of `quote_mint` owned by `user`, not only the associated one.
- Visible signers: **none**
- Review indicators:
  - No signer is visible in the IDL
  - Program-like account `quote_token_program` has no fixed address in the IDL
- Accounts:
  - `user` — writable
  - `user_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[117,115,101,114,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]},{"kind":"account","path":"user"}]`
  - `quote_mint` — read-only
  - `quote_token_program` — read-only
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `associated_user_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"user_volume_accumulator"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"account","path":"associated_token_program"}`
  - `associated_quote_user` — writable
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`

### `claim_token_incentives`

- Arguments: **0**
- Visible signers: `payer`
- Review indicators:
  - Program-like account `token_program` has no fixed address in the IDL
- Accounts:
  - `user` — read-only
  - `user_ata` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"user"},{"kind":"account","path":"token_program"},{"kind":"account","path":"mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `global_volume_accumulator` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]}]`
  - `global_incentive_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"global_volume_accumulator"},{"kind":"account","path":"token_program"},{"kind":"account","path":"mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `user_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[117,115,101,114,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]},{"kind":"account","path":"user"}]`
  - `mint` — read-only
    - Relations: `global_volume_accumulator`
  - `token_program` — read-only
  - `system_program` — fixed `11111111111111111111111111111111`
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`
  - `payer` — writable, signer

### `close_user_volume_accumulator`

- Arguments: **0**
- Visible signers: `user`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `user` — writable, signer
  - `user_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[117,115,101,114,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]},{"kind":"account","path":"user"}]`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `collect_creator_fee`

- Arguments: **0**
- Documentation: Collects creator_fee from creator_vault to the coin creator account
- Visible signers: **none**
- Review indicators:
  - No signer is visible in the IDL
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `creator` — writable
  - `creator_vault` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,45,118,97,117,108,116]},{"kind":"account","path":"creator"}]`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `collect_creator_fee_v2`

- Arguments: **0**
- Documentation: Collects creator_fee from creator_vault to the coin creator account
- Visible signers: **none**
- Review indicators:
  - No signer is visible in the IDL
  - Program-like account `quote_token_program` has no fixed address in the IDL
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `creator` — writable
  - `creator_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"creator"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"account","path":"associated_token_program"}`
  - `creator_vault` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,45,118,97,117,108,116]},{"kind":"account","path":"creator"}]`
  - `creator_vault_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"creator_vault"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"account","path":"associated_token_program"}`
  - `quote_mint` — read-only
  - `quote_token_program` — read-only
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `create`

- Arguments: **4**
- Documentation: Creates a new coin and bonding curve.
  - `name`: `"string"`
  - `symbol`: `"string"`
  - `uri`: `"string"`
  - `creator`: `"pubkey"`
- Visible signers: `mint`, `user`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `mint` — writable, signer
  - `mint_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[109,105,110,116,45,97,117,116,104,111,114,105,116,121]}]`
  - `bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"kind":"account","path":"mint"}]`
  - `associated_bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"bonding_curve"},{"kind":"const","value":[6,221,246,225,215,101,161,147,217,203,225,70,206,235,121,172,28,180,133,237,95,91,55,145,58,140,245,133,126,255,0,169]},{"kind":"account","path":"mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `mpl_token_metadata` — fixed `metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s`
  - `metadata` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[109,101,116,97,100,97,116,97]},{"kind":"const","value":[11,112,101,177,227,209,124,69,56,157,82,127,107,4,195,205,88,184,108,115,26,160,253,181,73,182,209,188,3,248,41,70]},{"kind":"account","path":"mint"}], program={"kind":"account","path":"mpl_token_metadata"}`
  - `user` — writable, signer
  - `system_program` — fixed `11111111111111111111111111111111`
  - `token_program` — fixed `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `rent` — fixed `SysvarRent111111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `create_v2`

- Arguments: **8**
- Documentation: Creates a new spl-22 coin and bonding curve. Remaining accounts select the quote mint (none = SOL): `quote_mint`, `associated_quote_bonding_curve`, `quote_token_program` (SPL Token or Token-2022; must own the mint), plus an optional fourth account, the `quote-control` PDA, read only when `Global` does not whitelist the mint. A mint admitted through quote-control seeds the curve's virtual quote reserves from its quote-control entry instead of `Global`, and cannot be used with `is_mayhem_mode` (`MayhemModeQuoteMintNotAllowed`). The Token-2022 native mint is rejected, and a Token-2022 quote mint may only carry the xStock operable extension set (metadata pointer/metadata, permanent delegate, initialized default account state, scaled UI amount, pausable, confidential-transfer mint, and a transfer hook with no program). The trailing `creator_fee_bps` argument (EOF-tolerant) sets the coin's own creator fee rate for a quote mint admitted through quote-control, and then requires `Global.creator_fee_configurable`, a non-cashback coin and a value in `1..=Global.max_configurable_creator_fee_bps`; on a SOL or `Global`-whitelisted quote it is ignored, and omitted or zero stores 0 so the pump-fees schedule rate applies. `is_cashback_enabled` is deprecated and must be false. `is_holder_reward` (EOF-tolerant, gated by `Global.is_holder_reward_enabled`) sets the creator to the `holder-rewards` PDA of the mint, so creator fees accrue to its creator vault, are collected onto the PDA with `collect_creator_fee*` and paid out through `distribute_fee_to_holders`.
  - `name`: `"string"`
  - `symbol`: `"string"`
  - `uri`: `"string"`
  - `creator`: `"pubkey"`
  - `is_mayhem_mode`: `"bool"`
  - `is_cashback_enabled`: `{"defined":{"name":"OptionBool"}}`
  - `creator_fee_bps`: `{"defined":{"name":"OptionU64"}}`
  - `is_holder_reward`: `{"defined":{"name":"OptionBool"}}`
- Visible signers: `mint`, `user`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `mint` — writable, signer
  - `mint_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[109,105,110,116,45,97,117,116,104,111,114,105,116,121]}]`
  - `bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"kind":"account","path":"mint"}]`
  - `associated_bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"bonding_curve"},{"kind":"account","path":"token_program"},{"kind":"account","path":"mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `user` — writable, signer
  - `system_program` — fixed `11111111111111111111111111111111`
  - `token_program` — fixed `TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `mayhem_program_id` — writable, fixed `MAyhSmzXzV1pTf7LsNkrNwkWKTo4ougAJ1PPg47MD4e`
  - `global_params` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108,45,112,97,114,97,109,115]}], program={"kind":"const","value":[5,42,229,215,167,218,167,36,166,234,176,167,41,84,145,133,90,212,160,103,22,96,103,76,78,3,69,89,128,61,101,163]}`
  - `sol_vault` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[115,111,108,45,118,97,117,108,116]}], program={"kind":"const","value":[5,42,229,215,167,218,167,36,166,234,176,167,41,84,145,133,90,212,160,103,22,96,103,76,78,3,69,89,128,61,101,163]}`
  - `mayhem_state` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[109,97,121,104,101,109,45,115,116,97,116,101]},{"kind":"account","path":"mint"}], program={"kind":"const","value":[5,42,229,215,167,218,167,36,166,234,176,167,41,84,145,133,90,212,160,103,22,96,103,76,78,3,69,89,128,61,101,163]}`
  - `mayhem_token_vault` — writable
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `distribute_creator_fees`

- Arguments: **0**
- Documentation: Distributes creator fees to shareholders based on their share percentages The creator vault needs to have at least the minimum distributable amount to distribute fees This can be checked with the get_minimum_distributable_fee instruction
- Visible signers: **none**
- Review indicators:
  - No signer is visible in the IDL
- Accounts:
  - `mint` — read-only
    - Relations: `sharing_config`
  - `bonding_curve` — PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"kind":"account","path":"mint"}]`
  - `sharing_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[115,104,97,114,105,110,103,45,99,111,110,102,105,103]},{"kind":"account","path":"mint"}], program={"kind":"const","value":[12,53,255,169,5,90,142,86,141,168,247,188,7,86,21,39,76,241,201,44,164,31,64,0,156,81,106,164,20,194,124,112]}`
  - `creator_vault` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,45,118,97,117,108,116]},{"account":"BondingCurve","kind":"account","path":"bonding_curve.creator"}]`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`

### `distribute_creator_fees_v2`

- Arguments: **1**
  - `initialize_ata`: `"bool"`
- Visible signers: `payer`
- Review indicators:
  - Program-like account `quote_token_program` has no fixed address in the IDL
- Accounts:
  - `payer` — writable, signer
  - `mint` — read-only
    - Relations: `sharing_config`
  - `bonding_curve` — PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"kind":"account","path":"mint"}]`
  - `sharing_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[115,104,97,114,105,110,103,45,99,111,110,102,105,103]},{"kind":"account","path":"mint"}], program={"kind":"const","value":[12,53,255,169,5,90,142,86,141,168,247,188,7,86,21,39,76,241,201,44,164,31,64,0,156,81,106,164,20,194,124,112]}`
  - `creator_vault` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,45,118,97,117,108,116]},{"account":"BondingCurve","kind":"account","path":"bonding_curve.creator"}]`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`
  - `creator_vault_quote_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"creator_vault"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"account","path":"associated_token_program"}`
    - Documentation: Deserialized manually in the handler for non-legacy quote mints.
  - `quote_mint` — read-only
  - `quote_token_program` — read-only
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`

### `distribute_fee_to_holders`

- Arguments: **1**
- Documentation: Pays fees collected on the `holder-rewards` PDA (via `collect_creator_fee*` with the PDA as creator) out to holders: `amounts[i]` goes to remaining accounts `[2i]` (owner) / `[2i + 1]` (its quote ATA, created if missing). `holder_rewards_token_account` is any quote token account owned by the PDA (normally its ATA): the source on a token quote, and on a SOL quote a parked WSOL account closed into the PDA first; pass the program id when there is none. Signed by `Global.holder_reward_claim_authority`.
  - `amounts`: `{"vec":"u64"}`
- Visible signers: `holder_reward_claim_authority`
- Review indicators:
  - Program-like account `quote_token_program` has no fixed address in the IDL
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `holder_reward_claim_authority` — writable, signer
    - Relations: `global`
  - `mint` — read-only
  - `holder_rewards` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[104,111,108,100,101,114,45,114,101,119,97,114,100,115]},{"kind":"account","path":"mint"}]`
    - Documentation: deliver the collected fees here (lamports on a SOL quote)
  - `holder_rewards_token_account` — writable, optional
  - `quote_mint` — read-only
  - `quote_token_program` — read-only
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `extend_account`

- Arguments: **0**
- Documentation: Extends the size of program-owned accounts
- Visible signers: `user`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `account` — writable
  - `user` — writable, signer
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `get_minimum_distributable_fee`

- Arguments: **0**
- Documentation: Permissionless instruction to check the minimum required fees for distribution Returns the minimum required balance from the creator_vault and whether distribution can proceed
- Visible signers: **none**
- Review indicators:
  - No signer is visible in the IDL
- Accounts:
  - `mint` — read-only
    - Relations: `sharing_config`
  - `bonding_curve` — PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"kind":"account","path":"mint"}]`
  - `sharing_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[115,104,97,114,105,110,103,45,99,111,110,102,105,103]},{"kind":"account","path":"mint"}], program={"kind":"const","value":[12,53,255,169,5,90,142,86,141,168,247,188,7,86,21,39,76,241,201,44,164,31,64,0,156,81,106,164,20,194,124,112]}`
  - `creator_vault` — PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,45,118,97,117,108,116]},{"account":"BondingCurve","kind":"account","path":"bonding_curve.creator"}]`

### `init_user_volume_accumulator`

- Arguments: **0**
- Visible signers: `payer`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `payer` — writable, signer
  - `user` — read-only
  - `user_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[117,115,101,114,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]},{"kind":"account","path":"user"}]`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `initialize`

- Arguments: **0**
- Documentation: Creates the global state.
- Visible signers: `user`
- Review indicators:
  - _none from IDL metadata_
- Accounts:
  - `global` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `user` — writable, signer
  - `system_program` — fixed `11111111111111111111111111111111`

### `initialize_quote_control`

- Arguments: **0**
- Visible signers: `user`
- Review indicators:
  - _none from IDL metadata_
- Accounts:
  - `quote_control` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[113,117,111,116,101,45,99,111,110,116,114,111,108]}]`
  - `user` — writable, signer
  - `system_program` — fixed `11111111111111111111111111111111`

### `migrate`

- Arguments: **0**
- Documentation: Migrates liquidity to pump_amm if the bonding curve is complete
- Visible signers: `user`
- Review indicators:
  - _none from IDL metadata_
- Accounts:
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `withdraw_authority` — writable
    - Relations: `global`
  - `mint` — read-only
  - `bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"kind":"account","path":"mint"}]`
  - `associated_bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"bonding_curve"},{"kind":"account","path":"mint"},{"kind":"account","path":"mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `user` — writable, signer
  - `system_program` — fixed `11111111111111111111111111111111`
  - `token_program` — fixed `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`
  - `pump_amm` — fixed `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA`
  - `pool` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[112,111,111,108]},{"kind":"const","value":[0,0]},{"kind":"account","path":"pool_authority"},{"kind":"account","path":"mint"},{"kind":"account","path":"wsol_mint"}], program={"kind":"account","path":"pump_amm"}`
  - `pool_authority` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[112,111,111,108,45,97,117,116,104,111,114,105,116,121]},{"kind":"account","path":"mint"}]`
  - `pool_authority_mint_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"pool_authority"},{"kind":"account","path":"mint"},{"kind":"account","path":"mint"}], program={"kind":"account","path":"associated_token_program"}`
  - `pool_authority_wsol_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"pool_authority"},{"kind":"account","path":"token_program"},{"kind":"account","path":"wsol_mint"}], program={"kind":"account","path":"associated_token_program"}`
  - `amm_global_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108,95,99,111,110,102,105,103]}], program={"kind":"account","path":"pump_amm"}`
  - `wsol_mint` — fixed `So11111111111111111111111111111111111111112`
  - `lp_mint` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[112,111,111,108,95,108,112,95,109,105,110,116]},{"kind":"account","path":"pool"}], program={"kind":"account","path":"pump_amm"}`
  - `user_pool_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"pool_authority"},{"kind":"account","path":"token_2022_program"},{"kind":"account","path":"lp_mint"}], program={"kind":"account","path":"associated_token_program"}`
  - `pool_base_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"pool"},{"kind":"account","path":"mint"},{"kind":"account","path":"mint"}], program={"kind":"account","path":"associated_token_program"}`
  - `pool_quote_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"pool"},{"kind":"account","path":"token_program"},{"kind":"account","path":"wsol_mint"}], program={"kind":"account","path":"associated_token_program"}`
  - `token_2022_program` — fixed `TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `pump_amm_event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}], program={"kind":"account","path":"pump_amm"}`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`
  - `rent` — fixed `SysvarRent111111111111111111111111111111111`

### `migrate_bonding_curve_creator`

- Arguments: **0**
- Visible signers: **none**
- Review indicators:
  - No signer is visible in the IDL
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `mint` — read-only
    - Relations: `sharing_config`
  - `bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"kind":"account","path":"mint"}]`
  - `sharing_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[115,104,97,114,105,110,103,45,99,111,110,102,105,103]},{"kind":"account","path":"mint"}], program={"kind":"const","value":[12,53,255,169,5,90,142,86,141,168,247,188,7,86,21,39,76,241,201,44,164,31,64,0,156,81,106,164,20,194,124,112]}`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `migrate_v2`

- Arguments: **0**
- Documentation: Migrates liquidity to pump_amm if the bonding curve is complete
- Visible signers: `user`
- Review indicators:
  - Program-like account `base_token_program` has no fixed address in the IDL
  - Program-like account `quote_token_program` has no fixed address in the IDL
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `withdraw_authority` — writable
    - Relations: `global`
  - `base_mint` — read-only
  - `quote_mint` — read-only
  - `bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"kind":"account","path":"base_mint"}]`
  - `associated_base_bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"bonding_curve"},{"kind":"account","path":"base_token_program"},{"kind":"account","path":"base_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `associated_quote_bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"bonding_curve"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"account","path":"associated_token_program"}`
  - `user` — writable, signer
  - `system_program` — fixed `11111111111111111111111111111111`
  - `pump_amm` — fixed `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA`
  - `pool` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[112,111,111,108]},{"kind":"const","value":[0,0]},{"kind":"account","path":"pool_authority"},{"kind":"account","path":"base_mint"},{"kind":"account","path":"quote_mint"}], program={"kind":"account","path":"pump_amm"}`
  - `pool_authority` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[112,111,111,108,45,97,117,116,104,111,114,105,116,121]},{"kind":"account","path":"base_mint"}]`
  - `pool_authority_mint_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"pool_authority"},{"kind":"account","path":"base_token_program"},{"kind":"account","path":"base_mint"}], program={"kind":"account","path":"associated_token_program"}`
  - `pool_authority_quote_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"pool_authority"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"account","path":"associated_token_program"}`
  - `amm_global_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108,95,99,111,110,102,105,103]}], program={"kind":"account","path":"pump_amm"}`
  - `lp_mint` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[112,111,111,108,95,108,112,95,109,105,110,116]},{"kind":"account","path":"pool"}], program={"kind":"account","path":"pump_amm"}`
  - `user_pool_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"pool_authority"},{"kind":"account","path":"token_2022_program"},{"kind":"account","path":"lp_mint"}], program={"kind":"account","path":"associated_token_program"}`
  - `pool_base_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"pool"},{"kind":"account","path":"base_token_program"},{"kind":"account","path":"base_mint"}], program={"kind":"account","path":"associated_token_program"}`
  - `pool_quote_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"pool"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"account","path":"associated_token_program"}`
  - `base_token_program` — read-only
  - `quote_token_program` — read-only
  - `token_2022_program` — fixed `TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `pump_amm_event_authority` — read-only
  - `rent` — fixed `SysvarRent111111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `remove_quote_control_mint`

- Arguments: **1**
  - `quote_mint`: `"pubkey"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `authority` — writable, signer
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `quote_control` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[113,117,111,116,101,45,99,111,110,116,114,111,108]}]`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `remove_quote_mint`

- Arguments: **1**
  - `quote_mint`: `"pubkey"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `global` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `authority` — writable, signer
    - Relations: `global`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `sell`

- Arguments: **2**
- Documentation: Sells tokens into a bonding curve. For cashback coins, pass as remaining_accounts: [0] user_volume_accumulator, [1] bonding_curve_v2. If provided and valid, creator_fee goes to user_volume_accumulator. Otherwise, falls back to transferring creator_fee to creator_vault.
  - `amount`: `"u64"`
  - `min_sol_output`: `"u64"`
- Visible signers: `user`
- Review indicators:
  - Program-like account `token_program` has no fixed address in the IDL
- Accounts:
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `fee_recipient` — writable
  - `mint` — read-only
  - `bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"kind":"account","path":"mint"}]`
  - `associated_bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"bonding_curve"},{"kind":"account","path":"token_program"},{"kind":"account","path":"mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `associated_user` — writable
  - `user` — writable, signer
  - `system_program` — fixed `11111111111111111111111111111111`
  - `creator_vault` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,45,118,97,117,108,116]},{"account":"BondingCurve","kind":"account","path":"bonding_curve.creator"}]`
  - `token_program` — read-only
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`
  - `fee_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,95,99,111,110,102,105,103]},{"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}], program={"kind":"account","path":"fee_program"}`
  - `fee_program` — fixed `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ`

### `sell_v2`

- Arguments: **2**
  - `amount`: `"u64"`
  - `min_sol_output`: `"u64"`
- Visible signers: `user`
- Review indicators:
  - Program-like account `base_token_program` has no fixed address in the IDL
  - Program-like account `quote_token_program` has no fixed address in the IDL
- Accounts:
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `base_mint` — read-only
  - `quote_mint` — read-only
  - `base_token_program` — read-only
  - `quote_token_program` — read-only
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `fee_recipient` — writable
  - `associated_quote_fee_recipient` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"fee_recipient"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `buyback_fee_recipient` — writable
  - `associated_quote_buyback_fee_recipient` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"buyback_fee_recipient"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"kind":"account","path":"base_mint"}]`
  - `associated_base_bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"bonding_curve"},{"kind":"account","path":"base_token_program"},{"kind":"account","path":"base_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `associated_quote_bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"bonding_curve"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `user` — writable, signer
  - `associated_base_user` — writable
  - `associated_quote_user` — writable
    - Documentation: canonical SPL associated-token PDA. Validated in `sell_v2_ix` via `validate_user_quote_token_account` for non-legacy mints; ignored for legacy (SOL) trades.
  - `creator_vault` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,45,118,97,117,108,116]},{"account":"BondingCurve","kind":"account","path":"bonding_curve.creator"}]`
  - `associated_creator_vault` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"creator_vault"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `sharing_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[115,104,97,114,105,110,103,45,99,111,110,102,105,103]},{"kind":"account","path":"base_mint"}], program={"kind":"const","value":[12,53,255,169,5,90,142,86,141,168,247,188,7,86,21,39,76,241,201,44,164,31,64,0,156,81,106,164,20,194,124,112]}`
    - Documentation: seeds; the account is intentionally not deserialized here because it may be uninitialized for mints that have not created a fee sharing config. Handlers must check `data_is_empty()` / owner before reading.
  - `user_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[117,115,101,114,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]},{"kind":"account","path":"user"}]`
  - `associated_user_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"user_volume_accumulator"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `fee_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,95,99,111,110,102,105,103]},{"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}], program={"kind":"account","path":"fee_program"}`
  - `fee_program` — fixed `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`

### `set_creator`

- Arguments: **1**
- Documentation: Allows Global::set_creator_authority to set the bonding curve creator from Metaplex metadata or input argument
  - `creator`: `"pubkey"`
- Visible signers: `set_creator_authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `set_creator_authority` — signer
    - Relations: `global`
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `mint` — read-only
  - `metadata` — PDA
    - PDA: `seeds=[{"kind":"const","value":[109,101,116,97,100,97,116,97]},{"kind":"const","value":[11,112,101,177,227,209,124,69,56,157,82,127,107,4,195,205,88,184,108,115,26,160,253,181,73,182,209,188,3,248,41,70]},{"kind":"account","path":"mint"}], program={"kind":"const","value":[11,112,101,177,227,209,124,69,56,157,82,127,107,4,195,205,88,184,108,115,26,160,253,181,73,182,209,188,3,248,41,70]}`
  - `bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"kind":"account","path":"mint"}]`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `set_mayhem_virtual_params`

- Arguments: **0**
- Visible signers: `sol_vault_authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `sol_vault_authority` — writable, signer, PDA
    - PDA: `seeds=[{"kind":"const","value":[115,111,108,45,118,97,117,108,116]}], program={"kind":"const","value":[5,42,229,215,167,218,167,36,166,234,176,167,41,84,145,133,90,212,160,103,22,96,103,76,78,3,69,89,128,61,101,163]}`
  - `mayhem_token_vault` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"sol_vault_authority"},{"kind":"account","path":"token_program"},{"kind":"account","path":"mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `mint` — read-only
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"kind":"account","path":"mint"}]`
  - `token_program` — fixed `TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `set_metaplex_creator`

- Arguments: **0**
- Documentation: Syncs the bonding curve creator with the Metaplex metadata creator if it exists
- Visible signers: **none**
- Review indicators:
  - No signer is visible in the IDL
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `mint` — read-only
  - `metadata` — PDA
    - PDA: `seeds=[{"kind":"const","value":[109,101,116,97,100,97,116,97]},{"kind":"const","value":[11,112,101,177,227,209,124,69,56,157,82,127,107,4,195,205,88,184,108,115,26,160,253,181,73,182,209,188,3,248,41,70]},{"kind":"account","path":"mint"}], program={"kind":"const","value":[11,112,101,177,227,209,124,69,56,157,82,127,107,4,195,205,88,184,108,115,26,160,253,181,73,182,209,188,3,248,41,70]}`
  - `bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"kind":"account","path":"mint"}]`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `set_params`

- Arguments: **11**
- Documentation: Sets the global state parameters.
  - `initial_virtual_token_reserves`: `"u64"`
  - `initial_virtual_sol_reserves`: `"u64"`
  - `initial_real_token_reserves`: `"u64"`
  - `token_total_supply`: `"u64"`
  - `fee_basis_points`: `"u64"`
  - `withdraw_authority`: `"pubkey"`
  - `enable_migrate`: `"bool"`
  - `pool_migration_fee`: `"u64"`
  - `creator_fee_basis_points`: `"u64"`
  - `set_creator_authority`: `"pubkey"`
  - `admin_set_creator_authority`: `"pubkey"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `global` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `authority` — writable, signer
    - Relations: `global`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `set_quote_control_admin`

- Arguments: **1**
  - `new_admin`: `"pubkey"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `authority` — signer
    - Relations: `global`
  - `quote_control` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[113,117,111,116,101,45,99,111,110,116,114,111,108]}]`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `set_reserved_fee_recipients`

- Arguments: **1**
  - `whitelist_pda`: `"pubkey"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `global` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `authority` — signer
    - Relations: `global`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `set_virtual_quote_reserves`

- Arguments: **1**
  - `initial_virtual_quote_reserves`: `"u64"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `global` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `authority` — writable, signer
    - Relations: `global`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `sync_user_volume_accumulator`

- Arguments: **0**
- Visible signers: **none**
- Review indicators:
  - No signer is visible in the IDL
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `user` — read-only
  - `global_volume_accumulator` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]}]`
  - `user_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[117,115,101,114,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]},{"kind":"account","path":"user"}]`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `toggle_cashback_enabled`

- Arguments: **1**
  - `enabled`: `"bool"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `global` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `authority` — writable, signer
    - Relations: `global`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `toggle_create_v2`

- Arguments: **1**
  - `enabled`: `"bool"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `global` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `authority` — writable, signer
    - Relations: `global`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `toggle_mayhem_mode`

- Arguments: **1**
  - `enabled`: `"bool"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `global` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `authority` — writable, signer
    - Relations: `global`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `update_buyback_config`

- Arguments: **1**
  - `buyback_basis_points`: `{"option":"u64"}`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `global` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `authority` — writable, signer
    - Relations: `global`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `update_creator_fee_config`

- Arguments: **2**
  - `creator_fee_configurable`: `"bool"`
  - `max_configurable_creator_fee_bps`: `"u64"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `global` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `authority` — writable, signer
    - Relations: `global`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `update_global_authority`

- Arguments: **0**
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `global` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `authority` — signer
    - Relations: `global`
  - `new_authority` — read-only
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `update_holder_reward_config`

- Arguments: **2**
  - `is_holder_reward_enabled`: `"bool"`
  - `holder_reward_claim_authority`: `"pubkey"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `global` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}]`
  - `authority` — writable, signer
    - Relations: `global`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

## `pump_fees.json`

### `admin_cto_sharing_config`

- Arguments: **1**
  - `new_admin`: `{"option":"pubkey"}`
- Visible signers: `pool_authority`, `authority`
- Review indicators:
  - _none from IDL metadata_
- Accounts:
  - `pool_authority` — signer, PDA
    - PDA: `seeds=[{"kind":"const","value":[112,111,111,108,45,97,117,116,104,111,114,105,116,121]},{"kind":"account","path":"mint"}], program={"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}`
  - `authority` — signer
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}], program={"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}`
  - `mint` — read-only
    - Relations: `sharing_config`
  - `sharing_config` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[115,104,97,114,105,110,103,45,99,111,110,102,105,103]},{"kind":"account","path":"mint"}]`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ`

### `claim_social_fee_pda`

- Arguments: **2**
  - `user_id`: `"string"`
  - `platform`: `"u8"`
- Visible signers: `social_claim_authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `recipient` — writable
  - `social_fee_pda` — writable
  - `fee_program_global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,45,112,114,111,103,114,97,109,45,103,108,111,98,97,108]}]`
  - `social_claim_authority` — signer
    - Relations: `fee_program_global`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `claim_social_fee_pda_v2`

- Arguments: **2**
  - `user_id`: `"string"`
  - `platform`: `"u8"`
- Visible signers: `social_claim_authority`
- Review indicators:
  - Program-like account `quote_token_program` has no fixed address in the IDL
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `recipient` — writable
  - `social_fee_pda` — writable
  - `quote_mint` — writable
    - Documentation: Quote mint for claim
  - `associated_social_fee_pda` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"social_fee_pda"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"account","path":"associated_token_program"}`
  - `associated_recipient` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"recipient"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"account","path":"associated_token_program"}`
  - `quote_token_program` — read-only
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `fee_program_global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,45,112,114,111,103,114,97,109,45,103,108,111,98,97,108]}]`
  - `social_claim_authority` — signer
    - Relations: `fee_program_global`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `crank_donation_fee_pda`

- Arguments: **0**
- Visible signers: `payer`
- Review indicators:
  - _none from IDL metadata_
- Accounts:
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ`
  - `payer` — writable, signer
    - Documentation: Pays rent when [`temp_wsol_token_account`] is created (`init_if_needed`); receives rent when it is closed after the relay CPI.
  - `system_program` — fixed `11111111111111111111111111111111`
  - `token_program` — fixed `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `rent` — fixed `SysvarRent111111111111111111111111111111111`
  - `fee_program_global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,45,112,114,111,103,114,97,109,45,103,108,111,98,97,108]}]`
  - `donation_fee_pda` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[100,111,110,97,116,105,111,110,45,102,101,101,45,112,100,97]},{"account":"DonationFeePda","kind":"account","path":"donation_fee_pda.base_mint"},{"account":"DonationFeePda","kind":"account","path":"donation_fee_pda.config_id"}]`
  - `quote_mint` — writable
    - Documentation: Quote mint from donation fee pda.
  - `donation_fee_pda_ata` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"donation_fee_pda"},{"kind":"const","value":[6,221,246,225,215,101,161,147,217,203,225,70,206,235,121,172,28,180,133,237,95,91,55,145,58,140,245,133,126,255,0,169]},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
    - Documentation: WSOL ATA owned by `donation_fee_pda`.
  - `donation_relay_program` — fixed `RLAYHr9TRFcKB2ubYQhspcnXiaGpaVzNQvHytt47RZu`
  - `donation_relay_event_authority` — read-only
  - `mint_whitelist` — read-only
  - `epoch_tracker` — writable
  - `debouncer` — writable
  - `debouncer_ata` — writable

### `create_donation_fee_pda`

- Arguments: **0**
- Visible signers: `payer`
- Review indicators:
  - _none from IDL metadata_
- Accounts:
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ`
  - `payer` — writable, signer
  - `system_program` — fixed `11111111111111111111111111111111`
  - `fee_program_global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,45,112,114,111,103,114,97,109,45,103,108,111,98,97,108]}]`
  - `donation_fee_pda` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[100,111,110,97,116,105,111,110,45,102,101,101,45,112,100,97]},{"kind":"account","path":"base_mint"},{"kind":"account","path":"config_id"}]`
  - `config_id` — read-only
    - Documentation: stored on the PDA, so distinct `config_id`s for the same `base_mint` derive distinct addresses.
  - `base_mint` — read-only
  - `bonding_curve` — PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"kind":"account","path":"base_mint"}], program={"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}`
  - `pool` — read-only
  - `sharing_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[115,104,97,114,105,110,103,45,99,111,110,102,105,103]},{"kind":"account","path":"base_mint"}]`
    - Documentation: (derived from `[SHARING_CONFIG_SEED, base_mint]`)

### `create_fee_sharing_config`

- Arguments: **0**
- Documentation: Create Fee Sharing Config
- Visible signers: `payer`
- Review indicators:
  - _none from IDL metadata_
- Accounts:
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ`
  - `payer` — writable, signer
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}], program={"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}`
  - `mint` — read-only
  - `sharing_config` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[115,104,97,114,105,110,103,45,99,111,110,102,105,103]},{"kind":"account","path":"mint"}]`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `bonding_curve` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"kind":"account","path":"mint"}], program={"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}`
  - `pump_program` — fixed `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`
  - `pump_event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}], program={"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}`
  - `pool` — writable, optional
  - `pump_amm_program` — optional, fixed `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA`
  - `pump_amm_event_authority` — optional, PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}], program={"kind":"const","value":[12,20,222,252,130,94,198,118,148,37,8,24,187,101,64,101,244,41,141,49,86,213,113,180,212,248,9,12,24,233,168,99]}`

### `create_social_fee_pda`

- Arguments: **2**
  - `user_id`: `"string"`
  - `platform`: `"u8"`
- Visible signers: `payer`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `payer` — writable, signer
  - `social_fee_pda` — writable
  - `system_program` — fixed `11111111111111111111111111111111`
  - `fee_program_global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,45,112,114,111,103,114,97,109,45,103,108,111,98,97,108]}]`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `extend_fee_config`

- Arguments: **0**
- Documentation: Realloc the fee_config PDA to [`FeeConfig::CURRENT_SIZE`] (signer pays rent delta).
- Visible signers: `user`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `fee_config` — writable
  - `user` — signer
  - `config_program_id` — read-only
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `get_fees`

- Arguments: **4**
- Documentation: Get Fees
  - `is_pump_pool`: `"bool"`
  - `market_cap_lamports`: `"u128"`
  - `trade_size_lamports`: `"u64"`
  - `is_new_quote_mint`: `{"defined":{"name":"OptionBool"}}`
- Visible signers: **none**
- Review indicators:
  - No signer is visible in the IDL
- Accounts:
  - `fee_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,95,99,111,110,102,105,103]},{"kind":"account","path":"config_program_id"}]`
  - `config_program_id` — read-only

### `get_fees_with_quote_mint`

- Arguments: **3**
  - `is_pump_pool`: `"bool"`
  - `market_cap_lamports`: `"u128"`
  - `quote_mint`: `"pubkey"`
- Visible signers: **none**
- Review indicators:
  - No signer is visible in the IDL
- Accounts:
  - `fee_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,95,99,111,110,102,105,103]},{"kind":"account","path":"config_program_id"}]`
  - `config_program_id` — read-only

### `initialize_buyback`

- Arguments: **1**
  - `index`: `"u8"`
- Visible signers: `payer`
- Review indicators:
  - Program-like account `token_program` has no fixed address in the IDL
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `payer` — writable, signer
  - `buyback_vault` — writable
  - `buyback_vault_ata` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"buyback_vault"},{"kind":"account","path":"token_program"},{"kind":"account","path":"mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `mint` — read-only
  - `token_program` — read-only
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `initialize_fee_config`

- Arguments: **0**
- Documentation: Initialize FeeConfig admin
- Visible signers: `admin`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `admin` — writable, signer, fixed `8LWu7QM2dGR1G8nKDHthckea57bkCzXyBTAKPJUBDHo8`
  - `fee_config` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,95,99,111,110,102,105,103]},{"kind":"account","path":"config_program_id"}]`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `config_program_id` — read-only
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `initialize_fee_program_global`

- Arguments: **3**
  - `social_claim_authority`: `"pubkey"`
  - `disable_flags`: `"u8"`
  - `claim_rate_limit`: `"u64"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `authority` — writable, signer
    - Relations: `pump_global`
  - `pump_global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}], program={"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}`
  - `fee_program_global` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,45,112,114,111,103,114,97,109,45,103,108,111,98,97,108]}]`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `revoke_fee_sharing_authority`

- Arguments: **0**
- Documentation: Revoke Fee Sharing Authority
- Visible signers: **none**
- Review indicators:
  - No signer is visible in the IDL
- Accounts:
  - _none declared_

### `set_authority`

- Arguments: **1**
  - `new_authority`: `"pubkey"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `authority` — writable, signer
    - Relations: `fee_program_global`
  - `fee_program_global` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,45,112,114,111,103,114,97,109,45,103,108,111,98,97,108]}]`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `set_claim_rate_limit`

- Arguments: **1**
  - `claim_rate_limit`: `"u64"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `authority` — writable, signer
    - Relations: `fee_program_global`
  - `fee_program_global` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,45,112,114,111,103,114,97,109,45,103,108,111,98,97,108]}]`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `set_disable_flags`

- Arguments: **1**
  - `disable_flags`: `"u8"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `authority` — writable, signer
    - Relations: `fee_program_global`
  - `fee_program_global` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,45,112,114,111,103,114,97,109,45,103,108,111,98,97,108]}]`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `set_exotic_flat_fees`

- Arguments: **1**
  - `exotic_flat_fees`: `{"defined":{"name":"Fees"}}`
- Visible signers: `admin`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `fee_config` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,95,99,111,110,102,105,103]},{"kind":"account","path":"config_program_id"}]`
  - `admin` — writable, signer
    - Relations: `fee_config`
  - `config_program_id` — read-only
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `set_social_claim_authority`

- Arguments: **1**
  - `social_claim_authority`: `"pubkey"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `authority` — writable, signer
    - Relations: `fee_program_global`
  - `fee_program_global` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,45,112,114,111,103,114,97,109,45,103,108,111,98,97,108]}]`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `sweep_buyback`

- Arguments: **1**
  - `index`: `"u8"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `token_program` has no fixed address in the IDL
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `destination` — writable
  - `authority` — writable, signer
    - Relations: `buyback_vault`
  - `buyback_vault` — writable
  - `buyback_vault_ata` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"buyback_vault"},{"kind":"account","path":"token_program"},{"kind":"account","path":"mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `destination_ata` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"destination"},{"kind":"account","path":"token_program"},{"kind":"account","path":"mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `mint` — read-only
  - `token_program` — read-only
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `transfer_fee_sharing_authority`

- Arguments: **0**
- Documentation: Transfer Fee Sharing Authority
- Visible signers: **none**
- Review indicators:
  - No signer is visible in the IDL
- Accounts:
  - _none declared_

### `update_admin`

- Arguments: **0**
- Documentation: Update admin (only callable by admin)
- Visible signers: `admin`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `admin` — signer
    - Relations: `fee_config`
  - `fee_config` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,95,99,111,110,102,105,103]},{"kind":"account","path":"config_program_id"}]`
  - `new_admin` — read-only
  - `config_program_id` — read-only
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `update_buyback_authority`

- Arguments: **2**
  - `index`: `"u8"`
  - `new_authority`: `"pubkey"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `authority` — writable, signer
    - Relations: `fee_program_global`
  - `fee_program_global` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,45,112,114,111,103,114,97,109,45,103,108,111,98,97,108]}]`
  - `buyback_vault` — writable
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `update_buyback_claim_rate_limit`

- Arguments: **2**
  - `index`: `"u8"`
  - `claim_rate_limit`: `"i64"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `authority` — writable, signer
    - Relations: `fee_program_global`
  - `fee_program_global` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,45,112,114,111,103,114,97,109,45,103,108,111,98,97,108]}]`
  - `buyback_vault` — writable
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `update_fee_config`

- Arguments: **2**
- Documentation: Set/Replace fee parameters entirely (only callable by admin)
  - `fee_tiers`: `{"vec":{"defined":{"name":"FeeTier"}}}`
  - `flat_fees`: `{"defined":{"name":"Fees"}}`
- Visible signers: `admin`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `fee_config` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,95,99,111,110,102,105,103]},{"kind":"account","path":"config_program_id"}]`
  - `admin` — signer
    - Relations: `fee_config`
  - `config_program_id` — read-only
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `update_fee_shares`

- Arguments: **1**
- Documentation: Update Fee Shares, make sure to distribute all the fees before calling this
  - `shareholders`: `{"vec":{"defined":{"name":"Shareholder"}}}`
- Visible signers: `authority`
- Review indicators:
  - _none from IDL metadata_
- Accounts:
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ`
  - `authority` — signer
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}], program={"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}`
  - `mint` — read-only
    - Relations: `sharing_config`
  - `sharing_config` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[115,104,97,114,105,110,103,45,99,111,110,102,105,103]},{"kind":"account","path":"mint"}]`
  - `bonding_curve` — PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"kind":"account","path":"mint"}], program={"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}`
  - `pump_creator_vault` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,45,118,97,117,108,116]},{"kind":"account","path":"sharing_config"}], program={"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `pump_program` — fixed `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`
  - `pump_event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}], program={"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}`
  - `pump_amm_program` — fixed `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA`
  - `amm_event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}], program={"kind":"const","value":[12,20,222,252,130,94,198,118,148,37,8,24,187,101,64,101,244,41,141,49,86,213,113,180,212,248,9,12,24,233,168,99]}`
  - `wsol_mint` — fixed `So11111111111111111111111111111111111111112`
  - `token_program` — fixed `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `coin_creator_vault_authority` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,95,118,97,117,108,116]},{"kind":"account","path":"sharing_config"}], program={"kind":"const","value":[12,20,222,252,130,94,198,118,148,37,8,24,187,101,64,101,244,41,141,49,86,213,113,180,212,248,9,12,24,233,168,99]}`
  - `coin_creator_vault_ata` — writable

### `update_fee_shares_v2`

- Arguments: **1**
- Documentation: Update Fee Shares, make sure to distribute all the fees before calling this
  - `shareholders`: `{"vec":{"defined":{"name":"Shareholder"}}}`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `token_program` has no fixed address in the IDL
- Accounts:
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ`
  - `authority` — writable, signer
  - `global` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108]}], program={"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}`
  - `mint` — read-only
    - Relations: `sharing_config`
  - `sharing_config` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[115,104,97,114,105,110,103,45,99,111,110,102,105,103]},{"kind":"account","path":"mint"}]`
  - `bonding_curve` — PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"kind":"account","path":"mint"}], program={"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}`
  - `pump_creator_vault` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,45,118,97,117,108,116]},{"kind":"account","path":"sharing_config"}], program={"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}`
  - `pump_creator_vault_ata` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"pump_creator_vault"},{"kind":"account","path":"token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"account","path":"associated_token_program"}`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `pump_program` — fixed `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`
  - `pump_event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}], program={"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}`
  - `pump_amm_program` — fixed `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA`
  - `amm_event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}], program={"kind":"const","value":[12,20,222,252,130,94,198,118,148,37,8,24,187,101,64,101,244,41,141,49,86,213,113,180,212,248,9,12,24,233,168,99]}`
  - `quote_mint` — read-only
  - `token_program` — read-only
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `coin_creator_vault_authority` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,95,118,97,117,108,116]},{"kind":"account","path":"sharing_config"}], program={"kind":"const","value":[12,20,222,252,130,94,198,118,148,37,8,24,187,101,64,101,244,41,141,49,86,213,113,180,212,248,9,12,24,233,168,99]}`
  - `coin_creator_vault_ata` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"coin_creator_vault_authority"},{"kind":"account","path":"token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"account","path":"associated_token_program"}`

### `update_stable_fee_config`

- Arguments: **1**
- Documentation: Set/Replace fee parameters entirely (only callable by admin)
  - `fee_tiers`: `{"vec":{"defined":{"name":"FeeTier"}}}`
- Visible signers: `admin`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `fee_config` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,95,99,111,110,102,105,103]},{"kind":"account","path":"config_program_id"}]`
  - `admin` — signer
    - Relations: `fee_config`
  - `config_program_id` — read-only
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `upsert_fee_tiers`

- Arguments: **2**
- Documentation: Update or expand fee tiers (only callable by admin)
  - `fee_tiers`: `{"vec":{"defined":{"name":"FeeTier"}}}`
  - `offset`: `"u8"`
- Visible signers: `admin`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `fee_config` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,95,99,111,110,102,105,103]},{"kind":"account","path":"config_program_id"}]`
  - `admin` — signer
    - Relations: `fee_config`
  - `config_program_id` — read-only
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `upsert_stable_fee_tiers`

- Arguments: **2**
- Documentation: Update or expand fee tiers (only callable by admin)
  - `fee_tiers`: `{"vec":{"defined":{"name":"FeeTier"}}}`
  - `offset`: `"u8"`
- Visible signers: `admin`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `fee_config` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,95,99,111,110,102,105,103]},{"kind":"account","path":"config_program_id"}]`
  - `admin` — signer
    - Relations: `fee_config`
  - `config_program_id` — read-only
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

## `pump_amm.json`

### `admin_cto_pool`

- Arguments: **3**
  - `coin_creator`: `"pubkey"`
  - `is_holder_reward`: `"bool"`
  - `creator_fee_bps`: `{"option":"u64"}`
- Visible signers: `payer`, `pool_authority`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `payer` — writable, signer
  - `global_config` — read-only
  - `pool` — writable
  - `pool_authority` — signer, PDA
    - PDA: `seeds=[{"kind":"const","value":[112,111,111,108,45,97,117,116,104,111,114,105,116,121]},{"account":"Pool","kind":"account","path":"pool.base_mint"}], program={"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `admin_update_token_incentives`

- Arguments: **5**
  - `start_time`: `"i64"`
  - `end_time`: `"i64"`
  - `seconds_in_a_day`: `"i64"`
  - `day_number`: `"u64"`
  - `token_supply_per_day`: `"u64"`
- Visible signers: `admin`
- Review indicators:
  - Program-like account `token_program` has no fixed address in the IDL
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `admin` — writable, signer
    - Relations: `global_config`
  - `global_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108,95,99,111,110,102,105,103]}]`
  - `global_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]}]`
  - `mint` — read-only
  - `global_incentive_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"global_volume_accumulator"},{"kind":"account","path":"token_program"},{"kind":"account","path":"mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `token_program` — read-only
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `boost_buy_and_burn`

- Arguments: **2**
  - `quote_amount_in`: `"u64"`
  - `min_base_amount_burned`: `"u64"`
- Visible signers: `authority`
- Review indicators:
  - Program-like account `base_token_program` has no fixed address in the IDL
  - Program-like account `quote_token_program` has no fixed address in the IDL
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `pool` — read-only
  - `authority` — writable, signer
  - `global_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108,95,99,111,110,102,105,103]}]`
  - `base_mint` — writable
    - Relations: `pool`
  - `quote_mint` — read-only
    - Relations: `pool`
  - `pool_base_token_account` — writable
    - Relations: `pool`
  - `pool_quote_token_account` — writable
    - Relations: `pool`
  - `boost_vault_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,111,115,116,95,118,97,117,108,116]},{"kind":"account","path":"pool"}]`
  - `boost_vault` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"boost_vault_authority"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `base_token_program` — read-only
  - `quote_token_program` — read-only
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `buy`

- Arguments: **3**
- Documentation: For cashback coins, optionally pass user_volume_accumulator_wsol_ata as remaining_accounts[0]. If provided and valid, the ATA will be initialized if needed.
  - `base_amount_out`: `"u64"`
  - `max_quote_amount_in`: `"u64"`
  - `track_volume`: `{"defined":{"name":"OptionBool"}}`
- Visible signers: `user`
- Review indicators:
  - Program-like account `base_token_program` has no fixed address in the IDL
  - Program-like account `quote_token_program` has no fixed address in the IDL
- Accounts:
  - `pool` — writable
  - `user` — writable, signer
  - `global_config` — read-only
  - `base_mint` — read-only
    - Relations: `pool`
  - `quote_mint` — read-only
    - Relations: `pool`
  - `user_base_token_account` — writable
  - `user_quote_token_account` — writable
  - `pool_base_token_account` — writable
    - Relations: `pool`
  - `pool_quote_token_account` — writable
    - Relations: `pool`
  - `protocol_fee_recipient` — read-only
  - `protocol_fee_recipient_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"protocol_fee_recipient"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `base_token_program` — read-only
  - `quote_token_program` — read-only
  - `system_program` — fixed `11111111111111111111111111111111`
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA`
  - `coin_creator_vault_ata` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"coin_creator_vault_authority"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `coin_creator_vault_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,95,118,97,117,108,116]},{"account":"Pool","kind":"account","path":"pool.coin_creator"}]`
  - `global_volume_accumulator` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]}]`
  - `user_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[117,115,101,114,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]},{"kind":"account","path":"user"}]`
  - `fee_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,95,99,111,110,102,105,103]},{"kind":"const","value":[12,20,222,252,130,94,198,118,148,37,8,24,187,101,64,101,244,41,141,49,86,213,113,180,212,248,9,12,24,233,168,99]}], program={"kind":"account","path":"fee_program"}`
  - `fee_program` — fixed `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ`

### `buy_exact_quote_in`

- Arguments: **3**
- Documentation: Given a budget of spendable_quote_in, buy at least min_base_amount_out Fees will be deducted from spendable_quote_in f(quote) = tokens, where tokens >= min_base_amount_out Make sure the payer has enough SOL to cover creation of the following accounts (unless already created): - protocol_fee_recipient_token_account: rent.minimum_balance(TokenAccount::LEN) - coin_creator_vault_ata: rent.minimum_balance(TokenAccount::LEN) - user_volume_accumulator: rent.minimum_balance(UserVolumeAccumulator::LEN) For cashback coins, optionally pass user_volume_accumulator_wsol_ata as remaining_accounts[0]. If provided and valid, the ATA will be initialized if needed.
  - `spendable_quote_in`: `"u64"`
  - `min_base_amount_out`: `"u64"`
  - `track_volume`: `{"defined":{"name":"OptionBool"}}`
- Visible signers: `user`
- Review indicators:
  - Program-like account `base_token_program` has no fixed address in the IDL
  - Program-like account `quote_token_program` has no fixed address in the IDL
- Accounts:
  - `pool` — writable
  - `user` — writable, signer
  - `global_config` — read-only
  - `base_mint` — read-only
    - Relations: `pool`
  - `quote_mint` — read-only
    - Relations: `pool`
  - `user_base_token_account` — writable
  - `user_quote_token_account` — writable
  - `pool_base_token_account` — writable
    - Relations: `pool`
  - `pool_quote_token_account` — writable
    - Relations: `pool`
  - `protocol_fee_recipient` — read-only
  - `protocol_fee_recipient_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"protocol_fee_recipient"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `base_token_program` — read-only
  - `quote_token_program` — read-only
  - `system_program` — fixed `11111111111111111111111111111111`
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA`
  - `coin_creator_vault_ata` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"coin_creator_vault_authority"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `coin_creator_vault_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,95,118,97,117,108,116]},{"account":"Pool","kind":"account","path":"pool.coin_creator"}]`
  - `global_volume_accumulator` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]}]`
  - `user_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[117,115,101,114,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]},{"kind":"account","path":"user"}]`
  - `fee_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,95,99,111,110,102,105,103]},{"kind":"const","value":[12,20,222,252,130,94,198,118,148,37,8,24,187,101,64,101,244,41,141,49,86,213,113,180,212,248,9,12,24,233,168,99]}], program={"kind":"account","path":"fee_program"}`
  - `fee_program` — fixed `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ`

### `claim_cashback`

- Arguments: **0**
- Documentation: Pays out the user's accrued cashback. `user_wsol_token_account` may be any token account of `quote_mint` owned by `user`, not only the associated one.
- Visible signers: **none**
- Review indicators:
  - No signer is visible in the IDL
  - Program-like account `quote_token_program` has no fixed address in the IDL
- Accounts:
  - `user` — writable
  - `user_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[117,115,101,114,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]},{"kind":"account","path":"user"}]`
  - `quote_mint` — read-only
  - `quote_token_program` — read-only
  - `user_volume_accumulator_wsol_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"user_volume_accumulator"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `user_wsol_token_account` — writable
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA`

### `claim_token_incentives`

- Arguments: **0**
- Visible signers: `payer`
- Review indicators:
  - Program-like account `token_program` has no fixed address in the IDL
- Accounts:
  - `user` — read-only
  - `user_ata` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"user"},{"kind":"account","path":"token_program"},{"kind":"account","path":"mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `global_volume_accumulator` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]}]`
  - `global_incentive_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"global_volume_accumulator"},{"kind":"account","path":"token_program"},{"kind":"account","path":"mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `user_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[117,115,101,114,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]},{"kind":"account","path":"user"}]`
  - `mint` — read-only
    - Relations: `global_volume_accumulator`
  - `token_program` — read-only
  - `system_program` — fixed `11111111111111111111111111111111`
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA`
  - `payer` — writable, signer

### `close_user_volume_accumulator`

- Arguments: **0**
- Visible signers: `user`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `user` — writable, signer
  - `user_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[117,115,101,114,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]},{"kind":"account","path":"user"}]`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `collect_coin_creator_fee`

- Arguments: **0**
- Visible signers: **none**
- Review indicators:
  - No signer is visible in the IDL
  - Program-like account `quote_token_program` has no fixed address in the IDL
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `quote_mint` — read-only
  - `quote_token_program` — read-only
  - `coin_creator` — read-only
  - `coin_creator_vault_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,95,118,97,117,108,116]},{"kind":"account","path":"coin_creator"}]`
  - `coin_creator_vault_ata` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"coin_creator_vault_authority"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `coin_creator_token_account` — writable
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `create_config`

- Arguments: **5**
  - `lp_fee_basis_points`: `"u64"`
  - `protocol_fee_basis_points`: `"u64"`
  - `protocol_fee_recipients`: `{"array":["pubkey",8]}`
  - `coin_creator_fee_basis_points`: `"u64"`
  - `admin_set_coin_creator_authority`: `"pubkey"`
- Visible signers: `admin`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `admin` — writable, signer, fixed `8LWu7QM2dGR1G8nKDHthckea57bkCzXyBTAKPJUBDHo8`
  - `global_config` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108,95,99,111,110,102,105,103]}]`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `create_pool`

- Arguments: **9**
  - `index`: `"u16"`
  - `base_amount_in`: `"u64"`
  - `quote_amount_in`: `"u64"`
  - `coin_creator`: `"pubkey"`
  - `is_mayhem_mode`: `"bool"`
  - `is_cashback_coin`: `{"defined":{"name":"OptionBool"}}`
  - `creator_fee_bps`: `{"defined":{"name":"OptionU64"}}`
  - `can_edit_creator_fee`: `{"defined":{"name":"OptionBool"}}`
  - `is_holder_reward`: `{"defined":{"name":"OptionBool"}}`
- Visible signers: `creator`
- Review indicators:
  - Program-like account `base_token_program` has no fixed address in the IDL
  - Program-like account `quote_token_program` has no fixed address in the IDL
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `pool` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[112,111,111,108]},{"kind":"arg","path":"index"},{"kind":"account","path":"creator"},{"kind":"account","path":"base_mint"},{"kind":"account","path":"quote_mint"}]`
  - `global_config` — read-only
  - `creator` — writable, signer
  - `base_mint` — read-only
  - `quote_mint` — read-only
  - `lp_mint` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[112,111,111,108,95,108,112,95,109,105,110,116]},{"kind":"account","path":"pool"}]`
  - `user_base_token_account` — writable
  - `user_quote_token_account` — writable
  - `user_pool_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"creator"},{"kind":"account","path":"token_2022_program"},{"kind":"account","path":"lp_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `pool_base_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"pool"},{"kind":"account","path":"base_token_program"},{"kind":"account","path":"base_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `pool_quote_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"pool"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `token_2022_program` — fixed `TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`
  - `base_token_program` — read-only
  - `quote_token_program` — read-only
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `deposit`

- Arguments: **3**
  - `lp_token_amount_out`: `"u64"`
  - `max_base_amount_in`: `"u64"`
  - `max_quote_amount_in`: `"u64"`
- Visible signers: `user`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `pool` — writable
  - `global_config` — read-only
  - `user` — signer
  - `base_mint` — read-only
    - Relations: `pool`
  - `quote_mint` — read-only
    - Relations: `pool`
  - `lp_mint` — writable
    - Relations: `pool`
  - `user_base_token_account` — writable
  - `user_quote_token_account` — writable
  - `user_pool_token_account` — writable
  - `pool_base_token_account` — writable
    - Relations: `pool`
  - `pool_quote_token_account` — writable
    - Relations: `pool`
  - `token_program` — fixed `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`
  - `token_2022_program` — fixed `TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `disable`

- Arguments: **5**
  - `disable_create_pool`: `"bool"`
  - `disable_deposit`: `"bool"`
  - `disable_withdraw`: `"bool"`
  - `disable_buy`: `"bool"`
  - `disable_sell`: `"bool"`
- Visible signers: `admin`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `admin` — signer
    - Relations: `global_config`
  - `global_config` — writable
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `extend_account`

- Arguments: **0**
- Visible signers: `user`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `account` — writable
  - `user` — writable, signer
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `init_boost`

- Arguments: **0**
- Visible signers: `creator`
- Review indicators:
  - Program-like account `quote_token_program` has no fixed address in the IDL
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `pool` — writable
  - `global_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108,95,99,111,110,102,105,103]}]`
  - `creator` — writable, signer
  - `base_mint` — read-only
    - Relations: `pool`
  - `quote_mint` — read-only
    - Relations: `pool`
  - `pool_base_token_account` — read-only
    - Relations: `pool`
  - `pool_quote_token_account` — writable
    - Relations: `pool`
  - `boost_vault_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,111,115,116,95,118,97,117,108,116]},{"kind":"account","path":"pool"}]`
  - `boost_vault` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"boost_vault_authority"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `quote_token_program` — read-only
  - `system_program` — fixed `11111111111111111111111111111111`
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `init_user_volume_accumulator`

- Arguments: **0**
- Visible signers: `payer`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `payer` — writable, signer
  - `user` — read-only
  - `user_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[117,115,101,114,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]},{"kind":"account","path":"user"}]`
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `migrate_pool_coin_creator`

- Arguments: **0**
- Documentation: Migrate Pool Coin Creator to Sharing Config
- Visible signers: **none**
- Review indicators:
  - No signer is visible in the IDL
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `pool` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[112,111,111,108]},{"account":"Pool","kind":"account","path":"pool.index"},{"account":"Pool","kind":"account","path":"pool.creator"},{"account":"Pool","kind":"account","path":"pool.base_mint"},{"account":"Pool","kind":"account","path":"pool.quote_mint"}]`
  - `sharing_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[115,104,97,114,105,110,103,45,99,111,110,102,105,103]},{"account":"Pool","kind":"account","path":"pool.base_mint"}], program={"kind":"const","value":[12,53,255,169,5,90,142,86,141,168,247,188,7,86,21,39,76,241,201,44,164,31,64,0,156,81,106,164,20,194,124,112]}`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `sell`

- Arguments: **2**
  - `base_amount_in`: `"u64"`
  - `min_quote_amount_out`: `"u64"`
- Visible signers: `user`
- Review indicators:
  - Program-like account `base_token_program` has no fixed address in the IDL
  - Program-like account `quote_token_program` has no fixed address in the IDL
- Accounts:
  - `pool` — writable
  - `user` — writable, signer
  - `global_config` — read-only
  - `base_mint` — read-only
    - Relations: `pool`
  - `quote_mint` — read-only
    - Relations: `pool`
  - `user_base_token_account` — writable
  - `user_quote_token_account` — writable
  - `pool_base_token_account` — writable
    - Relations: `pool`
  - `pool_quote_token_account` — writable
    - Relations: `pool`
  - `protocol_fee_recipient` — read-only
  - `protocol_fee_recipient_token_account` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"protocol_fee_recipient"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `base_token_program` — read-only
  - `quote_token_program` — read-only
  - `system_program` — fixed `11111111111111111111111111111111`
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — fixed `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA`
  - `coin_creator_vault_ata` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"coin_creator_vault_authority"},{"kind":"account","path":"quote_token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `coin_creator_vault_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,95,118,97,117,108,116]},{"account":"Pool","kind":"account","path":"pool.coin_creator"}]`
  - `fee_config` — PDA
    - PDA: `seeds=[{"kind":"const","value":[102,101,101,95,99,111,110,102,105,103]},{"kind":"const","value":[12,20,222,252,130,94,198,118,148,37,8,24,187,101,64,101,244,41,141,49,86,213,113,180,212,248,9,12,24,233,168,99]}], program={"kind":"account","path":"fee_program"}`
  - `fee_program` — fixed `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ`

### `set_boost_authority`

- Arguments: **0**
- Visible signers: `admin`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `admin` — signer
    - Relations: `global_config`
  - `global_config` — writable
  - `boost_authority` — read-only
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `set_coin_creator`

- Arguments: **0**
- Documentation: Sets Pool::coin_creator from Metaplex metadata creator or BondingCurve::creator
- Visible signers: **none**
- Review indicators:
  - No signer is visible in the IDL
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `pool` — writable
  - `metadata` — PDA
    - PDA: `seeds=[{"kind":"const","value":[109,101,116,97,100,97,116,97]},{"kind":"const","value":[11,112,101,177,227,209,124,69,56,157,82,127,107,4,195,205,88,184,108,115,26,160,253,181,73,182,209,188,3,248,41,70]},{"account":"Pool","kind":"account","path":"pool.base_mint"}], program={"kind":"const","value":[11,112,101,177,227,209,124,69,56,157,82,127,107,4,195,205,88,184,108,115,26,160,253,181,73,182,209,188,3,248,41,70]}`
  - `bonding_curve` — PDA
    - PDA: `seeds=[{"kind":"const","value":[98,111,110,100,105,110,103,45,99,117,114,118,101]},{"account":"Pool","kind":"account","path":"pool.base_mint"}], program={"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `set_reserved_fee_recipients`

- Arguments: **1**
  - `whitelist_pda`: `"pubkey"`
- Visible signers: `admin`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `global_config` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108,95,99,111,110,102,105,103]}]`
  - `admin` — signer
    - Relations: `global_config`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `sync_user_volume_accumulator`

- Arguments: **0**
- Visible signers: **none**
- Review indicators:
  - No signer is visible in the IDL
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `user` — read-only
  - `global_volume_accumulator` — PDA
    - PDA: `seeds=[{"kind":"const","value":[103,108,111,98,97,108,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]}]`
  - `user_volume_accumulator` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[117,115,101,114,95,118,111,108,117,109,101,95,97,99,99,117,109,117,108,97,116,111,114]},{"kind":"account","path":"user"}]`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `toggle_boost`

- Arguments: **1**
  - `enabled`: `"bool"`
- Visible signers: `admin`
- Review indicators:
  - _none from IDL metadata_
- Accounts:
  - `admin` — signer
    - Relations: `global_config`
  - `global_config` — writable

### `toggle_cashback_enabled`

- Arguments: **1**
  - `enabled`: `"bool"`
- Visible signers: `admin`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `admin` — signer
    - Relations: `global_config`
  - `global_config` — writable
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `toggle_mayhem_mode`

- Arguments: **1**
  - `enabled`: `"bool"`
- Visible signers: `admin`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `admin` — signer
    - Relations: `global_config`
  - `global_config` — writable
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `transfer_creator_fees_to_pump`

- Arguments: **0**
- Documentation: Transfer creator fees to pump creator vault If coin creator fees are currently below rent.minimum_balance(TokenAccount::LEN) The transfer will be skipped
- Visible signers: **none**
- Review indicators:
  - No signer is visible in the IDL
  - Program-like account `token_program` has no fixed address in the IDL
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `wsol_mint` — read-only
    - Documentation: Pump Canonical Pool are quoted in wSOL
  - `token_program` — read-only
  - `system_program` — fixed `11111111111111111111111111111111`
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `coin_creator` — read-only
  - `coin_creator_vault_authority` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,95,118,97,117,108,116]},{"kind":"account","path":"coin_creator"}]`
  - `coin_creator_vault_ata` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"coin_creator_vault_authority"},{"kind":"account","path":"token_program"},{"kind":"account","path":"wsol_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `pump_creator_vault` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,45,118,97,117,108,116]},{"kind":"account","path":"coin_creator"}], program={"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `transfer_creator_fees_to_pump_v2`

- Arguments: **0**
- Visible signers: `payer`
- Review indicators:
  - Program-like account `token_program` has no fixed address in the IDL
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `payer` — writable, signer
  - `quote_mint` — read-only
  - `token_program` — read-only
  - `system_program` — fixed `11111111111111111111111111111111`
  - `associated_token_program` — fixed `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL`
  - `coin_creator` — read-only
  - `coin_creator_vault_authority` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,95,118,97,117,108,116]},{"kind":"account","path":"coin_creator"}]`
  - `coin_creator_vault_ata` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"coin_creator_vault_authority"},{"kind":"account","path":"token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"const","value":[140,151,37,143,78,36,137,241,187,61,16,41,20,142,13,131,11,90,19,153,218,255,16,132,4,142,123,216,219,233,248,89]}`
  - `pump_creator_vault` — writable, PDA
    - PDA: `seeds=[{"kind":"const","value":[99,114,101,97,116,111,114,45,118,97,117,108,116]},{"kind":"account","path":"coin_creator"}], program={"kind":"const","value":[1,86,224,246,147,102,90,207,68,219,21,104,191,23,91,170,81,137,203,151,245,210,255,59,101,93,43,182,253,109,24,176]}`
  - `pump_creator_vault_ata` — writable, PDA
    - PDA: `seeds=[{"kind":"account","path":"pump_creator_vault"},{"kind":"account","path":"token_program"},{"kind":"account","path":"quote_mint"}], program={"kind":"account","path":"associated_token_program"}`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `update_admin`

- Arguments: **0**
- Visible signers: `admin`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `admin` — signer
    - Relations: `global_config`
  - `global_config` — writable
  - `new_admin` — read-only
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `update_buyback_config`

- Arguments: **1**
  - `buyback_basis_points`: `{"option":"u64"}`
- Visible signers: `admin`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `admin` — signer
    - Relations: `global_config`
  - `global_config` — writable
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `update_creator_fee_config`

- Arguments: **2**
  - `creator_fee_configurable`: `"bool"`
  - `max_configurable_creator_fee_bps`: `"u64"`
- Visible signers: `admin`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `admin` — writable, signer
    - Relations: `global_config`
  - `global_config` — writable
  - `system_program` — fixed `11111111111111111111111111111111`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `update_fee_config`

- Arguments: **5**
  - `lp_fee_basis_points`: `"u64"`
  - `protocol_fee_basis_points`: `"u64"`
  - `protocol_fee_recipients`: `{"array":["pubkey",8]}`
  - `coin_creator_fee_basis_points`: `"u64"`
  - `admin_set_coin_creator_authority`: `"pubkey"`
- Visible signers: `admin`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `admin` — signer
    - Relations: `global_config`
  - `global_config` — writable
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only

### `withdraw`

- Arguments: **3**
  - `lp_token_amount_in`: `"u64"`
  - `min_base_amount_out`: `"u64"`
  - `min_quote_amount_out`: `"u64"`
- Visible signers: `user`
- Review indicators:
  - Program-like account `program` has no fixed address in the IDL
- Accounts:
  - `pool` — writable
  - `global_config` — read-only
  - `user` — signer
  - `base_mint` — read-only
    - Relations: `pool`
  - `quote_mint` — read-only
    - Relations: `pool`
  - `lp_mint` — writable
    - Relations: `pool`
  - `user_base_token_account` — writable
  - `user_quote_token_account` — writable
  - `user_pool_token_account` — writable
  - `pool_base_token_account` — writable
    - Relations: `pool`
  - `pool_quote_token_account` — writable
    - Relations: `pool`
  - `token_program` — fixed `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA`
  - `token_2022_program` — fixed `TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`
  - `event_authority` — PDA
    - PDA: `seeds=[{"kind":"const","value":[95,95,101,118,101,110,116,95,97,117,116,104,111,114,105,116,121]}]`
  - `program` — read-only
