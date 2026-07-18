# Kubernetes Scheduler Labs

## 1. Check Existing Nodes

```bash
kubectl get nodes -o wide
```

```bash
kubectl get nodes --show-labels
```

---

# Node Labels

## 2. Add Labels to Worker Nodes

Label `worker1` as development node.

```bash
kubectl label node worker1 env=dev --overwrite
```

Label `worker2` as production node.

```bash
kubectl label node worker2 env=prod --overwrite
```

---

## 3. Verify Node Labels

```bash
kubectl get nodes -L env
```

Expected:

```text
NAME            STATUS   ENV
control-plane   Ready
worker1         Ready    dev
worker2         Ready    prod
```

---

# Node Selector

## 4. Create Node Selector Pod

Create file:

```bash
vim node-selector.yaml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-selector
spec:
  nodeSelector:
    env: dev
  containers:
    - name: nginx
      image: nginx:1.29
      ports:
        - containerPort: 80
```

---

## 5. Deploy Pod

```bash
kubectl apply -f node-selector.yaml
```

---

## 6. Verify Pod Placement

```bash
kubectl get pod nginx-selector -o wide
```

```bash
kubectl describe pod nginx-selector
```

Expected:

```text
Node: worker1
```

---

## 7. Delete Pod

```bash
kubectl delete -f node-selector.yaml
```

---

# Taints and Tolerations

## 8. Add Taint to Worker Node

Add production taint to worker2.

```bash
kubectl taint node worker2 env=prod:NoSchedule
```

---

## 9. Verify Taint

```bash
kubectl describe node worker2 | grep Taints
```

Expected:

```text
Taints: env=prod:NoSchedule
```

---

# Pod Without Toleration

## 10. Create Pod Without Toleration

Create file:

```bash
vim no-toleration.yaml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-no-toleration
spec:
  nodeSelector:
    env: prod
  containers:
    - name: nginx
      image: nginx:1.29
      ports:
        - containerPort: 80
```

---

## 11. Deploy

```bash
kubectl apply -f no-toleration.yaml
```

---

## 12. Verify

```bash
kubectl get pod nginx-no-toleration -o wide
```

```bash
kubectl describe pod nginx-no-toleration
```

Expected:

```text
STATUS: Pending
```

Reason:

```text
had untolerated taint {env: prod}
```

---

## 13. Delete Pod

```bash
kubectl delete -f no-toleration.yaml
```

---

# Pod With Toleration

## 14. Create Pod With Toleration

Create file:

```bash
vim toleration.yaml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-toleration
spec:
  nodeSelector:
    env: prod
  tolerations:
    - key: env
      operator: Equal
      value: prod
      effect: NoSchedule
  containers:
    - name: nginx
      image: nginx:1.29
      ports:
        - containerPort: 80
```

---

## 15. Deploy

```bash
kubectl apply -f toleration.yaml
```

---

## 16. Verify

```bash
kubectl get pod nginx-toleration -o wide
```

```bash
kubectl describe pod nginx-toleration
```

Expected:

```text
Node: worker2
```

---

## 17. Delete Pod

```bash
kubectl delete -f toleration.yaml
```

---

# Cleanup

## 18. Remove Taint

```bash
kubectl taint node worker2 env=prod:NoSchedule-
```

Verify:

```bash
kubectl describe node worker2 | grep Taints
```

Expected:

```text
Taints: <none>
```

---

## 19. Remove Labels

```bash
kubectl label node worker1 env-
```

```bash
kubectl label node worker2 env-
```

---

## 20. Final Verification

```bash
kubectl get nodes -L env
```

```bash
kubectl get pods -o wide
```