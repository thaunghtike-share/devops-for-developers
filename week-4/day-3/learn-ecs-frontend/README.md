# learn-ecs-frontend

Clean React + Vite frontend for ECS demo.

## Environment

Only one app-level environment variable is required:

## Local Run

```bash
docker build \
  --build-arg VITE_API_URL=http://localhost:8000 \
  -t learn-ecs-frontend .

docker run -d -p 3000:80 learn-ecs-frontend 
```

Open:

```text
http://localhost:3000
```

## Docker Build For ECS

```bash
docker build \
  --build-arg VITE_API_URL=http://learn-ecs-backend.ecs.local:8000 \
  -t learn-ecs-frontend .
```

## ECS Container Port

```text
80
```

## Notes

This repo does NOT use:

```text
docker-entrypoint.sh
config.js
nginx API proxy
fake frontend env variables
```

The app uses:

```js
import.meta.env.VITE_API_URL
```
