# Lab 5 - Secret as .env File

## Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: env-secret
type: Opaque
stringData:
  .env: |
    DB_HOST=postgres
    DB_USER=admin
    DB_PASSWORD=password123
```

## Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dotenv-demo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: dotenv-demo
  template:
    metadata:
      labels:
        app: dotenv-demo
    spec:
      containers:
      - name: app
        image: busybox:1.36
        command: ["sh","-c","sleep 3600"]
        volumeMounts:
        - name: env-volume
          mountPath: /app/.env
          subPath: .env
      volumes:
      - name: env-volume
        secret:
          secretName: env-secret
```

## Verify

```bash
kubectl exec -it POD_NAME -- cat /app/.env
```
