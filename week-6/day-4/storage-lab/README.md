# Kubernetes Storage Lab

YAML/script notes: [note.md](note.md)

## Files

```bash
ls -1 manifests
```

```text
1-empty-dir.yaml
2-host-path.yaml
3-pv-pvc.yaml
4-postgres-hostpath.yaml
5-postgres-local-path.yaml
6-ebs-storage-class.yaml
7-postgres-ebs.yaml
```

## Fix Kubelet Node IP for Vagrant kubeadm

```bash
kubectl get nodes -o wide
```

If both nodes show `10.0.2.15`, set kubelet to use the Vagrant private network IPs.

### Control Plane

```bash
sudo sed -i 's|KUBELET_KUBEADM_ARGS="|KUBELET_KUBEADM_ARGS="--node-ip=172.20.20.10 |' /var/lib/kubelet/kubeadm-flags.env
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

### Worker Node

```bash
sudo sed -i 's|KUBELET_KUBEADM_ARGS="|KUBELET_KUBEADM_ARGS="--node-ip=172.20.20.11 |' /var/lib/kubelet/kubeadm-flags.env
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

### Verify

```bash
kubectl get nodes -o wide
```

Expected:

```text
control-plane   Ready   control-plane   ...   172.20.20.10
worker          Ready   <none>          ...   172.20.20.11
```

## 0. Namespace

```bash
kubectl create namespace storage-lab
kubectl get namespace storage-lab
```

## 1. emptyDir

```bash
kubectl apply -f manifests/1-empty-dir.yaml
POD_NAME=$(kubectl get pod -n storage-lab -l app=emptydir-demo -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it -n storage-lab $POD_NAME -- sh
```

```bash
echo "hello emptydir" > /data/test.txt
cat /data/test.txt
exit
```

```bash
kubectl rollout restart deployment/emptydir-demo -n storage-lab
kubectl get pods -n storage-lab
POD_NAME=$(kubectl get pod -n storage-lab -l app=emptydir-demo -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it -n storage-lab $POD_NAME -- sh
```

```bash
cat /data/test.txt
exit
```

## 2. hostPath

```bash
kubectl apply -f manifests/2-host-path.yaml
POD_NAME=$(kubectl get pod -n storage-lab -l app=hostpath-demo -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it -n storage-lab $POD_NAME -- sh
```

```bash
echo "hello hostpath" > /storage/test.txt
cat /storage/test.txt
exit
```

```bash
kubectl rollout restart deployment/hostpath-demo -n storage-lab
kubectl rollout status deployment/hostpath-demo -n storage-lab
POD_NAME=$(kubectl get pod -n storage-lab -l app=hostpath-demo -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it -n storage-lab $POD_NAME -- sh
```

```bash
cat /storage/test.txt
exit
```

## 3. PV and PVC

```bash
sudo mkdir -p /data/postgres
sudo chmod 777 /data/postgres
kubectl apply -f manifests/3-pv-pvc.yaml
kubectl get pv
kubectl get pvc -n storage-lab
```

## 4. PostgreSQL with hostPath PV

```bash
kubectl apply -f manifests/4-postgres-hostpath.yaml
kubectl rollout status statefulset/postgres-hostpath -n storage-lab
kubectl exec -it -n storage-lab postgres-hostpath-0 -- bash
```

```bash
psql -U postgres
```

```sql
CREATE DATABASE demo;
\l
\q
```

```bash
exit
```

```bash
kubectl rollout restart statefulset/postgres-hostpath -n storage-lab
kubectl rollout status statefulset/postgres-hostpath -n storage-lab
kubectl exec -it -n storage-lab postgres-hostpath-0 -- bash
```

```bash
psql -U postgres
```

```sql
\l
\q
```

```bash
exit
```

```bash
kubectl get pvc -n storage-lab
kubectl get pv
```

## 5. Install local-path

```bash
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml
kubectl get storageclass
kubectl get deployment -n local-path-storage
```

## 6. PostgreSQL with local-path

```bash
kubectl apply -f manifests/5-postgres-local-path.yaml
kubectl rollout status statefulset/postgres-local-path -n storage-lab
kubectl get pvc -n storage-lab
kubectl get pv
kubectl exec -it -n storage-lab postgres-local-path-0 -- bash
```

```bash
psql -U postgres
```

```sql
CREATE DATABASE localdemo;
\l
\q
```

```bash
exit
```

## 7. AWS EBS CSI Driver

```bash
eksctl create addon \
  --name aws-ebs-csi-driver \
  --cluster <cluster-name> \
  --region <region> \
  --service-account-role-arn <role-arn> \
  --force
```

```bash
kubectl get daemonset -n kube-system | grep ebs-csi
kubectl get deployment -n kube-system | grep ebs-csi
```

## 8. AWS EBS StorageClass

```bash
kubectl apply -f manifests/6-ebs-storage-class.yaml
kubectl get storageclass
```

## 9. PostgreSQL with AWS EBS

```bash
kubectl apply -f manifests/7-postgres-ebs.yaml
kubectl rollout status statefulset/postgres-ebs -n storage-lab
kubectl get pvc -n storage-lab
kubectl get pv
kubectl exec -it -n storage-lab postgres-ebs-0 -- bash
```

```bash
psql -U postgres
```

```sql
CREATE DATABASE ebsdemo;
\l
\q
```

```bash
exit
```

```bash
aws ec2 describe-volumes \
  --filters Name=tag:kubernetes.io/created-for/pvc/namespace,Values=storage-lab
```

## 10. Cleanup

```bash
kubectl delete -f manifests/7-postgres-ebs.yaml --ignore-not-found
kubectl delete -f manifests/6-ebs-storage-class.yaml --ignore-not-found
kubectl delete -f manifests/5-postgres-local-path.yaml --ignore-not-found
kubectl delete -f manifests/4-postgres-hostpath.yaml --ignore-not-found
kubectl delete -f manifests/3-pv-pvc.yaml --ignore-not-found
kubectl delete -f manifests/2-host-path.yaml --ignore-not-found
kubectl delete -f manifests/1-empty-dir.yaml --ignore-not-found
kubectl delete namespace storage-lab --ignore-not-found
sudo rm -rf /data/hostpath-demo
sudo rm -rf /data/postgres
```

```bash
kubectl delete -f https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml --ignore-not-found
```
