# AWS Load Balancer Controller - Lab 1

# Environment

| Item | Value |
|------|-------|
| AWS Region | ap-southeast-1 |
| Cluster Name | my-eks-cluster |
| Kubernetes Version | 1.36 |
| Availability Zones | ap-southeast-1a, ap-southeast-1b |
| VPC CIDR | 10.0.0.0/16 |

---

# VPC Design

```text
                                   Internet
                                       │
                                       │
                              Internet Gateway
                                       │
     ┌────────────────────────────────────────────────────────┐
     │                 Custom VPC (10.0.0.0/16)               │
     │                                                        │
     │   Public Subnet A             Public Subnet B          │
     │   10.0.1.0/24                 10.0.2.0/24              │
     │          │                           │                 │
     │          └──────────────┬────────────┘                 │
     │                         │                              │
     │                  Internet-facing ALB                   │
     │                         │                              │
     │                    NAT Gateway                         │
     │                         │                              │
     │   Private Subnet A            Private Subnet B         │
     │   10.0.11.0/24                10.0.12.0/24             │
     │          │                           │                 │
     │     Worker Node                Worker Node             │
     │                                                        │
     │          Amazon EKS Control Plane (Managed)            │
     └────────────────────────────────────────────────────────┘
```

---

# Network Design

| Resource | CIDR | AZ | Purpose |
|----------|------|----|----------|
| VPC | 10.0.0.0/16 | - | Entire EKS Network |
| Public Subnet A | 10.0.1.0/24 | ap-southeast-1a | Internet-facing ALB |
| Public Subnet B | 10.0.2.0/24 | ap-southeast-1b | Internet-facing ALB |
| Private Subnet A | 10.0.11.0/24 | ap-southeast-1a | Worker Nodes |
| Private Subnet B | 10.0.12.0/24 | ap-southeast-1b | Worker Nodes |

---

# Architecture

```text
                    Internet
                        │
                        ▼
               Internet Gateway
                        │
                        ▼
          Internet-facing Application
               Load Balancer (ALB)
                        │
                        ▼
        AWS Load Balancer Controller
                        │
                        ▼
              Amazon EKS Cluster
                        │
        ┌───────────────┴───────────────┐
        │                               │
   Worker Node                     Worker Node
 Private Subnet A               Private Subnet B
```

---

# Verify AWS CLI

```bash
aws --version
kubectl version --client
eksctl version
helm version
```

---

# Update kubeconfig

```bash
aws eks update-kubeconfig \
  --name my-eks-cluster \
  --region ap-southeast-1
```

---

# Verify Cluster

```bash
kubectl get nodes
```

# Associate IAM OIDC Provider

```bash
eksctl utils associate-iam-oidc-provider \
  --cluster my-eks-cluster \
  --region ap-southeast-1 \
  --approve
```

---

# Verify OIDC Provider

```bash
aws eks describe-cluster \
  --name my-eks-cluster \
  --region ap-southeast-1 \
  --query "cluster.identity.oidc.issuer" \
  --output text
```

---

# Download IAM Policy

```bash
curl -Lo iam_policy.json \
https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.14.1/docs/install/iam_policy.json
```

---

# Create IAM Policy

```bash
aws iam create-policy \
  --policy-name AWSLoadBalancerControllerIAMPolicy \
  --policy-document file://iam_policy.json
```

---

# Get AWS Account ID

```bash
ACCOUNT_ID=$(aws sts get-caller-identity \
  --query Account \
  --output text)
```

---

# Create IAM Service Account

```bash
eksctl create iamserviceaccount \
  --cluster my-eks-cluster \
  --region ap-southeast-1 \
  --namespace kube-system \
  --name aws-load-balancer-controller \
  --attach-policy-arn arn:aws:iam::$ACCOUNT_ID:policy/AWSLoadBalancerControllerIAMPolicy \
  --override-existing-serviceaccounts \
  --approve
```

---

# Verify Service Account

```bash
kubectl get sa -n kube-system
```

---

# Add Helm Repository

```bash
helm repo add eks https://aws.github.io/eks-charts
```

```bash
helm repo update
```

---

# Install AWS Load Balancer Controller

# Get VPC ID

```bash
VPC_ID=$(aws eks describe-cluster \
  --name my-eks-cluster \
  --region ap-southeast-1 \
  --query "cluster.resourcesVpcConfig.vpcId" \
  --output text)

echo $VPC_ID
```

```bash
helm install aws-load-balancer-controller \
eks/aws-load-balancer-controller \
-n kube-system \
--set clusterName=my-eks-cluster \
--set serviceAccount.create=false \
--set serviceAccount.name=aws-load-balancer-controller \
--set region=ap-southeast-1 \
--set vpcId=$VPC_ID \
--version 1.14.0
```

---

# Verify Helm Release

```bash
helm list -n kube-system
```

---

# Verify Deployment

```bash
kubectl get deployment \
-n kube-system
```