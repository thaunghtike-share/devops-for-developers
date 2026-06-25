# Kubernetes ServiceAccount Lab

## Lab Objectives

In this lab, you will learn:

- What a ServiceAccount is
- Why Pods use ServiceAccounts
- Default ServiceAccount
- Custom ServiceAccount
- ServiceAccount Token
- automountServiceAccountToken
- ImagePullSecrets with ServiceAccount
- Prepare for RBAC

---

# 1. Create Namespace

```bash
kubectl create namespace serviceaccount-lab
```

Verify

```bash
kubectl get ns
```

---

# 2. Check Default ServiceAccount

Every namespace automatically contains one ServiceAccount.

```bash
kubectl get serviceaccount -n serviceaccount-lab
```

Expected

```text
NAME      SECRETS   AGE
default   0         10s
```

Describe it.

```bash
kubectl describe sa default -n serviceaccount-lab
```

Notice there is nothing special configured.

---

# 3. Deploy a Pod

Create

```bash
vim pod-default.yaml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-default
  namespace: serviceaccount-lab
spec:
  containers:
    - name: nginx
      image: nginx:latest
```

Apply

```bash
kubectl apply -f pod-default.yaml
```

Verify

```bash
kubectl get pod -n serviceaccount-lab
```

---

# 4. Verify Which ServiceAccount Is Used

```bash
kubectl describe pod nginx-default -n serviceaccount-lab
```

Expected

```text
Service Account: default
```

Notice

Even though we never specified

```yaml
serviceAccountName:
```

Kubernetes automatically attached the default ServiceAccount.

---

# 5. Inspect ServiceAccount Token

Enter Pod

```bash
kubectl exec -it nginx-default -n serviceaccount-lab -- sh
```

Check directory

```bash
cd /var/run/secrets/kubernetes.io/serviceaccount

ls
```

Expected

```text
ca.crt
namespace
token
```

Read namespace

```bash
cat namespace
```

Read token

```bash
cat token
```

Exit

```bash
exit
```

---

# 6. Create Custom ServiceAccount

```bash
kubectl create serviceaccount app-sa -n serviceaccount-lab
```

Verify

```bash
kubectl get sa -n serviceaccount-lab
```

---

# 7. Deploy Pod Using Custom ServiceAccount

Create

```bash
vim pod-custom-sa.yaml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-custom
  namespace: serviceaccount-lab
spec:
  serviceAccountName: app-sa
  containers:
    - name: nginx
      image: nginx:latest
```

Apply

```bash
kubectl apply -f pod-custom-sa.yaml
```

Verify

```bash
kubectl describe pod nginx-custom -n serviceaccount-lab
```

Expected

```text
Service Account: app-sa
```

---

# 8. Inspect Custom ServiceAccount Token

```bash
kubectl exec -it nginx-custom -n serviceaccount-lab -- sh
```

```bash
cd /var/run/secrets/kubernetes.io/serviceaccount

ls

cat namespace

cat token
```

Exit

```bash
exit
```

Notice

The Pod now uses the token belonging to **app-sa**.

---

# 9. Use the Kubernetes API

Enter the Pod using the default ServiceAccount.

```bash
kubectl exec -it nginx-default -n serviceaccount-lab -- sh
```

Install curl

```bash
apt update

apt install curl -y
```

Read the token

```bash
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
```

Read the CA certificate

```bash
CACERT=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
```

Call Kubernetes API

```bash
curl --cacert $CACERT -H "Authorization: Bearer $TOKEN" https://kubernetes.default.svc/api
```

You should receive a valid response from the Kubernetes API Server.

Now try listing Pods.

```bash
curl --cacert $CACERT -H "Authorization: Bearer $TOKEN" https://kubernetes.default.svc/api/v1/namespaces/serviceaccount-lab/pods
```

Expected

```text
403 Forbidden
```

Notice

The Pod successfully authenticated using the ServiceAccount token.

However, it is not authorized to list Pods.

This is exactly what RBAC controls.

---

# 10. Create Docker Registry Secret

```bash
kubectl create secret docker-registry dockerhub-secret \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=learndevopsnow123 \
  --docker-password=Tho@861998 \
  -n serviceaccount-lab
```

---

# 11. Attach ImagePullSecret to ServiceAccount

```bash
kubectl patch sa app-sa \
-p '{"imagePullSecrets":[{"name":"dockerhub-secret"}]}' \
-n serviceaccount-lab
```

Verify

```bash
kubectl describe sa app-sa -n serviceaccount-lab
```

Expected

```text
Image pull secrets:
  dockerhub-secret
```

---

# 12. Deploy Private Image

```bash
vim private-app.yaml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: private-app
  namespace: serviceaccount-lab
spec:
  serviceAccountName: app-sa
  containers:
    - name: app
      image: learndevopsnow123/python-flask-app:1.0
```

Notice

No need to define

```yaml
imagePullSecrets:
```

inside the Pod.

The ServiceAccount automatically injects it.

---

# 13. Cleanup

```bash
kubectl delete namespace serviceaccount-lab
```

---

# Summary

You learned

- Every namespace has a default ServiceAccount
- Pods automatically use the default ServiceAccount
- ServiceAccount tokens are automatically mounted
- Custom ServiceAccounts can be attached to Pods
- Token mounting can be disabled
- ServiceAccounts can provide ImagePullSecrets
- Pods can authenticate to the Kubernetes API
- RBAC controls authorization

---

# Next Lab

Kubernetes RBAC

- Role
- ClusterRole
- RoleBinding
- ClusterRoleBinding
- Granting permissions to ServiceAccounts