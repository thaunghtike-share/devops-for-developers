# Learn DevOps Three Tier App V2

Ready-to-run Docker Compose app.

## Architecture

```text
Frontend Nginx UI
        ↓
Backend Flask API :8000
        ↓
PostgreSQL Database
```

## Features

- Pretty frontend UI
- Register user
- Show total user count
- Show today's user count
- Show role count
- List registered users
- Delete user
- API health status
- Backend runs on port 8000
- No logo image required

## Run

```bash
docker compose up --build
```

Open:

```text
http://localhost:3000
```

## Backend API

Direct backend URL:

```text
http://localhost:8000/api/health
```

## Stop

```bash
docker compose down
```

## Reset Database

```bash
docker compose down -v
docker compose up --build
```

## Services

| Service | Container Port | Local Port |
|---|---:|---:|
| frontend | 80 | 3000 |
| backend | 8000 | 8000 |
| db | 5432 | internal only |

## API Endpoints

```text
GET    /api/health
GET    /api/stats
GET    /api/users
POST   /api/register
DELETE /api/users/:id
```
