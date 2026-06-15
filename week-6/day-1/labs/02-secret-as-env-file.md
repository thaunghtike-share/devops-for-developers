# Lab - Secret as .env File with subPath

## Build and Push Linux Image

```bash
cd backend

docker buildx build \
  --platform linux/amd64 \
  -t learndevopsnow123/secret-lab-backend:1.0 \
  --push .

cd ..
```

## Required .env

The backend image requires `/app/.env`:

```text
APP_NAME=Learn DevOps Now
BACKEND_PORT=8000
FLASK_ENV=production
POSTGRES_DB=appdb
POSTGRES_USER=admin
POSTGRES_PASSWORD=password123
DB_HOST=postgres
DB_PORT=5432
```

## PostgreSQL Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres
  namespace: secret-lab
type: Opaque
stringData:
  POSTGRES_DB: appdb
  POSTGRES_USER: admin
  POSTGRES_PASSWORD: password123
```

## PostgreSQL Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: secret-lab
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:16-alpine
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          valueFrom:
            secretKeyRef:
              name: postgres
              key: POSTGRES_DB
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: postgres
              key: POSTGRES_USER
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres
              key: POSTGRES_PASSWORD
---
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: secret-lab
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
```


```bash
kubectl port-forward deployment/postgres 5432:5432 -n secret-lab

psql -h localhost -p 5432 -U admin -d appdb

SELECT current_database(), current_user;

```

## Backend .env Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: backend
  namespace: secret-lab
type: Opaque
stringData:
  .env: |
    APP_NAME=Learn DevOps Now
    BACKEND_PORT=8000
    FLASK_ENV=production
    POSTGRES_DB=appdb
    POSTGRES_USER=admin
    POSTGRES_PASSWORD=password123
    DB_HOST=postgres
    DB_PORT=5432
```

## Backend Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: secret-lab
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: learndevopsnow123/secret-lab-backend:1.0
        ports:
        - containerPort: 8000
        volumeMounts:
        - name: dotenv
          mountPath: /app/.env
          subPath: .env
      volumes:
      - name: dotenv
        secret:
          secretName: backend
---
apiVersion: v1
kind: Service
metadata:
  name: backend
  namespace: secret-lab
spec:
  selector:
    app: backend
  ports:
  - port: 80
    targetPort: 8000
```

## Verify

```bash
kubectl get pods -n secret-lab

kubectl exec -it deployment/backend -n secret-lab -- bash

ls -l 
cat /app/.env

kubectl port-forward service/backend 8005:80 -n secret-lab

curl http://localhost:8005/api/health
```
