# Lab: Secure Kubernetes Application with Cert Manager, Wildcard SSL & Traefik Ingress

## Prerequisites

- Kubernetes Cluster
- Helm
- Traefik Ingress Controller Installed
- Wildcard DNS Record

```
*.learndevopsnow.it.com
```

must point to the Traefik LoadBalancer.

---

# Add Helm Repository

```bash
helm repo add jetstack https://charts.jetstack.io

helm repo update
```

---

# Install cert-manager

```bash
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set crds.enabled=true
```

---

# Verify Installation

```bash
kubectl get pods -n cert-manager

kubectl get crds | grep cert-manager
```

Expected Pods

- cert-manager
- cert-manager-cainjector
- cert-manager-webhook

---

# Create Cloudflare API Token Secret

Replace the API Token before running.

```bash
kubectl create secret generic cloudflare-api-token \
  --namespace cert-manager \
  --from-literal=api-token=YOUR_API_TOKEN
```

Verify

```bash
kubectl get secret -n cert-manager
```

---

# Create ClusterIssuer

Create **clusterissuer.yaml**

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-production
spec:
  acme:
    email: zwe.zzzin@gmail.com ## Replace with your mail
    server: https://acme-v02.api.letsencrypt.org/directory
    privateKeySecretRef:
      name: letsencrypt-production
    solvers:
      - dns01:
          cloudflare:
            apiTokenSecretRef:
              name: cloudflare-api-token
              key: api-token
```

Apply

```bash
kubectl apply -f clusterissuer.yaml
```

Verify

```bash
kubectl get clusterissuer

kubectl describe clusterissuer letsencrypt-production
```

Wait until

```
READY = True
```

---

# Create Wildcard Certificate

Create **certificate.yaml**

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: wildcard
spec:
  secretName: wildcard-tls
  issuerRef:
    name: letsencrypt-production
    kind: ClusterIssuer
  commonName: "*.learndevopsnow-mm.blog"
  dnsNames:
    - "*.learndevopsnow-mm.blog"
```

Apply

```bash
kubectl apply -f certificate.yaml
```

---

# Watch Certificate Creation

```bash
kubectl get certificaterequest

kubectl get order

kubectl get challenge

kubectl get certificate

kubectl get secret
```

Wait until

```
wildcard-tls
```

appears.

Verify

```bash
kubectl describe certificate wildcard

kubectl describe secret wildcard-tls
```

---

# Deploy Nginx

```bash
kubectl create deployment nginx \
  --image=nginx:1.29 \
  --replicas=2
```

Verify

```bash
kubectl get pods
```

---

# Create ClusterIP Service

```bash
kubectl expose deployment nginx \
  --port=80 \
  --target-port=80 \
  --name=nginx
```

Verify

```bash
kubectl get svc nginx
```

---

# Create Ingress

Create **ingress.yaml**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nginx
spec:
  ingressClassName: traefik
  tls:
    - hosts:
        - nginx.learndevopsnow-mm.blog
      secretName: wildcard-tls
  rules:
    - host: nginx.learndevopsnow-mm.blog
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

Apply

```bash
kubectl apply -f ingress.yaml
```

---

# Verify Ingress

```bash
kubectl get ingress

kubectl describe ingress nginx
```

---

# Verify Browser

Open

```
https://nginx.learndevopsnow.it.com
```

Verify

- HTTPS
- Valid Certificate
- Lock Icon

---

# Create Wildcard Certificate For Production Namespace

Create **prod-certificate.yaml**

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: wildcard
  namespace: production
spec:
  secretName: wildcard-tls
  issuerRef:
    name: letsencrypt-production
    kind: ClusterIssuer
  commonName: "*.learndevopsnow-mm.blog"
  dnsNames:
    - "*.learndevopsnow-mm.blog"
```

Apply

```bash
kubectl apply -f prod-certificate.yaml
```

---

# Troubleshooting

```bash
kubectl get clusterissuer

kubectl get certificate

kubectl get certificaterequest

kubectl get order

kubectl get challenge

kubectl describe clusterissuer letsencrypt-production

kubectl describe certificate wildcard

kubectl describe certificaterequest

kubectl describe order

kubectl describe challenge

kubectl describe ingress nginx

kubectl logs deployment/cert-manager -n cert-manager

kubectl logs deployment/cert-manager-webhook -n cert-manager

kubectl logs deployment/cert-manager-cainjector -n cert-manager
```

---

# Cleanup

```bash
kubectl delete ingress nginx

kubectl delete svc nginx

kubectl delete deployment nginx

kubectl delete certificate wildcard

kubectl delete clusterissuer letsencrypt-production

kubectl delete secret wildcard-tls

kubectl delete secret cloudflare-api-token -n cert-manager
```