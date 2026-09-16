#!/usr/bin/env python3
import importlib.util
import tempfile
import unittest
import zlib
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("pdf-text.py")
SPEC = importlib.util.spec_from_file_location("pdf_text", MODULE_PATH)
assert SPEC and SPEC.loader
PDF_TEXT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PDF_TEXT)


class PdfTextTest(unittest.TestCase):
    def test_extracts_and_unescapes_compressed_text_objects(self):
        content = rb"BT (M-01 \(known\) finding) Tj ET"
        document = b"%PDF-1.4\nstream\n" + zlib.compress(content) + b"\nendstream\n%%EOF"

        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory, "report.pdf")
            report.write_bytes(document)
            self.assertEqual(list(PDF_TEXT.extract(report)), ["M-01 (known) finding"])

    def test_deduplicates_text(self):
        content = b"BT (same finding) Tj ET BT (same finding) Tj ET"
        document = b"%PDF-1.4\nstream\n" + content + b"\nendstream\n%%EOF"

        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory, "report.pdf")
            report.write_bytes(document)
            self.assertEqual(list(PDF_TEXT.extract(report)), ["same finding"])

    def test_ignores_stream_like_bytes_outside_content_streams(self):
        document = b"%PDF-1.4\nBT (compressed binary false positive) Tj ET\n%%EOF"

        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory, "report.pdf")
            report.write_bytes(document)
            self.assertEqual(list(PDF_TEXT.extract(report)), [])

    def test_preserves_non_utf8_literal_bytes(self):
        content = b"BT (finding \\351) Tj ET"
        document = b"%PDF-1.4\nstream\n" + content + b"\nendstream\n%%EOF"

        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory, "report.pdf")
            report.write_bytes(document)
            self.assertEqual(list(PDF_TEXT.extract(report)), ["finding é"])


if __name__ == "__main__":
    unittest.main()
