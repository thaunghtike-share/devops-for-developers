# AWS Load Balancer Controller - Lab 2

# Environment

| Item | Value |
|------|-------|
| Cluster | my-eks-cluster |
| Namespace | default |
| Domain | *.learndevopsnow-mm.blog |

---

# Architecture

```text
                     Internet
                         │
                         ▼
              Application Load Balancer
                         │
                  Host-based Routing
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
 app1.learndevopsnow-mm.blog               app2.learndevopsnow-mm.blog
         │                               │
      Service                        Service
         │                               │
     Deployment                    Deployment
```

---

# Verify Cluster

```bash
kubectl get nodes
```

```bash
kubectl get pods -n kube-system
```

---

# Create Deployment - App 1

```bash
kubectl create deployment app1 \
--image=nginx \
--replicas=2
```

---

# Expose Service - App 1

```bash
kubectl expose deployment app1 \
--port=80 \
--target-port=80
```

---

# Create Deployment - App 2

```bash
kubectl create deployment app2 \
--image=httpd \
--replicas=2
```

---

# Expose Service - App 2

```bash
kubectl expose deployment app2 \
--port=80 \
--target-port=80
```

---

# Verify

```bash
kubectl get deployment
```

```bash
kubectl get service
```

---

# Create Ingress - App 1

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app1
  annotations:
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
spec:
  ingressClassName: alb
  rules:
  - host: app1.learndevopsnow-mm.blog
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

```bash
kubectl apply -f app1-ingress.yaml
```

---

# Verify

```bash
kubectl get ingress
```

---

# Create Ingress - App 2

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app2
  annotations:
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
spec:
  ingressClassName: alb
  rules:
  - host: app2.learndevopsnow-mm.blog
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
kubectl apply -f app2-ingress.yaml
```

---

# Verify

```bash
kubectl get ingress
```