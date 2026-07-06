# Kubeadm Certificate Management Lab

Beginner lab for kubeadm certificate commands.

Cluster:

```text
control-plane   172.20.20.10
worker1         172.20.20.11
worker2         172.20.20.12
```

---

## 1. Start Vagrant Cluster

Run on your Mac terminal.

```bash
cd /Users/mac/Desktop/workspace/class/kubeadm
vagrant status
vagrant up
vagrant ssh control-plane
```

---

## 2. Check Cluster

Run on `control-plane`.

```bash
sudo ls -l /etc/kubernetes/pki
sudo ls -l /etc/kubernetes/pki/etcd
```

---

## 3. Check Certificate Expiration

Run on `control-plane`.

```bash
sudo kubeadm certs check-expiration
```

---

## 4. Check Certificate Files

Check API server certificate.

```bash
sudo openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text -noout
```

---

## 5. Backup Certificates

Run on `control-plane`.

```bash
sudo cp -r /etc/kubernetes/pki /etc/kubernetes/pki-backup
sudo cp /etc/kubernetes/admin.conf /etc/kubernetes/admin.conf.backup
```

Check backup.

```bash
sudo ls -ld /etc/kubernetes/pki-backup
sudo ls -l /etc/kubernetes/admin.conf.backup
```

---

## 6. Renew API Server Certificate Only

Run on `control-plane`.

```bash
sudo kubeadm certs renew apiserver
```

Check again.

```bash
sudo kubeadm certs check-expiration
```

Restart API server static Pod.

```bash
sudo mv /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/kube-apiserver.yaml
sleep 20
kubectl get nodes
kubectl get pods -n kube-system | grep kube-apiserver
sudo mv /tmp/kube-apiserver.yaml /etc/kubernetes/manifests/kube-apiserver.yaml
sleep 40
```

Verify.

```bash
kubectl get nodes
kubectl get pods -n kube-system | grep kube-apiserver
```

---

## 7. Renew All kubeadm Certificates

Run on `control-plane`.

```bash
sudo kubeadm certs renew all
```

Check certificates.

```bash
sudo kubeadm certs check-expiration 
```

---

## 8. Copy New Admin Kubeconfig

Run on `control-plane`.

```bash
mkdir -p $HOME/.kube
sudo cp /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

Verify.

```bash
kubectl get nodes
```

---

## 9. Restart All Control Plane Static Pods

Run on `control-plane`.

```bash
sudo mkdir -p /tmp/k8s-manifests

sudo mv /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/k8s-manifests/
sudo mv /etc/kubernetes/manifests/kube-controller-manager.yaml /tmp/k8s-manifests/
sudo mv /etc/kubernetes/manifests/kube-scheduler.yaml /tmp/k8s-manifests/
sudo mv /etc/kubernetes/manifests/etcd.yaml /tmp/k8s-manifests/

sleep 30

sudo mv /tmp/k8s-manifests/*.yaml /etc/kubernetes/manifests/

sleep 60
```

Verify.

```bash
kubectl get nodes -o wide
kubectl get pods -n kube-system
kubectl get --raw='/readyz?verbose'
```
