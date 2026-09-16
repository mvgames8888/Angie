import base64
import io
import json
import tempfile
import unittest
from pathlib import Path

from scripts.capture_devnet import UPGRADEABLE_LOADER, base58_encode, capture
from scripts.inventory_idls import EXPECTED_PROGRAMS


class Response(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *_args):
        self.close()


class DevnetCaptureTests(unittest.TestCase):
    def test_base58_preserves_leading_zeroes(self):
        self.assertEqual(base58_encode(b"\0\0\x01"), "112")

    def test_captures_program_and_programdata_with_manifest(self):
        data_key = bytes(range(1, 33))
        program = (2).to_bytes(4, "little") + data_key
        programdata = b"program-data"
        calls = []

        def account(raw, executable):
            return {
                "context": {"slot": 100},
                "value": {
                    "data": [base64.b64encode(raw).decode(), "base64"],
                    "executable": executable,
                    "owner": UPGRADEABLE_LOADER,
                },
            }

        def opener(request, timeout):
            self.assertEqual(timeout, 30)
            body = json.loads(request.data)
            calls.append(body["method"])
            if body["method"] == "getGenesisHash":
                result = "devnet-genesis"
            elif body["method"] == "getSlot":
                result = 100
            elif body["params"][0] in EXPECTED_PROGRAMS.values():
                result = account(program, True)
            else:
                result = account(programdata, False)
            return Response(json.dumps({"jsonrpc": "2.0", "result": result}).encode())

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "evidence"
            manifest = capture(output, opener=opener)
            saved = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(saved, manifest)
            self.assertEqual(len(saved["programs"]), 3)
            self.assertEqual((output / "pump.programdata.bin").read_bytes(), programdata)
        self.assertEqual(calls.count("getAccountInfo"), 6)

    def test_rejects_non_executable_program(self):
        def opener(request, timeout):
            body = json.loads(request.data)
            if body["method"] == "getGenesisHash":
                result = "devnet-genesis"
            elif body["method"] == "getSlot":
                result = 1
            else:
                result = {
                    "context": {"slot": 1},
                    "value": {
                        "data": [base64.b64encode(b"bad").decode(), "base64"],
                        "executable": False,
                        "owner": UPGRADEABLE_LOADER,
                    },
                }
            return Response(json.dumps({"result": result}).encode())

        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, "not an executable"):
                capture(Path(temporary), opener=opener)


if __name__ == "__main__":
    unittest.main()
