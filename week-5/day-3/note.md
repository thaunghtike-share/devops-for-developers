# Kubernetes Deployment and Service Lab

## Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 5
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
          image: nginx:1.25.5
          ports:
            - containerPort: 80
```

```bash
vim nginx-deployment.yaml
kubectl apply -f nginx-deployment.yaml
kubectl get deployment
kubectl get pods --show-labels
kubectl get rs
```

## Rolling Update

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 5
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
          image: nginx:latest
          ports:
            - containerPort: 80
```

```bash
vim nginx-deployment.yaml
kubectl apply -f nginx-deployment.yaml
watch kubectl get pods
kubectl describe deployment nginx-deployment
```

```bash
kubectl create deployment nginx-imperative --image=nginx:latest --replicas=2

kubectl get deployments
kubectl get pods
kubectl get rs

kubectl scale deployment nginx-imperative --replicas=4

kubectl delete deployment nginx-imperative
```

## ClusterIP Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-clusterip
spec:
  type: ClusterIP
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```

```bash
vim nginx-clusterip.yaml
kubectl apply -f nginx-clusterip.yaml
kubectl get svc
kubectl describe svc nginx-clusterip
kubectl get pods -o wide
```

## ClusterIP Test

```bash
kubectl run tester --image=busybox --restart=Never -- sleep 3600
kubectl get pods
kubectl exec -it tester -- sh
wget -qO- http://10.152.183.189 
wget -qO- http://nginx-clusterip.default.svc
kubectl delete pod tester --force
exit
```

## NodePort Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-nodeport
spec:
  type: NodePort
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
      nodePort: 30080
```

```bash
vim nginx-nodeport.yaml
kubectl apply -f nginx-nodeport.yaml
kubectl get svc
kubectl describe svc nginx-nodeport
curl http://<NODE_IP>:30080
```

## Scale

```bash
kubectl scale deployment nginx-deployment --replicas=6
kubectl get pods
kubectl get rs
```

## Clean Up

```bash
kubectl delete all --all --force
```
