# Lab 3 - TLS Secret as Files

## Create Certificate

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-keyout tls.key \
-out tls.crt \
-subj "/CN=demo.local"
```

## Imperative

```bash
kubectl create secret tls app-tls-secret \
  --cert=tls.crt \
  --key=tls.key
```

## Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tls-demo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: tls-demo
  template:
    metadata:
      labels:
        app: tls-demo
    spec:
      containers:
      - name: app
        image: busybox:1.36
        command: ["sh","-c","sleep 3600"]
        volumeMounts:
        - name: tls-volume
          mountPath: /app/certs
      volumes:
      - name: tls-volume
        secret:
          secretName: app-tls-secret
```

## Verify

```bash
kubectl exec -it POD_NAME -- ls /app/certs
kubectl exec -it POD_NAME -- cat /app/certs/tls.crt
```
