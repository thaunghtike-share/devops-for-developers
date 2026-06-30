````markdown
# Kubernetes Authentication Lab

## Create a Developer Kubeconfig with Access to dev and uat Namespaces

## Objectives

In this lab, you will learn:

- Create a Kubernetes user using Client Certificates
- Generate a Private Key
- Generate a Certificate Signing Request (CSR)
- Sign a Certificate using the Kubernetes CA
- Create a Developer kubeconfig
- Test Authentication
- Grant permissions using RBAC
- Verify namespace access

---

# 1. Generate Developer Private Key

```bash
openssl genrsa -out developer.key 2048
```

Verify

```bash
ls -l developer.key
```

---

# 2. Generate Certificate Signing Request

```bash
openssl req -new \
  -key developer.key \
  -out developer.csr \
  -subj "/CN=developer/O=developers"
```

Verify

```bash
openssl req -text -noout -in developer.csr
```

Expected

```text
Subject:
    CN = developer
    O = developers
```

---

# 3. Sign the Certificate using Kubernetes CA

Run this on the control-plane node.

```bash
sudo openssl x509 \
  -req \
  -in developer.csr \
  -CA /etc/kubernetes/pki/ca.crt \
  -CAkey /etc/kubernetes/pki/ca.key \
  -CAcreateserial \
  -out developer.crt \
  -days 365
```

Verify

```bash
openssl x509 -text -noout -in developer.crt
```

Expected

```text
Subject:
    CN = developer
    O = developers

Issuer:
    Kubernetes CA
```

---

# 4. Get the Kubernetes API Server Address

```bash
API_SERVER=$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}')

echo $API_SERVER
```

---

# 5. Create Developer kubeconfig

Create the cluster entry.

```bash
kubectl config set-cluster kubernetes \
  --server=$API_SERVER \
  --certificate-authority=/etc/kubernetes/pki/ca.crt \
  --embed-certs=true \
  --kubeconfig=developer.conf
```

Create the user entry.

```bash
kubectl config set-credentials developer \
  --client-certificate=developer.crt \
  --client-key=developer.key \
  --embed-certs=true \
  --kubeconfig=developer.conf
```

Create the context.

```bash
kubectl config set-context developer-context \
  --cluster=kubernetes \
  --user=developer \
  --kubeconfig=developer.conf
```

Use the context.

```bash
kubectl config use-context developer-context \
  --kubeconfig=developer.conf
```

Verify

```bash
kubectl config view --kubeconfig=developer.conf
```

---

# 6. Test Authentication

```bash
kubectl --kubeconfig=developer.conf get pods
```

Expected

```text
Error from server (Forbidden)
```

Authentication is successful.

Authorization has not been configured yet.

---

# 7. Create Namespaces

```bash
kubectl create namespace dev

kubectl create namespace uat
```

Verify

```bash
kubectl get ns
```

---

# 8. Create Role for dev Namespace

Create

```bash
vim dev-role.yaml
```

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer-full-access
  namespace: dev
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]
```

Apply

```bash
kubectl apply -f dev-role.yaml
```

---

# 9. Create RoleBinding for dev

Create

```bash
vim dev-rolebinding.yaml
```

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: developer-binding
  namespace: dev
subjects:
- kind: User
  name: developer
  apiGroup: rbac.authorization.k8s.io

roleRef:
  kind: Role
  name: developer-full-access
  apiGroup: rbac.authorization.k8s.io
```

Apply

```bash
kubectl apply -f dev-rolebinding.yaml
```

# 10. Test Access to dev

```bash
kubectl --kubeconfig=developer.conf get pods -n dev
```

Create a Pod.

```bash
kubectl --kubeconfig=developer.conf run nginx-dev \
  --image=nginx \
  -n dev
```

Verify

```bash
kubectl --kubeconfig=developer.conf get pods -n dev
```

---

# 11. Create Role for uat Namespace

Create

```bash
vim uat-role.yaml
```

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer-full-access
  namespace: uat
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]
```

Apply

```bash
kubectl apply -f uat-role.yaml
```

---

# 12. Create RoleBinding for uat

Create

```bash
vim uat-rolebinding.yaml
```

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: developer-binding
  namespace: uat
subjects:
- kind: User
  name: developer
  apiGroup: rbac.authorization.k8s.io

roleRef:
  kind: Role
  name: developer-full-access
  apiGroup: rbac.authorization.k8s.io
```

Apply

```bash
kubectl apply -f uat-rolebinding.yaml
```

# 13. Test Access to uat

```bash
kubectl --kubeconfig=developer.conf get pods -n uat
```

Create a Pod.

```bash
kubectl --kubeconfig=developer.conf run nginx-uat \
  --image=nginx \
  -n uat
```

Verify

```bash
kubectl --kubeconfig=developer.conf get pods -n uat
```

---

# 14. Verify Access to default Namespace

```bash
kubectl --kubeconfig=developer.conf get pods -n default
```

Expected

```text
Error from server (Forbidden)
```

---

# 15. Share kubeconfig to the Developer 

copy it to the default kubeconfig location.

```bash
mkdir -p ~/.kube

cp developer.conf ~/.kube/config
```

Verify

```bash
kubectl get pods -n dev
```

---

# 16. Cleanup

```bash
kubectl delete pod nginx-dev -n dev

kubectl delete pod nginx-uat -n uat
```

```bash
kubectl delete rolebinding developer-binding -n dev
kubectl delete role developer-full-access -n dev

kubectl delete rolebinding developer-binding -n uat
kubectl delete role developer-full-access -n uat
```

```bash
rm developer.key
rm developer.csr
rm developer.crt
rm developer.conf
```

---

# Summary

In this lab, you learned:

- Generate a Client Certificate
- Create a Kubernetes user identity
- Build a kubeconfig
- Authenticate to the Kubernetes API Server
- Grant namespace permissions using RBAC
- Restrict a user to specific namespaces
- Verify Authentication and Authorization
````