# AWS Certificate Manager - HTTPS Lab

# Verify Current Ingress

```bash
kubectl get ingress -n dev
kubectl get ingress -n prod
```

---

# Verify Current HTTP Access

```bash
curl -I http://app1.dev.learndevopsnow-mm.blog
curl -I http://app2.dev.learndevopsnow-mm.blog
curl -I http://app1.prod.learndevopsnow-mm.blog
curl -I http://app2.prod.learndevopsnow-mm.blog
```

---

# Request Certificate

Open AWS Certificate Manager.

Select:

```text
Request a public certificate
```

Domain name:

```text
*.dev.learndevopsnow-mm.blog
*.prod.learndevopsnow-mm.blog
```

Validation method:

```text
DNS validation
```

Key algorithm:

```text
RSA 2048
```

Request the certificate.

---

# Development App 1 Ingress

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
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP":80},{"HTTPS":443}]'
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:ap-southeast-1:265193792623:certificate/e757006b-e5d9-421f-954a-850a1b75a9f1
    alb.ingress.kubernetes.io/ssl-redirect: "443"
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

---

# Development App 2 Ingress

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
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP":80},{"HTTPS":443}]'
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:ap-southeast-1:265193792623:certificate/e757006b-e5d9-421f-954a-850a1b75a9f1
    alb.ingress.kubernetes.io/ssl-redirect: "443"
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

---

# Apply Development Ingress

```bash
kubectl apply -f dev-app1-ingress-https.yaml
kubectl apply -f dev-app2-ingress-https.yaml
```

---

# Verify Development Ingress

```bash
kubectl get ingress -n dev
```

```bash
kubectl describe ingress app1 -n dev
```

```bash
kubectl describe ingress app2 -n dev
```

---

# Verify Development ALB

Open:

```text
EC2 Dashboard
→ Load Balancers
→ Development ALB
→ Listeners and rules
```

Verify:

```text
HTTP : 80
HTTPS : 443
```

The HTTP Listener should redirect requests to HTTPS Port 443.

The HTTPS Listener should contain the App 1 and App 2 Host Header Rules.

Verify that the Development ACM certificate is attached to the HTTPS Listener.

---

# Test Development HTTPS

```bash
curl -I https://app1.dev.learndevopsnow-mm.blog
curl -I https://app2.dev.learndevopsnow-mm.blog
```

Browser:

```text
https://app1.dev.learndevopsnow-mm.blog
```

```text
https://app2.dev.learndevopsnow-mm.blog
```

---

# Verify Development HTTP to HTTPS Redirect

```bash
curl -I http://app1.dev.learndevopsnow-mm.blog
```

```bash
curl -I http://app2.dev.learndevopsnow-mm.blog
```

Expected:

```text
HTTP/1.1 301 Moved Permanently
```

The `Location` header should point to the HTTPS URL.

---

# Production App 1 Ingress

Create:

```text
prod-app1-ingress-https.yaml
```

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app1
  namespace: prod
  annotations:
    alb.ingress.kubernetes.io/group.name: prod
    alb.ingress.kubernetes.io/group.order: "10"
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP":80},{"HTTPS":443}]'
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:ap-southeast-1:265193792623:certificate/dc920831-66a3-490d-a9a7-7868a4a1fd2f
    alb.ingress.kubernetes.io/ssl-redirect: "443"
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

---

# Production App 2 Ingress

Create:

```text
prod-app2-ingress-https.yaml
```

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app2
  namespace: prod
  annotations:
    alb.ingress.kubernetes.io/group.name: prod
    alb.ingress.kubernetes.io/group.order: "20"
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP":80},{"HTTPS":443}]'
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:ap-southeast-1:ACCOUNT_ID:certificate/PROD_CERTIFICATE_ID
    alb.ingress.kubernetes.io/ssl-redirect: "443"
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

---

# Apply Production Ingress

```bash
kubectl apply -f prod-app1-ingress-https.yaml
kubectl apply -f prod-app2-ingress-https.yaml
```

---

# Verify Production Ingress

```bash
kubectl get ingress -n prod
```

```bash
kubectl describe ingress app1 -n prod
```

```bash
kubectl describe ingress app2 -n prod
```

---

# Verify Production ALB

Open:

```text
EC2 Dashboard
→ Load Balancers
→ Production ALB
→ Listeners and rules
```

Verify:

```text
HTTP : 80
HTTPS : 443
```

The HTTP Listener should redirect requests to HTTPS Port 443.

The HTTPS Listener should contain the App 1 and App 2 Host Header Rules.

Verify that the Production ACM certificate is attached to the HTTPS Listener.

---

# Test Production HTTPS

```bash
curl -I https://app1.prod.learndevopsnow-mm.blog
curl -I https://app2.prod.learndevopsnow-mm.blog
```

Browser:

```text
https://app1.prod.learndevopsnow-mm.blog
```

```text
https://app2.prod.learndevopsnow-mm.blog
```

---

# Verify Production HTTP to HTTPS Redirect

```bash
curl -I http://app1.prod.learndevopsnow-mm.blog
```

```bash
curl -I http://app2.prod.learndevopsnow-mm.blog
```

Expected:

```text
HTTP/1.1 301 Moved Permanently
```

The `Location` header should point to the HTTPS URL.

---

# Verify All Ingress Resources

```bash
kubectl get ingress -A
```

---

# Final Test

```bash
curl -IL http://app1.dev.learndevopsnow-mm.blog
curl -IL http://app2.dev.learndevopsnow-mm.blog
curl -IL http://app1.prod.learndevopsnow-mm.blog
curl -IL http://app2.prod.learndevopsnow-mm.blog
```