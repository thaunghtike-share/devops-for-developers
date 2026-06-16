# Kubeadm Kubernetes Cluster Lab

## 1. Lab Network

```text
vagrant version
VBoxManage --version

Control Plane IP: 172.20.20.10
Worker IP:        172.20.20.11
Pod CIDR:         192.168.0.0/16
```

---

## 2. Create Workspace

```bash
mkdir kubeadm-lab
cd kubeadm-lab
vim Vagrantfile
```

---

## 3. Vagrantfile

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"

  config.vm.define "control-plane" do |node|
    node.vm.hostname = "control-plane"
    node.vm.network "private_network", ip: "172.20.20.10"

    node.vm.provider "virtualbox" do |vb|
      vb.name = "kube-control-plane"
      vb.memory = 4096
      vb.cpus = 2
    end
  end

  config.vm.define "worker" do |node|
    node.vm.hostname = "worker"
    node.vm.network "private_network", ip: "172.20.20.11"

    node.vm.provider "virtualbox" do |vb|
      vb.name = "kube-worker"
      vb.memory = 2048
      vb.cpus = 2
    end
  end
end
```

---

## 4. Start VMs

```bash
vagrant up
vagrant status
```

---

## 5. SSH into Nodes

### Control Plane

```bash
vagrant ssh control-plane
```

### Worker

Open another terminal.

```bash
vagrant ssh worker
```

---

# Run on BOTH Nodes

Run all commands in this section on both `control-plane` and `worker`.

---

## 6. Set Hostname Check

```bash
hostname
ip a
```

---

## 7. Disable Swap

```bash
sudo swapoff -a
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
```

Verify:

```bash
free -h
```

---

## 8. Load Kernel Modules

```bash
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter
```

Verify:

```bash
lsmod | grep overlay
lsmod | grep br_netfilter
```

---

## 9. Configure sysctl

```bash
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

sudo sysctl --system
```

Verify:

```bash
sysctl net.ipv4.ip_forward
sysctl net.bridge.bridge-nf-call-iptables
```

---

## 10. Install Containerd

```bash
sudo apt-get update
sudo apt-get install -y containerd

sudo mkdir -p /etc/containerd

containerd config default | sudo tee /etc/containerd/config.toml > /dev/null

sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml

sudo systemctl restart containerd
sudo systemctl enable containerd
sudo systemctl status containerd --no-pager
```

---

## 11. Install kubeadm, kubelet, kubectl

```bash
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gpg

sudo mkdir -p -m 755 /etc/apt/keyrings

curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.36/deb/Release.key \
| sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.36/deb/ /' \
| sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update

sudo apt-get install -y kubelet kubeadm kubectl

sudo apt-mark hold kubelet kubeadm kubectl

sudo systemctl enable kubelet
```

Verify:

```bash
kubeadm version
kubelet --version
kubectl version --client
```

---

# Run on CONTROL PLANE Only

---

## 12. Initialize Kubernetes Cluster

```bash
sudo kubeadm init \
  --apiserver-advertise-address=172.20.20.10 \
  --pod-network-cidr=192.168.0.0/16
```

---

## 13. Configure kubectl

```bash
mkdir -p $HOME/.kube

sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config

sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

Verify:

```bash
kubectl get nodes
kubectl get pods -A
```

At this stage, the control plane may show `NotReady` because CNI is not installed yet.

---

## 14. Get Worker Join Command

```bash
kubeadm token create --print-join-command
```

Copy the output.

Example:

```bash
sudo kubeadm join 172.20.20.10:6443 --token xxxxxx.xxxxxxxxxxxxxxxx \
  --discovery-token-ca-cert-hash sha256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 15. Install Calico CNI

```bash
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.30.2/manifests/calico.yaml
```

Check pods:

```bash
watch kubectl get pods -n kube-system
kubectl get nodes
```

Wait until the control plane becomes Ready:

```bash
watch kubectl get nodes
```

Press `CTRL + C` to exit watch.

---

## 16. Join Worker Node

Paste the join command from the control plane.

```bash
sudo kubeadm join 172.20.20.10:6443 --token xxxxxx.xxxxxxxxxxxxxxxx \
  --discovery-token-ca-cert-hash sha256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

# Back to CONTROL PLANE

---

## 17. Verify Cluster Nodes

```bash
kubectl get nodes
kubectl get pods -n kube-system

sudo systemctl status kubelet
sudo systemctl status containerd
ls /etc/kubernetes/manifests
sudo ctr -n k8s.io containers ls | grep -E "kube|etcd"
```

Expected:

```text
control-plane   Ready
worker          Ready
```

---

## 18. Useful Worker Commands

Run on worker:

```bash
sudo systemctl status kubelet --no-pager
sudo systemctl status containerd --no-pager
sudo ctr -n k8s.io containers ls | grep -E "kube|calico"
```

---

## 19. Destroy Vagrant VMs

Run from Mac inside `kubeadm-lab` directory:

```bash
vagrant halt
vagrant destroy -f
```

---

## 20. Common Troubleshooting

### Check VM status

```bash
vagrant status
```
