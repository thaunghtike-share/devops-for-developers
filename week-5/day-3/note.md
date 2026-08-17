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
```

## ClusterIP Test

```bash
kubectl run tester --image=busybox --restart=Never -- sleep 3600
kubectl exec -it tester -- sh
wget -qO- http://nginx-clusterip.default.svc.cluster.local
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

## Rolling Upgrade

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
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
          image: nginx:alpine
          ports:
            - containerPort: 80
```

```bash
vim nginx-deployment-v2.yaml
kubectl apply -f nginx-deployment-v2.yaml
kubectl rollout status deployment/nginx-deployment
kubectl set image deployment/nginx-deployment nginx=nginx:latest
kubectl rollout status deployment/nginx-deployment
kubectl get pods
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
