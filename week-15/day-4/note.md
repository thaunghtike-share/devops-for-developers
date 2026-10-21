# Argo CD Image Updater — EKS and ECR Lab

## 0. Environment

> **Student note:** Replace every occurrence of `172083944066` with your own 12-digit AWS account ID.

```bash
export EKS_CLUSTER_NAME="my-eks"
export AWS_REGION="us-east-1"
# Replace this with your own AWS account ID.
export AWS_ACCOUNT_ID="172083944066"
```

## 1. Install Argo CD Image Updater

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj-labs/argocd-image-updater/stable/config/install.yaml
```

## 2. Get EKS OIDC Issuer

```bash
export OIDC_ISSUER=$(aws eks describe-cluster \
  --name "$EKS_CLUSTER_NAME" \
  --region "$AWS_REGION" \
  --query 'cluster.identity.oidc.issuer' \
  --output text)

export OIDC_PROVIDER="${OIDC_ISSUER#https://}"
echo "$OIDC_ISSUER"
```

## 3. Associate IAM OIDC Provider

```bash
eksctl utils associate-iam-oidc-provider \
  --cluster "$EKS_CLUSTER_NAME" \
  --region "$AWS_REGION" \
  --approve
```

## 4. Create IAM Policy — All ECR Repositories

**`ecr-policy.json`**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ecr:*",
      "Resource": "*"
    }
  ]
}
```

```bash
aws iam create-policy \
  --policy-name ArgoCDImageUpdaterECRReadPolicy \
  --policy-document file://ecr-policy.json
```

## 5. Create IAM Role and Attach Policy

**`trust-policy.json`**

```bash
cat > trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::${AWS_ACCOUNT_ID}:oidc-provider/${OIDC_PROVIDER}"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "${OIDC_PROVIDER}:aud": "sts.amazonaws.com",
          "${OIDC_PROVIDER}:sub": "system:serviceaccount:argocd:argocd-image-updater-controller"
        }
      }
    }
  ]
}
EOF
```

```bash
aws iam create-role \
  --role-name ArgoCDImageUpdaterECRRole \
  --assume-role-policy-document file://trust-policy.json

# Replace 172083944066 with your own AWS account ID.
aws iam attach-role-policy \
  --role-name ArgoCDImageUpdaterECRRole \
  --policy-arn arn:aws:iam::172083944066:policy/ArgoCDImageUpdaterECRReadPolicy
```

## 6. Configure IRSA

```bash
# Replace 172083944066 with your own AWS account ID.
kubectl annotate serviceaccount argocd-image-updater-controller \
  -n argocd \
  eks.amazonaws.com/role-arn=arn:aws:iam::172083944066:role/ArgoCDImageUpdaterECRRole \
  --overwrite

kubectl rollout restart deployment argocd-image-updater-controller -n argocd
```

## 7. Create ECR Login Script

**`ecr-login.sh`**

```bash
cat > ecr-login.sh <<'EOF'
#!/bin/sh
set -eu

export HOME=/tmp
export AWS_CONFIG_FILE=/tmp/aws-config
export AWS_SHARED_CREDENTIALS_FILE=/tmp/aws-credentials

TOKEN=$(aws ecr get-login-password --region us-east-1)

printf 'AWS:%s\n' "$TOKEN"
EOF
```

## 8. Create ECR Authentication ConfigMap

```bash
kubectl create configmap argocd-image-updater-ecr-auth \
  -n argocd \
  --from-file=ecr-login.sh \
  --dry-run=client -o yaml | kubectl apply -f -
```

## 9. Configure ECR Registry

```bash
# Uses AWS_ACCOUNT_ID from Section 0. Students only need to change it there.
kubectl create configmap argocd-image-updater-config \
  -n argocd \
  --from-literal=registries.conf="registries:
  - name: ecr-us-east-1
    api_url: https://${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com
    prefix: ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com
    credentials: ext:/app/auth/ecr-login.sh
    credsexpire: 11h" \
  --dry-run=client -o yaml | kubectl apply -f -
```

## 10. Mount ECR Login Script

```bash
kubectl patch deployment argocd-image-updater-controller \
  -n argocd \
  --type=strategic \
  -p='{"spec":{"template":{"spec":{"volumes":[{"name":"ecr-auth","configMap":{"name":"argocd-image-updater-ecr-auth","defaultMode":493}}],"containers":[{"name":"argocd-image-updater-controller","volumeMounts":[{"name":"ecr-auth","mountPath":"/app/auth","readOnly":true}]}]}}}}'

kubectl rollout restart deployment argocd-image-updater-controller -n argocd
```

## 11. Reuse Existing Argo CD Git Credentials

Repository: `git@github.com:thaunghtike-share/gitops-lab.git`

Branch: `main`

GitHub: **Repository → Settings → Deploy keys → Allow write access**

## 12. Create DEV ImageUpdater Resource

**`gitops-demo-app-dev.yaml`**

```yaml
apiVersion: argocd-image-updater.argoproj.io/v1alpha1
kind: ImageUpdater
metadata:
  name: gitops-demo-app-dev
  namespace: argocd
spec:
  applicationRefs:
    - namePattern: gitops-demo-app-dev
      images:
        - alias: app
          # Replace the account ID and ECR repository name with your own values.
          imageName: 172083944066.dkr.ecr.us-east-1.amazonaws.com/gitops-demo-app:dev-0e16dba
          commonUpdateSettings:
            updateStrategy: newest-build
            allowTags: "regexp:^dev-.*$"
          manifestTargets:
            helm:
              name: image.repository
              tag: image.tag
      writeBackConfig:
        method: git
        gitConfig:
          branch: main
          writeBackTarget: "helmvalues:./values-dev.yaml"
```

```bash
kubectl apply -f gitops-demo-app-dev.yaml
```

## 13. Git Write-back Flow

```text
AWS ECR (gitops-demo-app:dev-*)
    ↓
Argo CD Image Updater
    ↓
GitOps Repository (main)
    ↓
helm-charts/gitops-demo-app/values-dev.yaml
    ↓
Argo CD — gitops-demo-app-dev
```
