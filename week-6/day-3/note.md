# Kubernetes Kubeconfig & Contexts

## 1. Why kubectl Works

```bash
kubectl get nodes
```

Ask how kubectl knows which API Server to contact.

---

## 2. kubeconfig File Location

```bash
ls -l ~/.kube/config
```

kubectl uses this file to connect to the cluster.

---

## 3. View Kubeconfig

```bash
kubectl config view
```

kubeconfig contains three main sections.

```yaml
clusters:
users:
contexts:
```

---

## 4. Clusters Section

```bash
kubectl config view
```

* API Server URL
* Certificate Authority

This section stores these values.

---

## 5. Users Section

```bash
kubectl config view
```

* Authentication Information
* kubernetes-admin user

This section stores these values.

---

## 6. Contexts Section

```bash
kubectl config view
```

A context combines:

```text
Cluster + User + Namespace
```

---

## 7. Current Context

```bash
kubectl config current-context
```

Output:

```text
kubernetes-admin@kubernetes
```

This is the context currently used by kubectl.

---

## 8. Existing Contexts

```bash
kubectl config get-contexts
```

You should see that only one context currently exists.

---

## 9. Create Namespaces

```bash
kubectl create namespace dev
kubectl create namespace prod
```

---

## 10. Create New Contexts

```bash
kubectl config set-context dev-context \
  --cluster=kubernetes \
  --user=kubernetes-admin \
  --namespace=dev
```

```bash
kubectl config set-context prod-context \
  --cluster=kubernetes \
  --user=kubernetes-admin \
  --namespace=prod
```

---

## 11. Verify Contexts

```bash
kubectl config get-contexts
```

Output:

```text
CURRENT   NAME
*         kubernetes-admin@kubernetes
          dev-context
          prod-context
```

You should now see the newly created contexts.

---

## 12. Create Pods 

```bash
kubectl run default-pod --image=nginx --restart=Never

kubectl run dev-pod --image=nginx --restart=Never -n dev

kubectl run prod-pod --image=nginx --restart=Never -n prod

kubectl get pods
kubectl get pods -n dev
kubectl get pods -n prod

```

## 13. Switch Context

```bash
kubectl config use-context dev-context
```

Verify:

```bash
kubectl config current-context
```

Output:

```text
dev-context
```

---

## 14. Check Current Namespace

```bash
kubectl config view --minify
```

Namespace:

```text
dev
```

You should see that it has changed to this namespace.

---

## 15. Switch to Production

```bash
kubectl config use-context prod-context
```

Verify:

```bash
kubectl config view --minify
```

Namespace:

```text
prod
```

---

## Summary

Cluster = API Server Information

User = Authentication Information

Context = Cluster + User + Namespace

kubectl = connects to the API Server by using kubeconfig and the current context.
