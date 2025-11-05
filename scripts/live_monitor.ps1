# Live Log Monitoring Script
# Continuously monitors backend and frontend

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "LIVE LOG MONITORING STARTED" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Monitoring every 3 seconds..." -ForegroundColor Gray
Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""

while ($true) {
    $timestamp = Get-Date -Format "HH:mm:ss"
    Clear-Host
    
    Write-Host "=== LIVE MONITORING - $timestamp ===" -ForegroundColor Cyan
    Write-Host ""
    
    # Check Backend
    Write-Host "[BACKEND API]" -ForegroundColor Yellow
    try {
        $response = Invoke-WebRequest -Uri http://localhost:5000/health -UseBasicParsing -TimeoutSec 2
        $health = $response.Content | ConvertFrom-Json
        
        Write-Host "  Status: " -NoNewline
        Write-Host "$($health.status)" -ForegroundColor Green
        Write-Host "  Service: $($health.service)"
        Write-Host "  Version: $($health.version)"
        
        if ($health.services) {
            $healthyCount = 0
            $totalCount = ($health.services.PSObject.Properties).Count
            
            $health.services.PSObject.Properties | ForEach-Object {
                $serviceName = $_.Name
                $serviceStatus = $health.services.$serviceName.status
                
                if ($serviceStatus -eq 'healthy') {
                    $healthyCount++
                } else {
                    Write-Host "    WARNING: $serviceName - $serviceStatus" -ForegroundColor Yellow
                    if ($health.services.$serviceName.error) {
                        Write-Host "      Error: $($health.services.$serviceName.error)" -ForegroundColor Red
                    }
                }
            }
            
            Write-Host "  Services: $healthyCount/$totalCount healthy"
        }
        
        if ($health.external_apis) {
            $configuredCount = 0
            $totalApis = ($health.external_apis.PSObject.Properties).Count
            
            $health.external_apis.PSObject.Properties | ForEach-Object {
                $apiName = $_.Name
                $apiStatus = $health.external_apis.$apiName.status
                
                if ($apiStatus -match 'configured|healthy') {
                    $configuredCount++
                } else {
                    Write-Host "    WARNING: $apiName - $apiStatus" -ForegroundColor Yellow
                }
            }
            
            Write-Host "  External APIs: $configuredCount/$totalApis configured"
        }
    } catch {
        Write-Host "  Status: " -NoNewline
        Write-Host "OFFLINE" -ForegroundColor Red
        Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Write-Host ""
    
    # Check Frontend
    Write-Host "[FRONTEND]" -ForegroundColor Yellow
    $frontendFound = $false
    foreach ($port in @(3001, 3000)) {
        try {
            $null = Invoke-WebRequest -Uri "http://localhost:$port" -UseBasicParsing -TimeoutSec 1
            Write-Host "  Port $port: " -NoNewline
            Write-Host "RUNNING" -ForegroundColor Green
            $frontendFound = $true
            break
        } catch {
        }
    }
    
    if (-not $frontendFound) {
        Write-Host "  Status: " -NoNewline
        Write-Host "OFFLINE" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "Refreshing in 3 seconds... (Ctrl+C to stop)" -ForegroundColor Gray
    Write-Host ""
    
    Start-Sleep -Seconds 3
}







