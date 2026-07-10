# Horizontal Pod Autoscaler (HPA) Lab

Kubernetes Horizontal Pod Autoscaler (HPA) automatically adjusts the number of pod replicas in a Deployment or StatefulSet based on observed CPU/memory utilization or custom metrics. It ensures your application scales out to handle traffic spikes and scales down to save resources when demand drops.

## Prerequisites

- Kubernetes Cluster
- Metrics Server Installed

---

# 1. Verify Metrics Server

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml


kubectl get deployment metrics-server -n kube-system

kubectl patch deployment metrics-server -n kube-system --type=json \
  -p='[
    {
      "op": "add",
      "path": "/spec/template/spec/containers/0/args/-",
      "value": "--kubelet-insecure-tls"
    }
  ]'

kubectl rollout status deployment/metrics-server -n kube-system

kubectl top nodes
kubectl top pods -A
```

---

# 2. Create Namespace

```bash
kubectl create namespace hpa-lab
```

---

# 3. Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  namespace: hpa-lab
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.29
          ports:
            - containerPort: 80
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 256Mi
```

Apply

```bash
kubectl apply -f deployment.yaml
```

---

# 4. Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
  namespace: hpa-lab
spec:
  selector:
    app: nginx
  ports:
    - port: 80
      targetPort: 80
```

Apply

```bash
kubectl apply -f service.yaml
```

---

# 5. Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nginx-hpa
  namespace: hpa-lab
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nginx
  minReplicas: 1
  maxReplicas: 5
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
```

Apply

```bash
kubectl apply -f hpa.yaml
```

---

# 6. Verify HPA

```bash
kubectl get hpa -n hpa-lab

kubectl describe hpa nginx-hpa -n hpa-lab
```

---

# 7. Verify Resources

```bash
kubectl get deployment -n hpa-lab

kubectl get pods -n hpa-lab

kubectl top pods -n hpa-lab
```

---

# 8. Generate Load

Run a temporary BusyBox pod.

```bash
kubectl run load-generator \
  --rm -it \
  --image=busybox \
  -n hpa-lab \
  -- /bin/sh
```

Inside the pod

```sh
for i in $(seq 1 50); do
  while true; do
    wget -q -O- http://nginx.hpa-lab.svc.cluster.local > /dev/null
  done &
done

wait
```

---

# 9. Watch Autoscaling

```bash
kubectl get hpa -w -n hpa-lab
```

```bash
kubectl get pods -w -n hpa-lab
```

```bash
kubectl top pods -n hpa-lab
```

---

# 10. Stop Load

Exit the BusyBox container.

```
Ctrl + C
```

or

```
exit
```

---

# 11. Watch Scale Down

```bash
kubectl get hpa -w -n hpa-lab
```

```bash
kubectl get pods -w -n hpa-lab
```

---

# 12. Cleanup

```bash
kubectl delete namespace hpa-lab
```