# Docker Compose App With Database

This demo includes:

- React frontend
- Flask backend
- MySQL database
- Redis cache
- MySQL init SQL file

## Run

```bash
cp .env.example .env
docker compose up -d --build
```

## Test

Frontend:

```text
http://localhost:3000
```

Backend:

```text
http://localhost:5000
```

Health:

```text
http://localhost:5000/health
```

MySQL + Redis test:

```text
http://localhost:5000/visits
```

## Useful Commands

```bash
docker compose ps
docker compose logs -f backend
docker compose exec mysql mysql -uappuser -papppassword compose_demo
docker compose exec redis redis-cli
docker compose down
docker compose down -v
```

## Notes

- Backend connects to MySQL using service name `mysql`.
- Backend connects to Redis using service name `redis`.
- MySQL data is persisted using named volume `mysql_data`.
- Initial database table is created from `db/init/01-init.sql`.
