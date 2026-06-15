# Lab - Secret as ENV and envFrom with PostgreSQL

## Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secret
  namespace: secret-lab
type: Opaque
stringData:
  POSTGRES_DB: appdb
  POSTGRES_USER: admin
  POSTGRES_PASSWORD: password123
```

## Deployment using env

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres-env
  namespace: secret-lab
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres-env
  template:
    metadata:
      labels:
        app: postgres-env
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
              name: postgres-secret
              key: POSTGRES_DB
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: POSTGRES_USER
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: POSTGRES_PASSWORD
```

## Verify env

```bash
kubectl get pod -n secret-lab -l app=postgres-env

kubectl exec -it POD_NAME -n secret-lab -- bash

printenv | grep POSTGRES

kubectl logs -f POD_NAME -n secret-lab
```

## Test PostgreSQL Login

```bash
kubectl exec -it POD_NAME -n secret-lab -- bash 

kubectl port-forward deployment/postgres-env 5432:5432 -n secret-lab

psql -h localhost -p 5432 -U admin -d appdb

SELECT current_database(), current_user;

```