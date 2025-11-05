#!/usr/bin/env bash
set -euo pipefail

if ! command -v toxiproxy-server >/dev/null 2>&1; then
  echo "toxiproxy-server not found. Install from https://github.com/Shopify/toxiproxy/releases"
  exit 1
fi

CONFIG="$(dirname "$0")/../../setup/mock_servers/toxiproxy.json"

echo "Starting toxiproxy-server with config ${CONFIG}"
nohup toxiproxy-server > toxiproxy.log 2>&1 &

sleep 2

if ! command -v toxiproxy-cli >/dev/null 2>&1; then
  echo "toxiproxy-cli not found. Install from https://github.com/Shopify/toxiproxy/releases"
  exit 0
fi

toxiproxy-cli delete bacen_api >/dev/null 2>&1 || true

toxiproxy-cli create bacen_api --listen 127.0.0.1:18080 --upstream api.bcb.gov.br:443

echo "Enable latency toxic with:"
echo "  toxiproxy-cli toxic add bacen_api --type latency --attribute latency=500 --attribute jitter=100"

echo "Enable packet loss simulation with:"
echo "  toxiproxy-cli toxic add bacen_api --type limit_data --attribute bytes=950"
