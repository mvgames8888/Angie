import unittest

from scripts.audit_quote_math import (
    budget_for_tokens,
    ceil_div,
    check_grid,
    quote_from_budget,
)


class QuoteMathAuditTests(unittest.TestCase):
    def test_ceil_div(self):
        self.assertEqual(ceil_div(0, 10), 0)
        self.assertEqual(ceil_div(10, 10), 1)
        self.assertEqual(ceil_div(11, 10), 2)
        with self.assertRaises(ValueError):
            ceil_div(1, 0)

    def test_reverse_quote_under_delivers_at_split_fee_boundary(self):
        budget = budget_for_tokens(7, 1, 1, 11, 23)
        quote = quote_from_budget(budget, 1, 1, 11, 23)
        self.assertEqual(quote["tokens_out"], 6)
        with_one_more = quote_from_budget(budget + 1, 1, 1, 11, 23)
        self.assertGreaterEqual(with_one_more["tokens_out"], 7)
        self.assertLessEqual(
            quote["net_sol"] + quote["protocol_fee"] + quote["creator_fee"],
            budget,
        )

    def test_zero_net_is_explicitly_outside_documented_formula_domain(self):
        with self.assertRaisesRegex(ValueError, "net_sol is zero"):
            quote_from_budget(0, 0, 0, 10, 10)

    def test_small_grid_invariants(self):
        result = check_grid(20)
        self.assertEqual(result["status"], "counterexample")
        self.assertGreater(result["cases_checked"], 10_000)
        self.assertEqual(result["maximum_net_adjustment"], 1)
        self.assertGreater(result["reverse_quote_under_delivery_cases"], 0)
        self.assertEqual(
            result["under_delivery_cases_fixed_by_one_more_budget_unit"],
            result["reverse_quote_under_delivery_cases"],
        )


if __name__ == "__main__":
    unittest.main()
