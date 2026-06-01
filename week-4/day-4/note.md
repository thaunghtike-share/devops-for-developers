# learn-ecs-backend

# AWS GitHub Actions OIDC Setup For ECR

# Step 1 - Set Environment Variables

```bash
export AWS_REGION="ap-southeast-1"
export GITHUB_USER="thaunghtike-share" 
export ROLE_NAME="github-actions-ecs-role"

export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
```

# Step 2 - Create GitHub OIDC Provider

```bash
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
```
---

# Step 3 - Create Trust Policy

```bash
cat > trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::$AWS_ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": [
          "repo:${GITHUB_USER}/learn-ecs-backend:*", 
          "repo:${GITHUB_USER}/learn-ecs-frontend:*"
         ] 
        }
      }
    }
  ]
}
EOF
```

---

# Step 4 - Verify Trust Policy

```bash
cat trust-policy.json
```

---

# Step 5 - Create IAM Role

```bash
aws iam create-role \
  --role-name $ROLE_NAME \
  --assume-role-policy-document file://trust-policy.json
```

---

# Step 6 - Attach ECR + ECS Permission

```bash
aws iam attach-role-policy \
  --role-name $ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser

aws iam attach-role-policy \
  --role-name $ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/AmazonECS_FullAccess
```

## Step 6.1 - Add IAM PassRole Permission For ECS

```bash
cat > ecs-passrole-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "*"
    }
  ]
}
EOF
```

Attach inline policy:

```bash
aws iam put-role-policy \
  --role-name $ROLE_NAME \
  --policy-name AllowPassRoleForECS \
  --policy-document file://ecs-passrole-policy.json
```

---

# Step 7 - Verify IAM Role

```bash
aws iam get-role \
  --role-name $ROLE_NAME
```


Backend API for ECS three-tier demo.

## Local Test

.env 

```text
APP_NAME=learn-ecs-backend

BACKEND_PORT=8000
FLASK_ENV=production

POSTGRES_DB=learn_devops
POSTGRES_USER=learn_user
POSTGRES_PASSWORD=learn_password
DB_HOST=learn-ecs-db
DB_PORT=5432
```

```bash
docker compose up --build
```

Backend URL:

```text
http://localhost:8000
```

Health check:

```bash
curl http://localhost:8000/api/health
```

## Backend API

```text
GET    /api/health
GET    /api/stats
GET    /api/users
POST   /api/register
DELETE /api/users/:id
```

## ECS Task Definition

Task definition family:

```text
learn-ecs-backend
```

Container name:

```text
learn-ecs-backend
```

Container port:

```text
8000
```

## ECS Environment Variables

```text
FLASK_ENV=production
DB_HOST=learn-ecs-db
DB_PORT=5432
POSTGRES_DB=learn_devops
POSTGRES_USER=learn_user
POSTGRES_PASSWORD=learn_password
```

If you use Cloud Map namespace like `ecs.local`, use:

```text
DB_HOST=learn-ecs-db.ecs.local
```

## Security Group

Backend inbound:

```text
Port 8000
Source = frontend security group or internal ALB security group
```

Backend outbound:

```text
Allow 5432 to db security group
```

