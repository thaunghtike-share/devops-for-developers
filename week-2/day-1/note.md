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

Backend:

```text
curl http://localhost:5001
```

Health:

```text
curl http://localhost:5001/health
```

MySQL + Redis test:

```text
curl http://localhost:5001/visits
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
