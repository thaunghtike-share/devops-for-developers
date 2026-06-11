# Kubernetes Day 3 Lab
## Deployment, ReplicaSet, Scaling, Rolling Update, ClusterIP Service, NodePort Service, Selector Testing

This lab does not include DaemonSet. DaemonSet will be used in Day 4.

---

## Lab Files

- `01-nginx-deployment.yaml`
- `02-nginx-clusterip-service.yaml`
- `03-nginx-nodeport-service.yaml`
- `04-nginx-deployment-v2.yaml`

---

## 1. Create Deployment

```bash
alias k="microk8s kubectl"
k apply -f 01-nginx-deployment.yaml
k get deployment
k get pods
k get pods --show-labels
k get rs
```

Check that all Pods have this label:

```text
app=nginx
```

---

## 2. Check ReplicaSet

```bash
k get rs
k describe deployment nginx-deployment
```

Deployment creates ReplicaSet. ReplicaSet maintains the desired Pod count.

---

## 3. Create ClusterIP Service

```bash
k apply -f 02-nginx-clusterip-service.yaml
k get svc
k describe svc nginx-clusterip
k get pods -o wide 
```

Check this section in service describe output:

```text
Selector: app=nginx
Endpoints: <Pod IPs>
```

The Service uses selector `app=nginx` to find matching Pods.

---

## 4. Test ClusterIP Service with Debug Pod

ClusterIP cannot be accessed directly from outside the cluster.

Create a temporary debug Pod imperatively:

```bash
k run tester --image=busybox --restart=Never -- sleep 3600
k get pods
k get svc
```

Enter the tester Pod:

```bash
k exec -it tester -- sh
```

Test ClusterIP Service by DNS name:

```bash
wget -qO- http://nginx-clusterip
```

Exit tester Pod:

```bash
exit
```

---

## 5. Create NodePort Service

```bash
k apply -f 03-nginx-nodeport-service.yaml
k get svc
k describe svc nginx-nodeport
```

Access from outside using Node IP and NodePort:

```bash
curl http://<NODE_IP>:30080
```

For MicroK8s single-node VM, get node IP:

```bash
k get nodes -o wide
```

Then use:

```bash
curl http://<NODE_INTERNAL_IP>:30080
```

---

## 6. Scale Out Deployment

```bash
k scale deployment nginx-deployment --replicas=6
k get pods
k get rs
k describe svc nginx-clusterip
```

Service endpoints should increase because new Pods also have label:

```text
app=nginx
```

---

## 7. Imperative 
k delete all --all --force
k create deployment nginx-imperative --image=nginx
k get deployment
k get pods
k get rs
k expose deployment nginx-imperative --port=80 --target-port=80
k get svc
k describe svc nginx-imperative

## 8. Scale Deployment

```bash
k edit deployment nginx-imperative 
k scale deployment nginx-imperative --replicas=5
k get pods
```

---

## 9. Clean Up

```bash
k delete all --all --force

or

k delete deployment --all --force
k delete service --all --force
k get all
```
