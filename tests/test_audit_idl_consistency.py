import unittest
from pathlib import Path

from scripts.audit_idl_consistency import analyze, analyze_instruction


class IdlConsistencyAuditTests(unittest.TestCase):
    def test_current_idls_have_three_legacy_migrate_seed_anomalies(self):
        result = analyze(Path("idl"))
        self.assertEqual(result["instructions_checked"], 109)
        self.assertEqual(
            result["finding_counts"],
            {"duplicate_ata_program_and_mint_seed": 3},
        )
        self.assertEqual(
            {finding["account"] for finding in result["findings"]},
            {
                "associated_bonding_curve",
                "pool_authority_mint_account",
                "pool_base_token_account",
            },
        )
        self.assertTrue(all(finding["instruction"] == "migrate" for finding in result["findings"]))

    def test_reports_missing_relation_and_pda_roots(self):
        instruction = {
            "name": "broken",
            "accounts": [
                {
                    "name": "vault",
                    "relations": ["missing_relation"],
                    "pda": {"seeds": [{"kind": "account", "path": "missing_seed.key"}]},
                }
            ],
        }
        kinds = {
            finding["kind"]
            for finding in analyze_instruction("fixture.json", instruction)
        }
        self.assertEqual(kinds, {"missing_relation_target", "missing_pda_path_root"})


if __name__ == "__main__":
    unittest.main()
