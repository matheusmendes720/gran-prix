param(
    [string]$ConfigPath = ""
)

function Ensure-ToxiProxyBinary {
    if (-not (Get-Command toxiproxy-server -ErrorAction SilentlyContinue)) {
        Write-Warning "toxiproxy-server not found. Download from https://github.com/Shopify/toxiproxy/releases"
        exit 1
    }
}

Ensure-ToxiProxyBinary

if (-not $ConfigPath) {
    $ConfigPath = Join-Path -Path (Split-Path -Parent $MyInvocation.MyCommand.Path) -ChildPath "..\..\setup\mock_servers\toxiproxy.json"
}

Write-Host "Launching toxiproxy-server (config: $ConfigPath)" -ForegroundColor Cyan
Start-Process -FilePath toxiproxy-server -NoNewWindow -RedirectStandardOutput "toxiproxy.log" -RedirectStandardError "toxiproxy.log"
Start-Sleep -Seconds 2

if (-not (Get-Command toxiproxy-cli -ErrorAction SilentlyContinue)) {
    Write-Warning "toxiproxy-cli not found. Install from https://github.com/Shopify/toxiproxy/releases"
    exit 0
}

toxiproxy-cli delete bacen_api 2>$null | Out-Null

toxiproxy-cli create bacen_api --listen 127.0.0.1:18080 --upstream api.bcb.gov.br:443

Write-Host "Enable latency toxic:"
Write-Host "  toxiproxy-cli toxic add bacen_api --type latency --attribute latency=500 --attribute jitter=100"

Write-Host "Enable packet loss simulation:"
Write-Host "  toxiproxy-cli toxic add bacen_api --type limit_data --attribute bytes=950"
