# Lab: Kubernetes Gateway API with HTTPS, Wildcard SSL & Kong Gateway

## 1. Make sure Kong is running

```bash
kubectl get all -n kong
```

---

## 2. Add cert-manager Helm Repository

```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update
```

---

## 3. Install cert-manager

```bash
helm upgrade --install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set crds.enabled=true
```

---

## 4. Create Cloudflare API Token Secret

```bash
kubectl create secret generic cloudflare-api-token \
  --namespace cert-manager \
  --from-literal=api-token=YOUR_TOKEN
```

---

## 5. Create ClusterIssuer

Create `clusterissuer.yaml`

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-production
spec:
  acme:
    email: thaunghtikeoo.aws@gmail.com
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

Apply:

```bash
kubectl apply -f clusterissuer.yaml
```

Check:

```bash
kubectl get clusterissuer
```

---

## 6. Create Wildcard Certificate in Kong Namespace

Create `certificate.yaml`

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: wildcard
  namespace: kong
spec:
  secretName: wildcard-tls
  issuerRef:
    name: letsencrypt-production
    kind: ClusterIssuer
  commonName: "*.learndevopsnow-mm.blog"
  dnsNames:
    - "*.learndevopsnow-mm.blog"
```

Apply:

```bash
kubectl apply -f certificate.yaml
```

Check:

```bash
kubectl get certificate -n kong
```

```bash
kubectl get secret wildcard-tls -n kong
```

---

## 7. Create Shared Gateway

Create `gateway.yaml`

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: kong-gateway
  namespace: kong
spec:
  gatewayClassName: kong
  listeners:
    - name: http
      protocol: HTTP
      port: 80
      allowedRoutes:
        namespaces:
          from: All
    - name: https
      protocol: HTTPS
      port: 443
      tls:
        mode: Terminate
        certificateRefs:
          - group: ""
            kind: Secret
            name: wildcard-tls
      allowedRoutes:
        namespaces:
          from: All
```

Apply:

```bash
kubectl apply -f gateway.yaml
```

Check:

```bash
kubectl get gateway -n kong
```

```bash
kubectl describe gateway kong-gateway -n kong
```

---

## 8. Create HTTPS HTTPRoute

WhoAmI Application and Service remain in the `demo` namespace.

Create `httproute.yaml`

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: whoami
  namespace: demo
spec:
  parentRefs:
    - name: kong-gateway
      namespace: kong
      sectionName: https
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

## 9. Create HTTP to HTTPS Redirect

Create `http-redirect.yaml`

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: whoami-http-redirect
  namespace: demo
spec:
  parentRefs:
    - name: kong-gateway
      namespace: kong
      sectionName: http
  hostnames:
    - "whoami.learndevopsnow-mm.blog"
  rules:
    - filters:
        - type: RequestRedirect
          requestRedirect:
            scheme: https
            statusCode: 301
```

Apply:

```bash
kubectl apply -f http-redirect.yaml
```

---

## 10. Verify HTTPRoutes

```bash
kubectl get httproute -n demo
```

```bash
kubectl describe httproute whoami -n demo
```

```bash
kubectl describe httproute whoami-http-redirect -n demo
```

---

## 11. Test HTTPS

```bash
curl https://whoami.learndevopsnow-mm.blog
```

---

## 12. Test HTTP to HTTPS Redirect

```bash
curl -I http://whoami.learndevopsnow-mm.blog
```

Expected:

```text
HTTP/1.1 301 Moved Permanently
Location: https://whoami.learndevopsnow-mm.blog/
```

---

## 13. Test Redirect and Application

```bash
curl -L http://whoami.learndevopsnow-mm.blog
```

---

## Final Architecture

```text
Internet
   │
   ▼
Kong Proxy LoadBalancer
   │
   ▼
kong Namespace
   │
   └── Shared Gateway
       ├── HTTP Listener  :80
       └── HTTPS Listener :443
              │
              └── wildcard-tls
                   │
                   └── *.learndevopsnow-mm.blog

                │
                │ allowedRoutes: All
                ▼

demo Namespace
   │
   ├── HTTPRoute
   │      │
   │      └── whoami-service:80
   │
   └── HTTP Redirect Route
          │
          └── HTTP → HTTPS
```