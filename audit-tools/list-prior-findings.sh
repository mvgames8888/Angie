#!/usr/bin/env bash
set -euo pipefail

# Produce a lightweight duplicate-checking index from PDF text and outline
# metadata. The extractor intentionally has no third-party dependencies.
repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
extractor="$repo_root/audit-tools/pdf-text.py"

find "$repo_root/agglayer-contracts-main/audits" \
     "$repo_root/vault-bridge-main/audit" \
     -type f -name '*.pdf' -print0 2>/dev/null |
while IFS= read -r -d '' report; do
    printf '\n== %s ==\n' "${report#"$repo_root/"}"
    {
        "$extractor" "$report"
        strings -n 8 "$report" |
            sed -n 's/.*<\/Title (\([^)]*\)).*/\1/p' |
            sed 's/\\(/(/g; s/\\)/)/g; s/\\\\/\\/g'
    } | awk '!seen[$0]++'
done
