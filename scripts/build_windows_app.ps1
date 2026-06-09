$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\pip.exe" install -r requirements.txt
& ".\.venv\Scripts\pyinstaller.exe" --clean --noconfirm "packaging\rag_customer_service.spec"

Write-Host ""
Write-Host "Build complete:"
Write-Host "  $ProjectRoot\dist\RAGCustomerService\RAGCustomerService.exe"
