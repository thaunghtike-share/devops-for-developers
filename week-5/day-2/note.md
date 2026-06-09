# Check MicroK8s Cluster Status
microk8s status

# View Cluster Nodes
microk8s kubectl get nodes

# View All System Pods
microk8s kubectl get pods -A

# View All Services
microk8s kubectl get svc -A

# Enable Common Addons
microk8s enable dns storage

# Verify Addons Pods
microk8s kubectl get pods -A

# Create Pod Imperatively
microk8s kubectl run nginx --image=nginx

# Check Pod Status
microk8s kubectl get pods

# Get Detailed Pod Information
microk8s kubectl describe pod nginx

microk8s kubectl logs -f nginx

# Check Containerd Status
microk8s kubectl get node microk8s -o jsonpath='{.status.nodeInfo.containerRuntimeVersion}'; echo 

sudo systemctl status snap.microk8s.daemon-containerd

microk8s ctr containers list

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-yaml
spec:
  containers:
    - name: nginx
      image: nginx
      ports:
        - containerPort: 80
```        

# Create Pod Declaratively
microk8s kubectl create -f pod.yaml

# Verify Created Pods
microk8s kubectl get pods

# Delete Imperative Pod
microk8s kubectl delete pod nginx

# Delete Declarative Pod
microk8s kubectl delete -f pod.yaml

# Verify Cleanup
microk8s kubectl get pods