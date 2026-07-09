# Kubeadm Cluster Upgrade Lab

```text
Start:  v1.35.6
Target: v1.36.2
```

```text
control-plane   172.20.20.10
worker1         172.20.20.11
worker2         172.20.20.12
```

---

## 1. Check Current Version

control-plane:

```bash
kubectl get nodes -o wide
kubelet --version
kubeadm version -o short
kubectl version --client
```

---

## 2. Set Target Repo on Control Plane

control-plane:

```bash
sudo cat /etc/apt/sources.list.d/kubernetes.list


echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.36/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update
```

```bash
apt-cache madison kubeadm
apt-cache madison kubelet
apt-cache madison kubectl
```

---

## 3. Upgrade Control Plane kubeadm

control-plane:

```bash
sudo apt-mark unhold kubeadm
sudo apt-get install -y kubeadm=1.36.2-2.1
sudo apt-mark hold kubeadm
```

```bash
kubeadm version -o short
```

---

## 4. Upgrade Plan

control-plane:

```bash
sudo kubeadm upgrade plan
```

---

## 5. Upgrade Control Plane Components

control-plane:

```bash
sudo kubeadm upgrade apply v1.36.2
```

```bash
kubectl get nodes
kubectl get pods -n kube-system
sudo cat /etc/kubernetes/manifests/kube-apiserver.yaml 
```

---

## 6. Drain Control Plane

control-plane:

```bash
kubectl drain control-plane \
  --ignore-daemonsets \
  --delete-emptydir-data \
  --force
```

---

## 7. Upgrade Control Plane kubelet and kubectl

control-plane:

```bash
sudo apt-mark unhold kubelet kubectl
sudo apt-get install -y kubelet=1.36.2-2.1 kubectl=1.36.2-2.1
sudo apt-mark hold kubelet kubectl
```

```bash
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

```bash
kubelet --version
kubectl version --client
kubectl get nodes -o wide
```

```bash
kubectl uncordon control-plane
kubectl get nodes -o wide
```

---

## 8. Drain worker1

control-plane:

```bash
kubectl create deploy nginx --image=nginx --replicas=2
kubectl get pods -o wide
```

```bash
kubectl drain worker1 \
  --ignore-daemonsets \
  --delete-emptydir-data
```

```bash
kubectl get pods -o wide
kubectl get events --sort-by=.lastTimestamp
```

---

## 9. Upgrade worker1

Mac terminal:

```bash
cd /Users/mac/Desktop/workspace/class/kubeadm
vagrant ssh worker1
```

worker1:

```bash
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.36/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update
```

```bash
sudo apt-mark unhold kubeadm
sudo apt-get install -y kubeadm=1.36.2-2.1
sudo apt-mark hold kubeadm
```

```bash
sudo kubeadm upgrade node
```

```bash
sudo apt-mark unhold kubelet kubectl
sudo apt-get install -y kubelet=1.36.2-2.1 kubectl=1.36.2-2.1
sudo apt-mark hold kubelet kubectl
```

```bash
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

```bash
kubeadm version -o short
kubelet --version
kubectl version --client
```

control-plane:

```bash
kubectl uncordon worker1
kubectl get nodes -o wide
kubectl get pods -o wide
```

---

## 10. Drain worker2

control-plane:

```bash
kubectl get pods -o wide
```

```bash
kubectl drain worker2 \
  --ignore-daemonsets \
  --delete-emptydir-data
```

```bash
kubectl get pods -o wide
kubectl get events --sort-by=.lastTimestamp
```

---

## 11. Upgrade worker2

Mac terminal:

```bash
cd /Users/mac/Desktop/workspace/class/kubeadm
vagrant ssh worker2
```

worker2:

```bash
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.36/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update
```

```bash
sudo apt-mark unhold kubeadm
sudo apt-get install -y kubeadm=1.36.2-2.1
sudo apt-mark hold kubeadm
```

```bash
sudo kubeadm upgrade node
```

```bash
sudo apt-mark unhold kubelet kubectl
sudo apt-get install -y kubelet=1.36.2-2.1 kubectl=1.36.2-2.1
sudo apt-mark hold kubelet kubectl
```

```bash
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

```bash
kubeadm version -o short
kubelet --version
kubectl version --client
```

control-plane:

```bash
kubectl uncordon worker2
kubectl get nodes -o wide
kubectl get pods -o wide
```

---

## 12. Final Check

control-plane:

```bash
kubectl get nodes -o wide
kubectl get pods -A
kubectl get deployment,pods -o wide
kubectl version
kubeadm version -o short
kubelet --version
kubectl version --client
```

```bash
kubectl get --raw='/readyz?verbose'
```

```bash
sudo apt-mark showhold
```

---

## 13. Cleanup

control-plane:

```bash
kubectl delete deployment nginx
```

---

## 14. Troubleshooting

control-plane:

```bash
kubectl get nodes
kubectl describe node control-plane
kubectl describe node worker1
kubectl describe node worker2
kubectl get pods -A -o wide
kubectl get events -A --sort-by=.lastTimestamp
```

node with issue:

```bash
sudo systemctl status kubelet --no-pager
sudo journalctl -u kubelet -n 80 --no-pager
```
