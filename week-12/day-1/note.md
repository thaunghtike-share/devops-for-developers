# AWS Load Balancer Controller - Lab 3

# Environment

| Item | Value |
|------|-------|
| Cluster | my-eks-cluster |
| Namespace | dev, prod |
| Domain | *.dev.learndevopsnow-mm.blog |
| Domain | *.prod.learndevopsnow-mm.blog |

---

# Delete Previous Resources

```bash
kubectl delete ingress --all --force
kubectl delete all --all --force
```

---

# Create Namespaces

```bash
kubectl create namespace dev
kubectl create namespace prod
```

---

# Verify

```bash
kubectl get ns
```

---

# Deploy Applications

## Development

### App 1

```bash
kubectl create deployment app1 \
--image=nginx \
--replicas=2 \
-n dev

kubectl expose deployment app1 \
--port=80 \
--target-port=80 \
-n dev
```

---

### App 2

```bash
kubectl create deployment app2 \
--image=httpd \
--replicas=2 \
-n dev

kubectl expose deployment app2 \
--port=80 \
--target-port=80 \
-n dev
```

---

## Production

### App 1

```bash
kubectl create deployment app1 \
--image=nginx \
--replicas=2 \
-n prod

kubectl expose deployment app1 \
--port=80 \
--target-port=80 \
-n prod
```

---

### App 2

```bash
kubectl create deployment app2 \
--image=httpd \
--replicas=2 \
-n prod

kubectl expose deployment app2 \
--port=80 \
--target-port=80 \
-n prod
```

---

# Verify

```bash
kubectl get pods -n dev
kubectl get svc -n dev
kubectl get pods -n prod
kubectl get svc -n prod
```

---

# Create Development Ingress Group

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app1
  namespace: dev
  annotations:
    alb.ingress.kubernetes.io/group.name: dev
    alb.ingress.kubernetes.io/group.order: "10"
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
spec:
  ingressClassName: alb
  rules:
    - host: app1.dev.learndevopsnow-mm.blog
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app1
                port:
                  number: 80
```

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app2
  namespace: dev
  annotations:
    alb.ingress.kubernetes.io/group.name: dev
    alb.ingress.kubernetes.io/group.order: "20"
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
spec:
  ingressClassName: alb
  rules:
    - host: app2.dev.learndevopsnow-mm.blog
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app2
                port:
                  number: 80
```

```bash
kubectl apply -f app1-dev-ingress.yaml
kubectl apply -f app2-dev-ingress.yaml

```

# Create Production Ingress Group

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app1
  namespace: prod
  annotations:
    alb.ingress.kubernetes.io/group.name: production
    alb.ingress.kubernetes.io/group.order: "10"
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
spec:
  ingressClassName: alb
  rules:
    - host: app1.prod.learndevopsnow-mm.blog
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app1
                port:
                  number: 80
```

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app2
  namespace: prod
  annotations:
    alb.ingress.kubernetes.io/group.name: production
    alb.ingress.kubernetes.io/group.order: "20"
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
spec:
  ingressClassName: alb
  rules:
    - host: app2.prod.learndevopsnow-mm.blog
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app2
                port:
                  number: 80
```

```bash
kubectl apply -f app1-prod-ingress.yaml
kubectl apply -f app2-prod-ingress.yaml

```

---

# Verify

```bash
kubectl get ingress -A
```

---

# Verify AWS Console

- 2 Application Load Balancers
- 4 Target Groups
- Host-based Listener Rules