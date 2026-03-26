# Ooumph AI-Enabled Bridge & Flyover Planning System

An AI-powered decision support system for infrastructure planning, Andhra Pradesh Roads & Buildings Department.

## Features

- **Traffic Analysis**: AI-powered traffic flow analysis, congestion detection, and accident hotspot identification
- **Forecasting**: Predict future traffic demand (5-10 years) with multi-factor analysis
- **Simulation**: Compare infrastructure scenarios (flyover, road widening, signal optimization)
- **Site Analysis**: GIS-based site suitability evaluation with risk zone detection
- **Monitoring**: Real-time construction progress tracking with AI anomaly detection
- **AI Assistant**: Multi-agent federated thinking for explainable recommendations

## Tech Stack

### Backend
- Python 3.11+ with FastAPI
- SQLAlchemy ORM with async support
- PostgreSQL with PostGIS extension
- Redis for caching
- OpenAI API for AI features
- Alembic for database migrations

### Frontend
- React 18 with TypeScript
- Vite for build tooling
- TailwindCSS for styling
- React Router v6
- Zustand for state management
- Axios for API calls
- React Hook Form with Zod validation

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- Docker & Docker Compose (recommended)
- PostgreSQL 15 with PostGIS
- Redis 7

## Installation

### Using Docker Compose (Recommended)

```bash
git clone <repository-url>
cd ooumph-gip
cp .env.example .env
docker-compose up --build
```

Access the application:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Manual Setup

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Development

### Backend Development

Start the development server:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### Frontend Development

Start the development server:
```bash
cd frontend
npm run dev
```

### Database Migrations

Create a new migration:
```bash
cd backend
alembic revision -m "description of migration"
```

Apply migrations:
```bash
alembic upgrade head
```

## API Documentation

Access the Swagger UI at: http://localhost:8000/docs

## Project Structure

```
ooumph-gip/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── ai/            # AI agents and orchestration
│   │   ├── middleware/    # Custom middleware
│   │   ├── models/        # SQLAlchemy models
│   │   ├── routers/       # API route handlers
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   ├── stubs/         # Mock external services
│   │   └── utils/         # Utility functions
│   ├── alembic/           # Database migrations
│   └── tests/             # Test files
├── frontend/               # React Vite frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── hooks/         # Custom hooks
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   ├── store/         # Zustand stores
│   │   └── types/         # TypeScript types
│   └── public/            # Static assets
├── docker-compose.yml     # Docker Compose configuration
└── README.md              # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License
