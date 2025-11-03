# 🚀 Deployment Guide

## Production Deployment Guide for Demand Forecasting System

### Quick Deployment Options

#### Option 1: Docker Compose (Recommended)
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### Option 2: Docker Single Container
```bash
# Build image
docker build -t forecasting-system .

# Run container
docker run -d \
  -p 8080:8080 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/reports:/app/reports \
  --name forecasting-dashboard \
  forecasting-system
```

#### Option 3: Direct Python
```bash
# Run on server
python scripts/web_dashboard_server.py --host 0.0.0.0 --port 8080
```

## Pre-Deployment Checklist

### 1. Run Deployment Helper
```bash
python scripts/deployment_helper.py

# Create .env file template
python scripts/deployment_helper.py --create-env
```

### 2. Check System Health
```bash
python scripts/monitor_system.py
```

### 3. Verify Dependencies
```bash
pip install -r requirements.txt
```

### 4. Test System
```bash
# Run test forecast
python scripts/run_all.py --item CONN-001

# Test API
python scripts/api_server.py --port 5000
curl http://localhost:5000/health
```

## Docker Deployment

### Build Image
```bash
docker build -t nova-corrente-forecasting .
```

### Run Services
```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d forecasting-dashboard

# View logs
docker-compose logs -f forecasting-dashboard
```

### Volumes
- `./data` - Data files
- `./models` - Trained models
- `./reports` - Generated reports
- `./logs` - System logs

## Environment Configuration

### Create .env File
```bash
cp .env.example .env
# Edit .env with your settings
```

### Required Variables
```env
API_HOST=0.0.0.0
API_PORT=5000
DASHBOARD_HOST=0.0.0.0
DASHBOARD_PORT=8080
```

## Production Deployment Steps

### 1. Server Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Clone/Upload Project
```bash
git clone <repository> /opt/forecasting-system
cd /opt/forecasting-system
```

### 3. Configure Environment
```bash
cp .env.example .env
nano .env  # Edit configuration
```

### 4. Build and Deploy
```bash
docker-compose build
docker-compose up -d
```

### 5. Verify Deployment
```bash
# Check health
curl http://localhost:8080/api/health

# Check logs
docker-compose logs
```

## Database Integration

### SQLite (Default)
```python
from scripts.database_integration import DatabaseManager

with DatabaseManager('sqlite') as db:
    db.save_forecast('ITEM-001', forecast_series)
    forecast = db.get_latest_forecast('ITEM-001')
```

### PostgreSQL
```python
conn_string = "dbname=forecasting user=postgres password=secret host=localhost"
with DatabaseManager('postgres', conn_string) as db:
    db.save_forecast('ITEM-001', forecast_series)
```

## Scheduled Tasks

### Cron Job (Linux)
```bash
# Edit crontab
crontab -e

# Add daily forecast at 6 AM
0 6 * * * cd /opt/forecasting-system && docker-compose exec scheduled-forecast python scripts/scheduled_forecast.py >> logs/cron.log 2>&1
```

### Docker Compose (Built-in)
The `scheduled-forecast` service runs automatically with `restart: unless-stopped`

## Monitoring

### System Health Checks
```bash
# Manual check
python scripts/monitor_system.py

# Continuous monitoring
python scripts/monitor_system.py --continuous
```

### Log Analysis
```bash
python scripts/log_analyzer.py
```

## Scaling

### Horizontal Scaling
```bash
# Scale dashboard service
docker-compose up -d --scale forecasting-dashboard=3
```

### Load Balancing
Use nginx or traefik as reverse proxy:
```nginx
upstream dashboard {
    server localhost:8080;
    server localhost:8081;
    server localhost:8082;
}

server {
    listen 80;
    location / {
        proxy_pass http://dashboard;
    }
}
```

## Backup

### Backup Strategy
```bash
# Backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf backup_$DATE.tar.gz data/ models/ reports/ logs/
```

### Automated Backups
```bash
# Add to crontab
0 2 * * * /opt/forecasting-system/backup.sh
```

## Security

### Firewall Configuration
```bash
# Allow only necessary ports
sudo ufw allow 8080/tcp
sudo ufw allow 5000/tcp
sudo ufw enable
```

### SSL/TLS Setup
Use nginx or traefik with Let's Encrypt certificates.

## Troubleshooting

### Container Won't Start
```bash
docker-compose logs forecasting-dashboard
docker-compose ps
```

### Port Already in Use
```bash
# Change ports in docker-compose.yml
ports:
  - "8081:8080"  # Use different external port
```

### Permission Issues
```bash
sudo chown -R $USER:$USER data/ models/ reports/ logs/
```

## Performance Optimization

### Resource Limits
```yaml
# In docker-compose.yml
services:
  forecasting-dashboard:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

### Database Optimization
- Use PostgreSQL for production
- Enable connection pooling
- Regular VACUUM and ANALYZE

## Production Checklist

- [ ] Dependencies installed
- [ ] Configuration files set
- [ ] Database configured
- [ ] Docker images built
- [ ] Services running
- [ ] Health checks passing
- [ ] Logs accessible
- [ ] Backups configured
- [ ] Monitoring active
- [ ] Security hardened
- [ ] SSL/TLS configured
- [ ] Firewall rules set

---

**Ready for production!** 🚀

