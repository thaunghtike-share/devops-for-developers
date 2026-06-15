## Local Test

.env 

```text
APP_NAME=Learn DevOps Now

BACKEND_PORT=8000
FLASK_ENV=production

POSTGRES_DB=learn_devops
POSTGRES_USER=learn_user
POSTGRES_PASSWORD=learn_password
DB_HOST=learn-ecs-db
DB_PORT=5432
```

Backend URL:

```text
http://localhost:8000
```

Health check:

```bash
curl http://localhost:8000/api/health
```

## Backend API

```text
GET    /api/health
GET    /api/stats
GET    /api/users
POST   /api/register
DELETE /api/users/:id
```