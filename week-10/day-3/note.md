# Configure AWS CLI

aws configure

AWS Access Key ID [None]: <YOUR_ACCESS_KEY>
AWS Secret Access Key [None]: <YOUR_SECRET_KEY>
Default region name [None]: ap-southeast-1
Default output format [None]: json

# Update kubeconfig for EKS Cluster

aws eks update-kubeconfig \
  --region ap-southeast-1 \
  --name my-eks-cluster

# Verify Current Context

kubectl config current-context

# View Worker Nodes

kubectl get nodes

# View System Pods

kubectl get pods -n kube-system

# View kubeconfig (Optional)

kubectl config view