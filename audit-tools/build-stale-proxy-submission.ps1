[CmdletBinding()]
param(
    [string]$OutputPath = (Join-Path (Get-Location) "stale-proxied-token-admin-submission.zip")
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$stage = Join-Path ([System.IO.Path]::GetTempPath()) ("stale-proxy-submission-" + [guid]::NewGuid())

$files = @(
    "reports/stale-proxied-token-admin.md",
    "pocs/stale-proxied-token-admin/evm_poc.py",
    "pocs/stale-proxied-token-admin/poc.py",
    "agglayer-contracts-main.zip"
)

foreach ($relativePath in $files) {
    $source = Join-Path $repoRoot $relativePath
    if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
        throw "Required submission file is missing: $source"
    }
}

try {
    New-Item -ItemType Directory -Force -Path (Join-Path $stage "reports") | Out-Null
    New-Item -ItemType Directory -Force -Path (Join-Path $stage "pocs/stale-proxied-token-admin") | Out-Null

    foreach ($relativePath in $files) {
        $source = Join-Path $repoRoot $relativePath
        $destination = Join-Path $stage $relativePath
        Copy-Item -LiteralPath $source -Destination $destination
    }

    $outputDirectory = Split-Path -Parent $OutputPath
    if ($outputDirectory) {
        New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null
    }
    Remove-Item -LiteralPath $OutputPath -Force -ErrorAction SilentlyContinue
    Compress-Archive -Path (Join-Path $stage "*") -DestinationPath $OutputPath -CompressionLevel Optimal
    Write-Host "Created submission archive: $OutputPath"
}
finally {
    Remove-Item -LiteralPath $stage -Recurse -Force -ErrorAction SilentlyContinue
}
