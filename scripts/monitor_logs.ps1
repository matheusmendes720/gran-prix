# Live Log Monitoring Script
# Continuously monitors backend and frontend status

$ErrorActionPreference = "Continue"

while ($true) {
    Clear-Host
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "LIVE MONITORING - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Check Backend
    Write-Host "[BACKEND API]" -ForegroundColor Yellow
    try {
        $response = Invoke-WebRequest -Uri http://localhost:5000/health -UseBasicParsing -TimeoutSec 3
        $health = $response.Content | ConvertFrom-Json
        Write-Host "  Status: " -NoNewline
        Write-Host "RUNNING" -ForegroundColor Green
        Write-Host "  Service: $($health.service)"
        Write-Host "  Version: $($health.version)"
        if ($health.services) {
            $healthy = ($health.services | Get-Member -MemberType NoteProperty | Where-Object { $health.services.$($_.Name).status -eq 'healthy' }).Count
            Write-Host "  Services: $healthy/$($health.services.PSObject.Properties.Count) healthy"
        }
    } catch {
        Write-Host "  Status: " -NoNewline
        Write-Host "OFFLINE" -ForegroundColor Red
        Write-Host "  Error: $($_.Exception.Message)"
    }
    Write-Host ""
    
    # Check Frontend
    Write-Host "[FRONTEND]" -ForegroundColor Yellow
    $frontendRunning = $false
    foreach ($port in @(3001, 3000)) {
        try {
            $null = Invoke-WebRequest -Uri "http://localhost:$port" -UseBasicParsing -TimeoutSec 2
            Write-Host "  Port $port: " -NoNewline
            Write-Host "RUNNING" -ForegroundColor Green
            $frontendRunning = $true
            break
        } catch {
        }
    }
    if (-not $frontendRunning) {
        Write-Host "  Status: " -NoNewline
        Write-Host "OFFLINE" -ForegroundColor Red
    }
    Write-Host ""
    
    # Check Backend Logs (if process exists)
    Write-Host "[BACKEND LOGS]" -ForegroundColor Yellow
    $pythonProcs = Get-Process | Where-Object { $_.ProcessName -eq "python" -or $_.ProcessName -eq "pythonw" } | Select-Object -First 1
    if ($pythonProcs) {
        Write-Host "  Python process running (PID: $($pythonProcs.Id))" -ForegroundColor Green
    } else {
        Write-Host "  No Python process found" -ForegroundColor Red
    }
    Write-Host ""
    
    Write-Host "Refreshing in 5 seconds... (Press Ctrl+C to stop)" -ForegroundColor Gray
    Write-Host ""
    
    Start-Sleep -Seconds 5
}








