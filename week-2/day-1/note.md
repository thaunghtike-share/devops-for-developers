# Docker Compose Demo Video Commands

> Project: `compose-app`
> Services: Flask Backend + MySQL + Redis

---

## Step 1 - Go To Project Folder

```bash
cd compose-app
```

---

## Step 2 - Check Project Files

```bash
ls
```

Expected files:

```text
backend
db
docker-compose.yml
.env
README.md
```

---

## Step 3 - Show Project Structure

If `tree` is installed:

```bash
tree
```

If `tree` is not installed:

```bash
find . -maxdepth 3 -type f
```

Expected structure:

```text
./README.md
./.env
./docker-compose.yml
./backend/Dockerfile
./backend/app.py
./backend/requirements.txt
./db/init/01-init.sql
```

---

## Step 4 - Show Environment File

```bash
cat .env
```

This file is used by Docker Compose.

Important values:

```text
APP_NAME=Learn DevOps Now
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_DATABASE=compose_demo
MYSQL_USER=appuser
MYSQL_PASSWORD=apppassword
REDIS_HOST=redis
REDIS_PORT=6379
```

---

## Step 5 - Show Docker Compose File

```bash
cat docker-compose.yml
```

This compose file creates 3 services:

```text
backend
mysql
redis
```

---

## Step 6 - Show Backend Dockerfile

```bash
cat backend/Dockerfile
```

---

## Step 7 - Show Backend Application Code

```bash
cat backend/app.py
```

---

## Step 8 - Show MySQL Init SQL

```bash
cat db/init/01-init.sql
```

This SQL file creates the `visits` table automatically when MySQL container starts for the first time.

---

## Step 9 - Check Current Docker Containers

```bash
docker ps
```

```bash
docker ps -a
```

---

## Step 10 - Validate Docker Compose Config

```bash
docker compose config
```

This command checks the final compose configuration after reading `.env`.

---

## Step 11 - Start All Services With Build

```bash
docker compose up -d --build
```

This will build the backend image and start:

```text
compose-backend
compose-mysql
compose-redis
```

---

## Step 12 - Check Running Services

```bash
docker compose ps
```

or:

```bash
docker ps
```

---

## Step 13 - Check Backend Logs

```bash
docker compose logs backend
```

For live logs:

```bash
docker compose logs -f backend
```

Press `CTRL + C` to exit live logs.

---

## Step 14 - Check MySQL Logs

```bash
docker compose logs mysql
```

---

## Step 15 - Check Redis Logs

```bash
docker compose logs redis
```

---

## Step 16 - Test Backend Home API

Backend is mapped from container port `5000` to local port `5001`.

```bash
curl http://localhost:5001
```

Expected response includes:

```json
{
  "message": "Hello from Flask Backend API",
  "app_name": "Learn DevOps Now"
}
```

---

## Step 17 - Test Health API

```bash
curl http://localhost:5001/health
```

Expected response includes:

```json
{
  "status": "healthy",
  "mysql": "connected",
  "redis": "connected"
}
```

---

## Step 18 - Test MySQL + Redis Integration

```bash
curl http://localhost:5001/visits
```

Run it multiple times:

```bash
curl http://localhost:5001/visits
curl http://localhost:5001/visits
curl http://localhost:5001/visits
```

This endpoint inserts rows into MySQL and increments visit count in Redis.

---

## Step 19 - Enter MySQL Container

```bash
docker compose exec mysql mysql -uappuser -papppassword compose_demo
```

Inside MySQL shell, run:

```sql
SHOW TABLES;
```

```sql
SELECT * FROM visits;
```

Exit MySQL:

```sql
exit;
```

---

## Step 20 - Enter Redis Container

```bash
docker compose exec redis redis-cli
```

Inside Redis CLI, run:

```redis
PING
```

```redis
GET total_visits
```

Exit Redis CLI:

```redis
exit
```

---

## Step 21 - Enter Backend Container

```bash
docker compose exec backend sh
```

Inside backend container:

```bash
ls
```

```bash
printenv | grep APP_NAME
```

```bash
printenv | grep DB_
```

```bash
printenv | grep REDIS_
```

Exit container:

```bash
exit
```

---

## Step 22 - Inspect Docker Network

```bash
docker network ls
```

```bash
docker network inspect compose-app_compose-net
```

If the network name is different, get it with:

```bash
docker network ls | grep compose
```

---

## Step 23 - Inspect Docker Volume

```bash
docker volume ls
```

```bash
docker volume inspect compose-app_mysql_data
```

If the volume name is different, get it with:

```bash
docker volume ls | grep mysql
```

---

## Step 24 - Restart Backend Service

```bash
docker compose restart backend
```

Check again:

```bash
docker compose ps
```

---

## Step 25 - Stop All Services

```bash
docker compose stop
```

Check:

```bash
docker compose ps
```

---

## Step 26 - Start All Services Again

```bash
docker compose start
```

Check:

```bash
docker compose ps
```

---

## Step 27 - Stop And Remove Containers Only

```bash
docker compose down
```

This removes containers and network, but keeps the named volume.

---

## Step 28 - Start Again To Prove MySQL Data Persists

```bash
docker compose up -d
```

Test visits again:

```bash
curl http://localhost:5001/visits
```

Because `mysql_data` volume still exists, MySQL data can persist.

---

## Step 29 - Full Cleanup Including MySQL Volume

Use this only when the demo is finished.

```bash
docker compose down -v
```

---

## Step 30 - Verify Cleanup

```bash
docker ps -a
```

```bash
docker volume ls | grep mysql
```

```bash
docker network ls | grep compose
```

---

## Important Note - If MySQL Port 3306 Is Already Used On Mac

Check port:

```bash
lsof -i :3306
```

If local MySQL is using port 3306, either stop local MySQL or change this line in `.env`:

```text
MYSQL_PORT=3307
```

Then run:

```bash
docker compose up -d --build
```
