# AWS GitHub Actions OIDC Setup For ECR

This setup allows GitHub Actions to securely push Docker images to AWS ECR using OIDC.

Instead of storing long-term AWS Access Keys inside GitHub Secrets, GitHub Actions will request temporary AWS credentials and assume an IAM Role.

---

# Step 1 - Set Environment Variables

```bash
export AWS_REGION="ap-southeast-1"
export GITHUB_USER="thaunghtike-share" ## Replace Your GitHub Username or Org Name
export GITHUB_REPO="aws-ecr-github-actions-oidc"
export ROLE_NAME="github-actions-ecr-role"

export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
```

## Description

This step defines reusable environment variables.

- AWS_REGION → AWS region
- GITHUB_USER → GitHub username
- GITHUB_REPO → GitHub repository name
- ROLE_NAME → IAM Role name
- AWS_ACCOUNT_ID → Automatically gets current AWS Account ID

---

# Step 2 - Create GitHub OIDC Provider

```bash
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
```

## Description

This step creates the GitHub OIDC Provider inside AWS IAM.

GitHub Actions uses OIDC tokens to authenticate with AWS.

AWS must trust GitHub Actions before GitHub can assume AWS IAM Roles.

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
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
          "token.actions.githubusercontent.com:sub": "repo:${GITHUB_USER}/${GITHUB_REPO}:ref:refs/heads/main"
        }
      }
    }
  ]
}
EOF
```

## Description

This step creates the IAM Trust Policy.

The Trust Policy defines which GitHub repository is allowed to assume the AWS IAM Role.

If the repository name, branch name, or ref value is incorrect, GitHub Actions will fail with:

```text
Not authorized to perform sts:AssumeRoleWithWebIdentity
```

---

# Step 4 - Verify Trust Policy

```bash
cat trust-policy.json
```

## Description

Always verify generated JSON files before applying them.

This helps detect:
- Typo mistakes
- Wrong repository names
- Wrong branch names
- Missing ref values

---

# Step 5 - Create IAM Role

```bash
aws iam create-role \
  --role-name $ROLE_NAME \
  --assume-role-policy-document file://trust-policy.json
```

## Description

This step creates the AWS IAM Role used by GitHub Actions.

GitHub Actions will assume this role using OIDC.

---

# Step 6 - Attach ECR Permission

```bash
aws iam attach-role-policy \
  --role-name $ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser
```

## Description

This step gives the IAM Role permission to manage AWS ECR repositories.

The role can:
- Push Docker images
- Pull Docker images
- Create repositories
- Manage ECR resources

---

# Step 7 - Verify IAM Role

```bash
aws iam get-role \
  --role-name github-actions-ecr-role
```

## Description

This step verifies the IAM Role configuration.

Check:
- Trust Policy
- Role ARN
- OIDC Provider
- Attached policies

---

# Important Notes

## Local Docker Login

When using ECR locally, Docker does not understand AWS IAM directly.

So AWS CLI generates a temporary Docker login token.

Example flow:

```text
AWS Credential
    ↓
aws ecr get-login-password
    ↓
temporary ECR token
    ↓
docker login
    ↓
Docker can push/pull ECR
```

---

## Why CI/CD Does Not Need Manual Login Command

Inside GitHub Actions:

```yaml
uses: aws-actions/amazon-ecr-login@v2
```

This action automatically runs:

```text
aws ecr get-login-password | docker login
```

internally.

So the login process still exists, but GitHub Actions handles it automatically.

---

# Access Key Method vs OIDC Method

## Access Key Method

Pros:
- Easier for beginners
- Simple setup

Cons:
- Stores long-term secrets
- Higher security risk
- Secrets may leak

---

## OIDC Method

Pros:
- No long-term AWS secrets
- Uses temporary credentials
- More secure
- Recommended for production

Cons:
- Slightly more complex setup

---

# Final Notes

Modern CI/CD pipelines increasingly use OIDC because it removes the need for long-term cloud credentials.

GitHub Actions + AWS OIDC is considered a production-grade secure authentication method for AWS deployments.
