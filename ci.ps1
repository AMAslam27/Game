param(
    [ValidateSet("ci", "install", "lint", "format-check", "typecheck", "test", "format")]
    [string]$Task = "ci",

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ExtraArgs = @()
)

$ErrorActionPreference = "Stop"

if ($Task -eq "ci" -and $ExtraArgs.Count -gt 0) {
    throw "Choose a specific task when passing extra arguments."
}

# Run from the project root regardless of the current directory.
Push-Location $PSScriptRoot

try {
    $commands = @{
        "install"      = @("install")
        "lint"         = @("run", "ruff", "check", ".")
        "format-check" = @("run", "ruff", "format", "--check", ".")
        "typecheck"    = @("run", "mypy", ".")
        "test"         = @("run", "pytest")
        "format"       = @("run", "ruff", "format", ".")
    }

    $checks = if ($Task -eq "ci") {
        @("lint", "format-check", "typecheck", "test")
    } else {
        @($Task)
    }

    foreach ($check in $checks) {
        Write-Host "Running $check..."
        $commandArgs = $commands[$check]
        & poetry @commandArgs @ExtraArgs

        if ($LASTEXITCODE -ne 0) {
            exit $LASTEXITCODE
        }
    }
} finally {
    Pop-Location
}