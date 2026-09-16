# Local audit helpers

These helpers operate only on the source archives extracted in the repository;
they do not connect to an RPC endpoint.

```bash
./audit-tools/list-prior-findings.sh > /tmp/prior-findings.txt
./audit-tools/search-prior-findings.sh 'nullifier|double.spending'
python3 -m unittest audit-tools/test_pdf_text.py
```

`list-prior-findings.sh` is intentionally best-effort. It combines text found
in compressed PDF content streams with PDF outline titles because the bundled
reports use both representations. `search-prior-findings.sh` regenerates that
index in a temporary file and prints matching lines with context.

## Build the stale-proxy submission on Windows

The repository does not track the generated submission ZIP because Codex Cloud
cannot create a pull request containing a new binary file. From PowerShell at
the repository root, build the archive with the expected directory layout:

```powershell
powershell -ExecutionPolicy Bypass -File .\audit-tools\build-stale-proxy-submission.ps1
```
