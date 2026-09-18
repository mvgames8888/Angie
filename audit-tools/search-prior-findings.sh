#!/usr/bin/env bash
set -euo pipefail

if (($# != 1)); then
    printf 'usage: %s PATTERN\n' "${0##*/}" >&2
    exit 2
fi

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
index=$(mktemp)
trap 'rm -f "$index"' EXIT

"$repo_root/audit-tools/list-prior-findings.sh" >"$index"
rg --ignore-case --line-number --context 2 -- "$1" "$index"
