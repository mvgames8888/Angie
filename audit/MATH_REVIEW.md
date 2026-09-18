# Documented quote-math review

## Scope

The Pump IDL publishes forward and reverse formulas for
`buy_exact_sol_in`. `scripts/audit_quote_math.py` implements those formulas as
unbounded Python integer arithmetic and checks two properties:

1. whether the reverse quote can produce a budget whose forward quote returns
   fewer tokens than requested; and
2. adjusted net SOL plus the separately rounded protocol and creator fees never
   exceeds the supplied budget.

This checks documentation consistency only. It cannot establish the integer
widths, checked operations, fee sources, reserve updates, or formulas used by
the deployed program.

## Result

An exhaustive grid through reserves of 64 units, all valid desired token
amounts, and seven representative protocol/creator fee splits checked 903,168
cases. It found 342,165 cases where the reverse formula's budget under-delivers
when passed back through the documented forward formula. The smallest example
uses virtual reserves `(1 SOL, 2 tokens)`, requests one token, and assigns one
basis point to each fee. The reverse quote returns a budget of three units; the
forward quote separately rounds both fees to one, reduces net SOL from two to
one, and returns zero tokens.

All counterexamples in this bounded grid met the budget-safety property and
delivered the requested amount after adding one budget unit. Thus the documented
reverse quote is internally inconsistent at split-fee rounding boundaries, but
the forward formula does not overspend the stated budget.

This is a **documentation/quoting candidate, not yet a security finding**. With
`min_tokens_out` set as documented, under-delivery should make the transaction
fail atomically. It becomes eligible only if the deployed behavior causes a
measurable unauthorized loss or exploitable repeated inefficiency rather than a
failed transaction or client-side inconvenience.

## Open runtime checks

- A zero budget produces `net_sol == 0`, after which the documented expression
  uses `net_sol - 1`. Verify that Devnet rejects this before subtraction and
  leaves all accounts unchanged. A clean rejection is not a finding.
- Repeat the model comparison at `u64` boundaries to establish whether the
  program promotes multiplication and addition to a wider checked type.
- Confirm that every fee charged by the deployed instruction is represented in
  `total_fee_bps`; in particular, determine whether buyback fees are a split of
  protocol fees or an additional component.
- Compare actual pre/post vault deltas and bonding-curve reserves rather than
  relying on return data or events.

Run the offline check with:

```bash
python3 scripts/audit_quote_math.py --limit 64
```
