# Nova Corrente - Deployment Guide

## Production Deployment with Docker Compose

This guide describes how to deploy Nova Corrente in a production environment using Docker Compose.

## Prerequisites

- Docker Engine (20.10.0 or later)
- Docker Compose (v2.0.0 or later)
- At least 4GB of RAM available
- 10GB of free disk space

## Quick Start

### 1. Clone the repository

```bash
git clone <repository-url>
cd gran-prix
```

### 2. Configure environment variables

Copy the example environment file and update the values:

```bash
cp .env.example .env
# Edit .env and set appropriate values
```

Important environment variables to configure:
- `SECRET_KEY`: Set a strong secret key for JWT tokens
- `DB_PASSWORD`: Set a strong database password
- `CORS_ORIGINS`: Set allowed origins for CORS
- `NEXT_PUBLIC_API_URL`: Set the backend API URL

### 3. Initialize the database

Before starting the services, you may need to initialize the database schema:

```bash
# If running locally for the first time, you can seed with demo data
docker-compose run --rm backend alembic upgrade head
```

### 4. Start the services

For development:
```bash
docker-compose up -d
```

For production:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 5. Access the application

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:5000`
- Database: `localhost:5432` (PostgreSQL)

## Services

### Database (PostgreSQL)
- Automatically initialized with the required schema
- Data persisted in a Docker volume
- Optimized for analytical workloads

### Backend API (Flask)
- Serves precomputed forecasts, features, KPIs, recommendations
- Read-only operations only (no real-time ML in production)
- JWT-based authentication and RBAC

### Frontend (Next.js)
- Interactive dashboard for analytics
- Connected to backend via API
- Responsive design

## Configuration

### Environment Variables

The application can be configured using environment variables in the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_USER` | Database username | `nova_corrente` |
| `DB_PASSWORD` | Database password | `strong_password` |
| `DB_NAME` | Database name | `nova_corrente` |
| `SECRET_KEY` | JWT secret key | `change-this-in-production` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:5000` |
| `EXTERNAL_APIS_ENABLED` | Enable external API calls | `false` |
| `ENABLE_ML_PROCESSING` | Enable ML processing | `false` |

### Production Considerations

1. **Security**:
   - Update `SECRET_KEY` with a strong, random value
   - Use HTTPS in production (configure reverse proxy)
   - Limit access to database port (5432)

2. **Performance**:
   - The production compose file includes resource limits
   - PostgreSQL is configured with production-ready settings
   - Use a reverse proxy like Nginx for static file serving

3. **Backup**:
   - Regular database backups are essential
   - The PostgreSQL data is stored in a Docker volume
   - Follow your organization's backup policies

## Data Pipeline

The ML processing happens offline. To run the data pipeline:

```bash
# Run the ML pipeline to generate forecasts and features
docker-compose exec backend python ml_pipeline/main.py

# Load precomputed outputs to the database
docker-compose exec backend python etl/load_ml_outputs.py
```

## Monitoring and Maintenance

### Health Checks

The services include health checks:

- Backend: `/health` endpoint
- Database: Built-in PostgreSQL health check

### Logs

View application logs:

```bash
# View all services logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres
```

### Updating

To update to a new version:

1. Pull the latest code: `git pull`
2. Update environment file if needed
3. Rebuild containers: `docker-compose build`
4. Start services: `docker-compose up -d`

## Troubleshooting

### Common Issues

1. **Database connection errors**:
   - Check that PostgreSQL is running: `docker-compose logs postgres`
   - Verify database credentials in `.env`

2. **Frontend cannot connect to API**:
   - Check `NEXT_PUBLIC_API_URL` in `.env`
   - Verify backend is running: `docker-compose logs backend`

3. **Performance issues**:
   - Ensure sufficient resources allocated to containers
   - Check PostgreSQL configuration in production compose

### Resetting the Database

If you need to reset the database (will lose all data):

```bash
docker-compose down -v  # Removes volumes
docker-compose up -d
```

## Architecture Notes

- All machine learning operations run offline
- Production only reads precomputed results
- No external API calls during normal operation
- PostgreSQL with partitioned tables for performance
- Materialized views for frequently accessed analytics