# Deployment Guide

## Server Requirements

- Docker with Docker Compose V2
- Ports available: 15432 (PostgreSQL), 16379 (Redis), 18000 (Backend), 13000 (Frontend)
- Environment file: `.env.production`

## Quick Deploy

```bash
./deploy.sh deploy
```

## Default Ports

| Service | Port | Description |
|---------|------|-------------|
| PostgreSQL | 15432 | PostGIS database |
| Redis | 16379 | Cache and session store |
| Backend API | 18000 | FastAPI application |
| Frontend | 13000 | React/Nginx application |

## Environment Variables

Create `.env.production` file with:

```env
# Database
POSTGRES_DB=ai_infrastructure_prod
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<your-secure-password>

# Ports (optional - defaults shown)
POSTGRES_PORT=15432
REDIS_PORT=16379
BACKEND_PORT=18000
FRONTEND_PORT=13000

# Application
SECRET_KEY=<your-secret-key>
OPENAI_API_KEY=<your-openai-api-key>
CORS_ORIGINS=*

# Frontend
VITE_API_BASE_URL=http://localhost:18000/api/v1
```

## Database Migrations

Migrations are run automatically during deployment using Alembic.

### Manual Migration Commands

```bash
# Check current migration status
docker compose -f docker-compose.prod.yml exec backend alembic current

# Run migrations
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Rollback one migration
docker compose -f docker-compose.prod.yml exec backend alembic downgrade -1

# Create new migration
docker compose -f docker-compose.prod.yml exec backend alembic revision --autogenerate -m "description"
```

### Migration Files Location

Migration files are stored in: `backend/alembic/versions/`

## Demo Users / Seeders

Demo users are created automatically during deployment.

### Default Credentials

| Role | Email | Password |
|------|-------|----------|
| Administrator | admin@ooumph.com | admin123 |
| Infrastructure Planner | planner@ooumph.com | planner123 |
| Viewer | viewer@ooumph.com | viewer123 |

### Manual Seed Command

```bash
docker compose -f docker-compose.prod.yml exec backend python seed_admin.py
```

### Seeder File Location

Seeder script: `backend/seed_admin.py`

## Useful Commands

### Container Management

```bash
# Start services
./deploy.sh start

# Stop services
./deploy.sh stop

# Restart services
./deploy.sh restart

# View status
docker compose -f docker-compose.prod.yml ps

# View logs
./deploy.sh logs
./deploy.sh logs backend
./deploy.sh logs frontend
```

### Database Access

```bash
# Connect to PostgreSQL
docker compose -f docker-compose.prod.yml exec postgres psql -U postgres -d ai_infrastructure_prod

# Backup database
docker compose -f docker-compose.prod.yml exec postgres pg_dump -U postgres ai_infrastructure_prod > backup.sql

# Restore database
cat backup.sql | docker compose -f docker-compose.prod.yml exec -T postgres psql -U postgres ai_infrastructure_prod
```

### Redis Access

```bash
# Connect to Redis CLI
docker compose -f docker-compose.prod.yml exec redis redis-cli
```

## Health Checks

- Backend: `http://localhost:18000/api/v1/health`
- API Docs: `http://localhost:18000/docs`

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
sudo lsof -i :<port>

# Kill process
sudo fuser -k <port>/tcp
```

### Clean Up Docker Resources

```bash
./deploy.sh cleanup
```

### Reset Everything

```bash
# Stop and remove containers, networks, volumes
docker compose -f docker-compose.prod.yml down -v

# Rebuild and deploy
./deploy.sh deploy
```

## Access URLs

After successful deployment:

- **Frontend**: http://localhost:13000
- **Backend API**: http://localhost:18000
- **API Documentation**: http://localhost:18000/docs
- **Health Check**: http://localhost:18000/api/v1/health
