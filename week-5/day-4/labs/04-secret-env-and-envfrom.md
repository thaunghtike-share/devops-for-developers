# Lab 4 - Secret as ENV and envFrom

## Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
stringData:
  DB_USER: admin
  DB_PASSWORD: password123
  JWT_SECRET: my-secret
```

## Deployment (env)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-env
spec:
  replicas: 1
  selector:
    matchLabels:
      app: app-env
  template:
    metadata:
      labels:
        app: app-env
    spec:
      containers:
      - name: app
        image: busybox:1.36
        command: ["sh","-c","sleep 3600"]
        env:
        - name: DB_USER
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: DB_USE4
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: DB_PASSWORD
```

## Deployment (envFrom)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-envfrom
spec:
  replicas: 1
  selector:
    matchLabels:
      app: app-envfrom
  template:
    metadata:
      labels:
        app: app-envfrom
    spec:
      containers:
      - name: app
        image: busybox:1.36
        command: ["sh","-c","sleep 3600"]
        envFrom:
        - secretRef:
            name: app-secret
```

## Verify

```bash
kubectl exec -it POD_NAME -- env | grep DB
kubectl exec -it POD_NAME -- env
```
