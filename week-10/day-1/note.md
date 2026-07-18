# Helm Lab - Video 2 Notes

## Go to Helm Chart

```bash
cd nginx
```

---

## Check Existing Release

```bash
helm list -n helm-labs
```

---

## Check Release Status

```bash
helm status demo -n helm-labs
```

---

## View Release History

```bash
helm history demo -n helm-labs
```

---

## Edit Chart Version

```bash
vim Chart.yaml
```

Update:

```yaml
version: 0.2.0
appVersion: "1.29"
```

---

## Change Image Tag

```bash
vim values.yaml
```

Update:

```yaml
image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: "alpine"
```

---

## Verify Template

```bash
helm lint .
```

---

## Render Templates

```bash
helm template demo .
```

---

## Upgrade Release

```bash
helm upgrade demo . \
  -n helm-labs
```

---

## Verify Upgrade

```bash
kubectl get pods -n helm-labs
```

```bash
kubectl describe pod <pod-name> -n helm-labs
```

```bash
kubectl get deployment -n helm-labs
```

```bash
helm status demo -n helm-labs
```

---

## View Release History

```bash
helm history demo -n helm-labs
```

Expected:

```text
REVISION    STATUS
1           superseded
2           deployed
```

---

## Rollback to Revision 1

```bash
helm rollback demo 1 \
  -n helm-labs
```

---

## Verify Rollback

```bash
helm history demo -n helm-labs
```

Expected:

```text
REVISION
1
2
3
```

Revision 3 is the rollback release.

---

## Check Current Release

```bash
helm status demo -n helm-labs
```

---

## Verify Image

```bash
kubectl describe deployment nginx -n helm-labs
```

or

```bash
kubectl get deployment nginx \
  -n helm-labs \
  -o jsonpath='{.spec.template.spec.containers[0].image}'
```

Expected:

```text
nginx:1.29
```

---

# Package Helm Chart

## Create Packages Directory

```bash
mkdir -p packages
```

---

## Package Chart

```bash
helm package . \
  -d packages
```

---

## Verify Package

```bash
tree packages
```

Expected:

```text
packages/
└── nginx-0.2.0.tgz
```

---

# Login to GitHub Container Registry

## Export GitHub Username

```bash
export GITHUB_USERNAME=<your-github-username>
```

---

## Export GitHub Token

```bash
export CR_PAT=<your-github-token>
```

---

## Login

```bash
echo $CR_PAT | helm registry login ghcr.io \
  -u $GITHUB_USERNAME \
  --password-stdin
```

Expected:

```text
Login succeeded
```

---

# Push Chart to OCI Registry

```bash
helm push \
packages/nginx-0.2.0.tgz \
oci://ghcr.io/$GITHUB_USERNAME/helm-charts
```

Expected:

```text
Pushed
```

---

# Verify Repository

Open:

```
https://github.com/<your-github-username>?tab=packages
```

---

# Pull Chart

```bash
helm pull \
oci://ghcr.io/$GITHUB_USERNAME/helm-charts/nginx \
--version 0.2.0
```

---

## Verify

```bash
ls
```

Expected:

```text
nginx-0.2.0.tgz
```

---

## Extract Chart

```bash
tar -xzf nginx-0.2.0.tgz
```

---

## Verify

```bash
tree nginx
```

---

# Install from OCI Registry

```bash
helm install github-demo \
oci://ghcr.io/$GITHUB_USERNAME/helm-charts/nginx \
--version 0.2.0 \
-n helm-labs
```

---

## Verify

```bash
helm list -n helm-labs
```

```bash
kubectl get pods -n helm-labs
```

---

# Uninstall Release

```bash
helm uninstall github-demo \
-n helm-labs
```

---

## Verify

```bash
helm list -n helm-labs
```

---

# Logout Registry

```bash
helm registry logout ghcr.io
```

---

# Cleanup

```bash
helm uninstall demo -n helm-labs
```

```bash
kubectl get all -n helm-labs
```