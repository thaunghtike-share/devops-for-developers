# Kong Gateway API - Gateway & HTTPRoute Lab

## 1. Install Gateway API CRDs

```bash
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.5.1/standard-install.yaml
```

Verify:

```bash
kubectl get crd | grep gateway.networking.k8s.io
```

---

## 2. Add Kong Helm Repository

```bash
helm repo add kong https://charts.konghq.com
helm repo update
```

---

## 3. Install Kong

```bash
helm upgrade --install kong kong/kong \
  --namespace kong \
  --create-namespace \
  --set proxy.annotations."service\.beta\.kubernetes\.io/aws-load-balancer-scheme"=internet-facing
```

---

## 4. Verify Kong Installation

```bash
kubectl get pods,svc -n kong
```

Wait until the Kong Pod is running and the `kong-kong-proxy` Service receives a LoadBalancer DNS name.

Get the Kong Proxy address:

```bash
kubectl get svc kong-kong-proxy -n kong
```

---

## 5. Create GatewayClass

Create `gatewayclass.yaml`:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: kong
  annotations:
    konghq.com/gatewayclass-unmanaged: "true"
spec:
  controllerName: konghq.com/kic-gateway-controller
```

Apply:

```bash
kubectl apply -f gatewayclass.yaml
```

Verify:

```bash
kubectl get gatewayclass
```

---

## 6. Create Demo Namespace

```bash
kubectl create namespace demo
```

---

## 7. Create Gateway

Create `gateway.yaml`:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: kong-gateway
  namespace: demo
spec:
  gatewayClassName: kong
  listeners:
    - name: http
      protocol: HTTP
      port: 80
      allowedRoutes:
        namespaces:
          from: Same
```

Apply:

```bash
kubectl create ns demo
kubectl apply -f gateway.yaml
```

Verify:

```bash
kubectl get gateway -n demo
```

Check Gateway status:

```bash
kubectl describe gateway kong-gateway -n demo
```

---

## 8. Deploy WhoAmI

```bash
kubectl create deployment whoami \
  --image=traefik/whoami \
  --replicas=2 \
  -n demo
```

---

## 9. Expose WhoAmI Service

```bash
kubectl expose deployment whoami \
  --name whoami \
  --port 80 \
  --target-port 80 \
  --type ClusterIP \
  -n demo
```

Verify:

```bash
kubectl get pods,svc -n demo
```

---

## 10. Test WhoAmI Service

Test the application from inside the cluster:

```bash
kubectl run curl-test \
  --image=curlimages/curl \
  --restart=Never \
  --rm -it \
  -n demo \
  -- curl http://whoami
```

---

## 11. Create HTTPRoute

Create `httproute.yaml`:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: whoami
  namespace: demo
spec:
  parentRefs:
    - name: kong-gateway
  hostnames:
    - "whoami.learndevopsnow-mm.blog"
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /
      backendRefs:
        - name: whoami
          port: 80
```

Apply:

```bash
kubectl apply -f httproute.yaml
```

---

## 12. Verify HTTPRoute

```bash
kubectl get httproute -n demo
```

Check details:

```bash
kubectl describe httproute whoami -n demo
```

Check Gateway and HTTPRoute together:

```bash
kubectl get gateway,httproute -n demo
```

---

## 13. Get Kong Proxy LoadBalancer DNS

```bash
kubectl get svc kong-kong-proxy -n kong
```

Get only the LoadBalancer DNS:

```bash
kubectl get svc kong-kong-proxy -n kong \
  -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```

---

## 14. Configure Cloudflare DNS

Create the following DNS record:

| Type | Name | Target | Proxy | TTL |
| --- | --- | --- | --- | --- |
| CNAME | whoami | Kong Proxy LoadBalancer DNS | DNS Only | Auto |

Domain:

```text
whoami.learndevopsnow-mm.blog
```

---

## 15. Test HTTPRoute

```bash
curl http://whoami.learndevopsnow-mm.blog
```

Run the command multiple times:

```bash
curl http://whoami.learndevopsnow-mm.blog
```

The requests should be routed to the WhoAmI application through Kong.

---

## 16. Final Verification

```bash
kubectl get gatewayclass
```

```bash
kubectl get gateway,httproute -n demo
```

```bash
kubectl get pods,svc -n demo
```

```bash
kubectl get pods,svc -n kong
```

---

## Request Flow

```text
Client
   ↓
Cloudflare DNS
   ↓
AWS LoadBalancer
   ↓
Kong Proxy
   ↓
Gateway :80
   ↓
HTTPRoute
   ↓
WhoAmI Service :80
   ↓
WhoAmI Pods
```