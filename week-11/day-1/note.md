# Add Traefik Helm Repository
helm repo add traefik https://traefik.github.io/charts

# Update Helm Repository
helm repo update

# Create Namespace
kubectl create namespace traefik

# Install Traefik Ingress Controller
helm install traefik traefik/traefik \
  --namespace traefik

# Verify Pods
kubectl get pods -n traefik

# Verify Service
kubectl get svc -n traefik

# Watch External IP
kubectl get svc -n traefik -w

## Create Deployment

```bash
kubectl create deployment nginx \
  --image=nginx:1.29 \
  --replicas=3
```

## Create SVC

```bash
kubectl expose deployment nginx \
  --port=80 \
  --target-port=80 \
  --name=nginx
```

## Verify Pods

```bash
kubectl get pods
```

## Verify Service

```bash
kubectl get svc
```

# Create Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nginx
spec:
  ingressClassName: traefik
  rules:
    - host: nginx.learndevopsnow.it.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: nginx
                port:
                  number: 80
```

---

# Apply Ingress

```bash
kubectl apply -f ingress.yaml
```

---

# Verify Ingress

```bash
kubectl get ingress
```

---

# Open in Browser

```text
http://nginx.learndevopsnow.it.com
```
