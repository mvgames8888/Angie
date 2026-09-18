import json
import tempfile
import unittest
from pathlib import Path

from scripts.candidate_vectors import generate_vectors, instruction_by_name


class CandidateVectorTests(unittest.TestCase):
    def test_generates_exact_candidate_account_indices(self):
        vectors = generate_vectors(Path("idl"))
        self.assertEqual(vectors["cluster"], "devnet")
        self.assertEqual(len(vectors["idls"]), 3)

        cashback = vectors["candidates"]["C-01"]
        self.assertEqual(cashback["program_address"], "pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA")
        index = cashback["mutation_indices"]["user_wsol_token_account"]
        self.assertEqual(cashback["accounts"][index]["name"], "user_wsol_token_account")
        self.assertTrue(cashback["accounts"][index]["writable"])
        self.assertFalse(cashback["accounts"][index]["signer"])

        donation = vectors["candidates"]["C-04"]
        self.assertEqual(
            set(donation["mutation_indices"]),
            {"mint_whitelist", "epoch_tracker", "debouncer", "debouncer_ata"},
        )

    def test_output_is_json_serializable_and_deterministic(self):
        first = generate_vectors(Path("idl"))
        second = generate_vectors(Path("idl"))
        self.assertEqual(first, second)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "vectors.json"
            path.write_text(json.dumps(first, sort_keys=True), encoding="utf-8")
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), second)

    def test_rejects_missing_or_duplicate_instruction(self):
        with self.assertRaisesRegex(ValueError, "exactly one"):
            instruction_by_name({"instructions": []}, "missing")
        duplicate = {"instructions": [{"name": "same"}, {"name": "same"}]}
        with self.assertRaisesRegex(ValueError, "found 2"):
            instruction_by_name(duplicate, "same")


if __name__ == "__main__":
    unittest.main()
