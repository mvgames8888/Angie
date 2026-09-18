#!/usr/bin/env python3
"""Check invariants in the Pump buy_exact_sol_in formulas published in its IDL."""

import argparse
import json
from typing import Any


BPS_DENOMINATOR = 10_000


def ceil_div(numerator: int, denominator: int) -> int:
    if numerator < 0 or denominator <= 0:
        raise ValueError("ceil_div requires a non-negative numerator and positive denominator")
    return (numerator + denominator - 1) // denominator


def quote_from_budget(
    budget: int,
    protocol_fee_bps: int,
    creator_fee_bps: int,
    virtual_sol_reserves: int,
    virtual_token_reserves: int,
) -> dict[str, int]:
    """Apply the documented forward quote, retaining intermediates for auditing."""
    values = (
        budget,
        protocol_fee_bps,
        creator_fee_bps,
        virtual_sol_reserves,
        virtual_token_reserves,
    )
    if any(value < 0 for value in values) or min(
        virtual_sol_reserves, virtual_token_reserves
    ) == 0:
        raise ValueError("quote inputs and fees must be non-negative; reserves must be positive")
    total_fee_bps = protocol_fee_bps + creator_fee_bps
    net_before_adjustment = budget * BPS_DENOMINATOR // (
        BPS_DENOMINATOR + total_fee_bps
    )
    protocol_fee = ceil_div(net_before_adjustment * protocol_fee_bps, BPS_DENOMINATOR)
    creator_fee = ceil_div(net_before_adjustment * creator_fee_bps, BPS_DENOMINATOR)
    over_budget = max(0, net_before_adjustment + protocol_fee + creator_fee - budget)
    net_sol = net_before_adjustment - over_budget
    if net_sol < 1:
        raise ValueError("documented token quote is undefined when adjusted net_sol is zero")
    tokens_out = (net_sol - 1) * virtual_token_reserves // (
        virtual_sol_reserves + net_sol - 1
    )
    return {
        "net_before_adjustment": net_before_adjustment,
        "protocol_fee": protocol_fee,
        "creator_fee": creator_fee,
        "over_budget": over_budget,
        "net_sol": net_sol,
        "tokens_out": tokens_out,
    }


def budget_for_tokens(
    tokens: int,
    protocol_fee_bps: int,
    creator_fee_bps: int,
    virtual_sol_reserves: int,
    virtual_token_reserves: int,
) -> int:
    """Apply the reverse quote documented by Pump's buy_exact_sol_in IDL entry."""
    if not 0 < tokens < virtual_token_reserves:
        raise ValueError("tokens must be between zero and virtual_token_reserves")
    if min(protocol_fee_bps, creator_fee_bps) < 0 or virtual_sol_reserves <= 0:
        raise ValueError("fees must be non-negative and virtual_sol_reserves positive")
    net_sol = ceil_div(
        tokens * virtual_sol_reserves, virtual_token_reserves - tokens
    ) + 1
    return ceil_div(
        net_sol * (BPS_DENOMINATOR + protocol_fee_bps + creator_fee_bps),
        BPS_DENOMINATOR,
    )


def check_grid(limit: int) -> dict[str, Any]:
    """Exhaustively check small values plus representative fee boundaries."""
    if limit < 2:
        raise ValueError("limit must be at least 2")
    fee_splits = ((0, 0), (1, 0), (0, 1), (1, 1), (99, 1), (250, 250), (9999, 9999))
    checks = 0
    maximum_adjustment = 0
    under_delivery_cases = 0
    maximum_token_shortfall = 0
    fixed_by_one_more_unit = 0
    first_counterexample = None
    for virtual_sol in range(1, limit + 1):
        for virtual_tokens in range(2, limit + 1):
            for desired_tokens in range(1, virtual_tokens):
                for protocol_bps, creator_bps in fee_splits:
                    budget = budget_for_tokens(
                        desired_tokens,
                        protocol_bps,
                        creator_bps,
                        virtual_sol,
                        virtual_tokens,
                    )
                    quote = quote_from_budget(
                        budget,
                        protocol_bps,
                        creator_bps,
                        virtual_sol,
                        virtual_tokens,
                    )
                    if quote["tokens_out"] < desired_tokens:
                        under_delivery_cases += 1
                        maximum_token_shortfall = max(
                            maximum_token_shortfall,
                            desired_tokens - quote["tokens_out"],
                        )
                        if first_counterexample is None:
                            first_counterexample = {
                                "virtual_sol_reserves": virtual_sol,
                                "virtual_token_reserves": virtual_tokens,
                                "desired_tokens": desired_tokens,
                                "protocol_fee_bps": protocol_bps,
                                "creator_fee_bps": creator_bps,
                                "documented_budget": budget,
                                "tokens_out": quote["tokens_out"],
                            }
                        one_more = quote_from_budget(
                            budget + 1,
                            protocol_bps,
                            creator_bps,
                            virtual_sol,
                            virtual_tokens,
                        )
                        if one_more["tokens_out"] >= desired_tokens:
                            fixed_by_one_more_unit += 1
                    charged = quote["net_sol"] + quote["protocol_fee"] + quote["creator_fee"]
                    if charged > budget:
                        raise AssertionError(f"forward quote exceeds budget: {charged} > {budget}")
                    maximum_adjustment = max(maximum_adjustment, quote["over_budget"])
                    checks += 1
    return {
        "status": "counterexample" if under_delivery_cases else "pass",
        "grid_limit": limit,
        "cases_checked": checks,
        "maximum_net_adjustment": maximum_adjustment,
        "reverse_quote_under_delivery_cases": under_delivery_cases,
        "maximum_token_shortfall": maximum_token_shortfall,
        "under_delivery_cases_fixed_by_one_more_budget_unit": fixed_by_one_more_unit,
        "first_counterexample": first_counterexample,
        "scope": "documented IDL formulas only; not deployed bytecode",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=64)
    args = parser.parse_args()
    print(json.dumps(check_grid(args.limit), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
