# Backend Log Monitoring Script
# Monitors backend console output for errors

$ErrorActionPreference = "Continue"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "BACKEND LOG MONITORING" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Monitoring backend logs for errors..." -ForegroundColor Yellow
Write-Host "Checking http://localhost:5000/health every 3 seconds..." -ForegroundColor Gray
Write-Host ""

$errorCount = 0
$lastError = $null

while ($true) {
    $timestamp = Get-Date -Format "HH:mm:ss"
    
    try {
        $response = Invoke-WebRequest -Uri http://localhost:5000/health -UseBasicParsing -TimeoutSec 3
        
        if ($response.StatusCode -eq 200) {
            $health = $response.Content | ConvertFrom-Json
            
            # Check for degraded/unhealthy status
            if ($health.status -ne "healthy") {
                Write-Host "[$timestamp] " -NoNewline -ForegroundColor Yellow
                Write-Host "WARNING: Status is $($health.status)" -ForegroundColor Yellow
            } else {
                Write-Host "[$timestamp] " -NoNewline -ForegroundColor Green
                Write-Host "OK - Backend healthy" -ForegroundColor Green
            }
            
            # Check for errors in services
            if ($health.services) {
                foreach ($service in $health.services.PSObject.Properties) {
                    if ($service.Value.status -ne "healthy") {
                        Write-Host "[$timestamp] " -NoNewline -ForegroundColor Red
                        Write-Host "ERROR: $($service.Name) - $($service.Value.status)" -ForegroundColor Red
                        if ($service.Value.error) {
                            Write-Host "  Details: $($service.Value.error)" -ForegroundColor Red
                        }
                    }
                }
            }
        }
    } catch {
        $errorCount++
        $lastError = $_.Exception.Message
        
        Write-Host "[$timestamp] " -NoNewline -ForegroundColor Red
        Write-Host "ERROR: Backend offline or unreachable" -ForegroundColor Red
        Write-Host "  Details: $lastError" -ForegroundColor Red
        Write-Host "  Error count: $errorCount" -ForegroundColor Red
    }
    
    Start-Sleep -Seconds 3
}








