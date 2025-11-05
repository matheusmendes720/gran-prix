param(
    [string]$PythonExecutable = "python"
)

$venvPath = Join-Path -Path (Get-Location) -ChildPath ".venv"

if (Test-Path $venvPath) {
    Write-Host "Virtual environment already exists at $venvPath" -ForegroundColor Yellow
    exit 0
}

Write-Host "Creating virtual environment in $venvPath" -ForegroundColor Cyan

$process = Start-Process -FilePath $PythonExecutable -ArgumentList "-m", "venv", ".venv" -NoNewWindow -PassThru -Wait

if ($process.ExitCode -ne 0) {
    Write-Host "Failed to create virtual environment (exit code $($process.ExitCode))" -ForegroundColor Red
    exit $process.ExitCode
}

Write-Host "Virtual environment created. Activate with:`n`n    .\\.venv\\Scripts\\Activate.ps1`n" -ForegroundColor Green
