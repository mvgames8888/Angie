import importlib.util
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile


POC_PATH = (
    Path(__file__).resolve().parents[1]
    / "pocs"
    / "max-withdraw-zero-liquidity"
    / "poc.py"
)
SPEC = importlib.util.spec_from_file_location("max_withdraw_poc", POC_PATH)
assert SPEC and SPEC.loader
poc = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(poc)

VULNERABLE_SOURCE = """
function _simulateWithdraw(uint256 assets) internal view returns (uint256) {
    uint256 maxWithdraw_ = $.yieldVault.maxWithdraw(address(this));
    Math.mulDiv(totalAssets, burnedYieldVaultShares, maxWithdraw_);
    return $.reservedAssets;
}
function withdraw(uint256 assets) external {}
"""


class MaxWithdrawZeroLiquidityTests(unittest.TestCase):
    def test_views_revert_but_reserve_withdrawal_succeeds(self):
        vault = poc.VaultModel(100, 100, 20, 0)
        with self.assertRaises(poc.DivisionByZero):
            vault.max_withdraw()
        with self.assertRaises(poc.DivisionByZero):
            vault.max_redeem()
        vault.withdraw_from_reserve(20)
        self.assertEqual((vault.owner_shares, vault.reserve, vault.supply), (80, 0, 80))

    def test_source_guard_rejects_fixed_implementation(self):
        fixed = VULNERABLE_SOURCE.replace(
            "Math.mulDiv", "if (maxWithdraw_ == 0) return $.reservedAssets;\nMath.mulDiv"
        )
        with self.assertRaisesRegex(poc.EvidenceError, "zero-liquidity guard"):
            poc.vulnerable_function(fixed)

    def test_reproduce_reads_supplied_archive(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with ZipFile(root / "vault-bridge-main.zip.txt", "w") as archive:
                archive.writestr(poc.SOURCE, VULNERABLE_SOURCE)
            poc.reproduce(root)

    def test_missing_evidence_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(poc.EvidenceError, "missing source evidence"):
                poc.reproduce(Path(temporary))


if __name__ == "__main__":
    unittest.main()
