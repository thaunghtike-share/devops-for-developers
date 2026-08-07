# Kong Gateway API - Video 1 Lab

## Prerequisites

- Kubernetes Cluster
- kubectl
- Helm 3
- Cloudflare Domain

---

## Install Gateway API CRDs

```bash
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.5.1/standard-install.yaml
```

---

## Add Kong Helm Repository

```bash
helm repo add kong https://charts.konghq.com
helm repo update
```

---

## Install Kong

```bash
helm upgrade --install kong kong/kong \
  --namespace kong \
  --create-namespace
```

---

## Verify Kong Installation

```bash
kubectl get pods,svc -n kong
```

Wait until all Pods are in the **Running** state and the Kong Proxy Service receives an **EXTERNAL-IP** or **LoadBalancer DNS**.

---

## Get Kong Proxy Address

```bash
kubectl get svc kong-kong-proxy -n kong
```

Copy the value shown under the **EXTERNAL-IP** column.

---

## Configure Cloudflare Wildcard DNS

| Type | Name | Target | Proxy | TTL |
|------|------|--------|-------|-----|
| CNAME | * | Kong Proxy LoadBalancer DNS | DNS Only | Auto |

---

## Create Demo Namespace

```bash
kubectl create namespace demo
```

---

## Deploy Sample Application

```bash
kubectl create deployment whoami \
  --image=traefik/whoami \
  --replicas=2 
```

---

## Expose Service

```bash
kubectl expose deployment whoami \
  --name whoami \
  --port 80 \
  --target-port 80 \
  --type ClusterIP 
```

---

## Test Service

```bash
kubectl run curl-test \
  --image=curlimages/curl \
  --restart=Never \
  --rm -it \
  -- curl http://whoami
```

## Create Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: whoami
spec:
  ingressClassName: kong
  rules:
    - host: whoami.learndevopsnow-mm.blog
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: whoami
                port:
                  number: 80
```                  

## Kong Helm Chart Upgrade

```bash
helm upgrade kong kong/kong \
  --namespace kong \
  --set proxy.annotations."service\.beta\.kubernetes\.io/aws-load-balancer-scheme"=internet-facing
```