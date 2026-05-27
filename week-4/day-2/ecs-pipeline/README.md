# CI/CD Workflows - Two Production Methods

This repo contains only 2 workflows:

1. `method-1-branch-and-manual.yml`
   - Dev: auto on push to `dev`
   - UAT: auto on push to `uat`
   - Prod: manual trigger using `workflow_dispatch`
   - Real step: Docker build and push to ECR
   - Dummy step: ECS or GitOps deploy

2. `method-2-release-tag.yml`
   - Prod: auto on release tag push like `v1.0.0`
   - Real step: Docker build and push to ECR
   - Dummy step: ECS or GitOps deploy

Required GitHub Secret:

```text
AWS_ACCOUNT_ID
```

AWS OIDC role name used in workflows:

```text
github-actions-ecr-role
```
