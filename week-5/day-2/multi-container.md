# Lab — kubectl + Single Pod + Multi-Container Pod + Init Container

## 1. Configure kubectl for MicroK8s

```bash
mkdir -p ~/.kube
microk8s config > ~/.kube/config
chmod 600 ~/.kube/config

kubectl get nodes
kubectl get pods -A
```

---

# Single Nginx Pod

## 2. Create Nginx Pod

```bash
kubectl run nginx --image=nginx:alpine

kubectl get pods
kubectl get pod nginx -o wide
kubectl describe pod nginx
```

## 3. Check Pod Logs

```bash
kubectl logs nginx
```

## 4. Exec Into Nginx Container

```bash
kubectl exec -it nginx -- sh

nginx -v
ps
exit
```

## 5. Delete Nginx Pod

```bash
kubectl delete pod nginx
kubectl get pods
```

---

# Multi-Container Pod

## 6. Create Multi-Container Pod YAML

```bash
vim pod.yaml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
spec:
  containers:
    - name: client
      image: alpine
      command: ["/bin/sh", "-c"]
      args:
        - |
          while true; do
            echo "Calling Nginx through localhost..."
            wget -qO- http://localhost:8080
            sleep 10
          done

    - name: nginx
      image: nginx:alpine
      ports:
        - containerPort: 8080
      command: ["/bin/sh", "-c"]
      args:
        - |
          sed -i 's/listen       80;/listen       8080;\n    listen       [::]:8080;/g' /etc/nginx/conf.d/default.conf
          nginx -g "daemon off;"
```

## 7. Create and Verify Multi-Container Pod

```bash
kubectl apply -f pod.yaml

kubectl get pods
kubectl get pods -o wide
kubectl describe pod multi-container-pod
```

## 8. Check Container Logs

```bash
# Client Container
kubectl logs multi-container-pod -c client
kubectl logs -f multi-container-pod -c client

# Nginx Container
kubectl logs multi-container-pod -c nginx
```

## 9. Exec Into Client Container

```bash
kubectl exec -it multi-container-pod -c client -- sh

wget -qO- http://localhost:8080

exit
```

## 10. Exec Into Nginx Container

```bash
kubectl exec -it multi-container-pod -c nginx -- sh

wget -qO- http://localhost:8080

exit
```

## 11. Delete Multi-Container Pod

```bash
kubectl delete -f multi-container-pod.yaml
kubectl get pods
```