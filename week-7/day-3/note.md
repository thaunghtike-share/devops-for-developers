# 🔐 Kubernetes RBAC Full Lab (Role + ClusterRole + ServiceAccount + CronJob Concept)

## 🎯 Objective

In this lab, you will learn:

- What ServiceAccount is
- How Kubernetes authenticates Pods
- How Authorization works using RBAC
- Difference between Role and ClusterRole
- Real production-style usage (CronJob / kubectl inside Pod)
- How API Server is discovered inside Pod

---

# 🧱 RBAC CORE FLOW

ServiceAccount → Identity  
Token → Authentication  
Role / ClusterRole → Permissions  
RoleBinding / ClusterRoleBinding → Attach permissions  

---

# 📦 1. Create Namespace

```bash
kubectl create namespace rbac-lab
```

---

# 👤 2. Create ServiceAccount

```bash
kubectl create serviceaccount app-sa -n rbac-lab
```

---

# 🚀 3. Create Test Pod (kubectl container)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: rbac-test
  namespace: rbac-lab
spec:
  serviceAccountName: app-sa
  containers:
    - name: kubectl
      image: bitnami/kubectl:latest
      command: ["sleep", "3600"]
```

Apply:

```bash
kubectl apply -f pod.yaml
```

---

# ❌ 4. Test Without RBAC (Expected FAIL)

```bash
kubectl exec -it rbac-test -n rbac-lab -- sh
kubectl get pods -n rbac-lab
```

Expected:

```
Error from server (Forbidden)
```

---

# 🔐 5. Create Role (Namespace Scope)

Role works ONLY inside one namespace.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: rbac-lab
rules:
  - apiGroups: [""]
    resources: ["pods", "deployments", "secrets"]
    verbs: ["get", "list", "delete", "create"]
```

Apply:

```bash
kubectl apply -f role.yaml
```

---

# 🔗 6. Create RoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pod-reader-binding
  namespace: rbac-lab
subjects:
  - kind: ServiceAccount
    name: app-sa
    namespace: rbac-lab
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

Apply:

```bash
kubectl apply -f rolebinding.yaml
```

---

# 🌐 7. Create ClusterRole (Cluster Scope)

ClusterRole works across entire cluster.

Real use case: node access

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: node-reader
rules:
  - apiGroups: [""]
    resources: ["nodes"]
    verbs: ["get", "list"]
```

Apply:

```bash
kubectl apply -f clusterrole.yaml
```

---

# 🔗 8. Create ClusterRoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: node-reader-binding
subjects:
  - kind: ServiceAccount
    name: app-sa
    namespace: rbac-lab
roleRef:
  kind: ClusterRole
  name: node-reader
  apiGroup: rbac.authorization.k8s.io
```

Apply:

```bash
kubectl apply -f clusterrolebinding.yaml
```

---

# 🧪 9. Test RBAC (Inside Pod)

```bash
kubectl exec -it rbac-test -n rbac-lab -- sh
```

### Test Nodes access

```bash
kubectl get nodes
```

# ⚠️ IMPORTANT CONCEPT

Authentication ≠ Authorization

```
Token valid ✔ → Authentication OK
No RBAC      ❌ → Forbidden
```

---

# 🧠 FINAL KEY IDEA

ServiceAccount = Identity  
RBAC = Permission  
ClusterRole = Cluster-wide permission  

---

# 🚀 OUTRO

Kubernetes separates:

- Who you are (ServiceAccount)
- How you login (Token)
- What you can do (RBAC)

Next: production RBAC design patterns (CI/CD + multi-team + security model)