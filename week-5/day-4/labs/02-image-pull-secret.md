# Lab 2 - Image Pull Secret

## Imperative

```bash
kubectl create secret docker-registry dockerhub-secret \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=learndevopsnow123 \
  --docker-password=Tho@861998 \
  -n secret-lab
```

## Verify

```bash
kubectl get secrets -n secret-lab

kubectl get secret dockerhub-secret -n secret-lab

kubectl get secret dockerhub-secret \
-o yaml \
-n secret-lab
```

---

## Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: private-app
  namespace: secret-lab
spec:
  replicas: 1
  selector:
    matchLabels:
      app: private-app
  template:
    metadata:
      labels:
        app: private-app
    spec:
      imagePullSecrets:
      - name: dockerhub-secret
      containers:
      - name: private-app
        image: learndevopsnow123/python-flask-app:1.0
        imagePullPolicy: Always
        ports:
        - name: http
          containerPort: 5000
          protocol: TCP
---
apiVersion: v1
kind: Service
metadata:
  name: private-app-service
  namespace: secret-lab
spec:
  type: ClusterIP
  selector:
    app: private-app
  ports:
  - name: http
    port: 80
    targetPort: 5000
    protocol: TCP
```

```bash
vim lab.yaml
kubectl apply -f lab.yaml
kubectl port-forward svc/private-app-service 5005:80 -n secret-lab
``` 
