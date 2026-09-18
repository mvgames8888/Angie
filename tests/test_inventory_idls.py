import json
import tempfile
import unittest
from io import BytesIO
from pathlib import Path

from scripts.inventory_idls import (
    EXPECTED_PROGRAMS,
    argument_summary,
    download_idls,
    inventory,
    pda_summary,
    review_indicators,
)


class FakeResponse(BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *_args):
        self.close()


class InventoryTests(unittest.TestCase):
    def payload(self, address: str) -> dict:
        return {
            "address": address,
            "instructions": [
                {
                    "name": "trade",
                    "accounts": [
                        {"name": "user", "signer": True, "writable": True},
                        {
                            "name": "pool",
                            "accounts": [
                                {"name": "vault", "isMut": True, "pda": {"seeds": []}}
                            ],
                        },
                    ],
                    "args": [{"name": "amount", "type": "u64"}],
                }
            ],
        }

    def write_idls(self, directory: Path) -> None:
        for filename, address in EXPECTED_PROGRAMS.items():
            (directory / filename).write_text(
                json.dumps(self.payload(address)), encoding="utf-8"
            )

    def test_inventory_supports_nested_accounts_and_schema_aliases(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.write_idls(directory)
            report = inventory(directory)
        self.assertIn("Visible signers: `user`", report)
        self.assertIn("`pool.vault` — writable, PDA", report)
        self.assertEqual(report.count("### `trade`"), 3)
        self.assertIn("Instructions inventoried: **3**", report)
        self.assertIn("Manual-review indicators: **0**", report)
        self.assertIn("`amount`: `\"u64\"`", report)
        self.assertIn("PDA: `seeds=[]`", report)
        self.assertEqual(report.count("SHA-256 `"), 3)

    def test_renders_complex_argument_and_pda_metadata_deterministically(self):
        self.assertEqual(
            argument_summary(
                [{"name": "params", "type": {"defined": {"name": "TradeParams"}}}]
            ),
            ['`params`: `{"defined":{"name":"TradeParams"}}`'],
        )
        self.assertEqual(
            pda_summary(
                {
                    "pda": {
                        "program": {"kind": "account", "path": "program"},
                        "seeds": [{"kind": "const", "value": [1, 2]}],
                    }
                }
            ),
            'seeds=[{"kind":"const","value":[1,2]}], '
            'program={"kind":"account","path":"program"}',
        )

    def test_flags_only_conservative_manual_review_indicators(self):
        accounts = [
            ("authority", {"signer": True, "optional": True}),
            ("token_program", {}),
            ("system_program", {"address": "11111111111111111111111111111111"}),
        ]
        self.assertEqual(
            review_indicators(accounts),
            [
                "Optional signer `authority`",
                "Program-like account `token_program` has no fixed address in the IDL",
            ],
        )

    def test_flags_instruction_without_visible_signer(self):
        self.assertEqual(
            review_indicators([("vault", {"writable": True})]),
            ["No signer is visible in the IDL"],
        )

    def test_rejects_missing_idl(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, "missing required IDL"):
                inventory(Path(temporary))

    def test_rejects_wrong_program_address(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.write_idls(directory)
            target = directory / "pump.json"
            payload = json.loads(target.read_text(encoding="utf-8"))
            payload["address"] = "attacker"
            target.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "expected program address"):
                inventory(directory)

    def test_downloads_and_validates_all_idls(self):
        requested = []

        def opener(request, timeout):
            self.assertEqual(timeout, 30)
            filename = request.full_url.rsplit("/", 1)[-1]
            requested.append(filename)
            return FakeResponse(json.dumps(self.payload(EXPECTED_PROGRAMS[filename])).encode())

        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary) / "idl"
            download_idls(directory, opener=opener)
            report = inventory(directory)
        self.assertEqual(requested, list(EXPECTED_PROGRAMS))
        self.assertEqual(report.count("### `trade`"), 3)

    def test_failed_download_does_not_replace_existing_idls(self):
        def opener(request, timeout):
            filename = request.full_url.rsplit("/", 1)[-1]
            address = EXPECTED_PROGRAMS[filename]
            if filename == "pump_amm.json":
                address = "wrong"
            return FakeResponse(json.dumps(self.payload(address)).encode())

        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.write_idls(directory)
            (directory / "pump.json").write_text(
                (directory / "pump.json").read_text(encoding="utf-8") + "\n",
                encoding="utf-8",
            )
            original = (directory / "pump.json").read_bytes()
            with self.assertRaisesRegex(ValueError, "expected program address"):
                download_idls(directory, opener=opener)
            self.assertEqual((directory / "pump.json").read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
