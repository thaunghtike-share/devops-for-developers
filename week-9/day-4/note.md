# Helm Lab - Video 1 Notes

## Create Namespace

```bash
kubectl create namespace helm-labs
```

---

## Check Helm Version

```bash
helm version
```

---

## Create a New Helm Chart

```bash
helm create nginx
```

---

## Go to Chart Directory

```bash
cd nginx
```

---

## View Helm Chart Structure

```bash
tree
```

---

## Remove Unused Templates

```bash
rm -rf templates/hpa.yaml \
       templates/ingress.yaml \
       templates/serviceaccount.yaml \
       templates/tests
```

(Optional)

```bash
rm -f templates/NOTES.txt
```

> Do **NOT** delete `_helpers.tpl`.

---

## Edit values.yaml

```bash
vim values.yaml
```

Update:

```yaml
fullnameOverride: nginx

replicaCount: 1

image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: latest
```

---

## Edit Deployment Template

```bash
vim templates/deployment.yaml
```

- Remove unused configurations
  - Liveness Probe
  - Readiness Probe
  - Resources
  - Volume Mounts
  - Volumes
  - Node Selector
  - Affinity
  - Tolerations
  - Image Pull Secrets
  - Service Account

---

## Edit Service Template

```bash
vim templates/service.yaml
```

(Keep default ClusterIP service)

---

## View Helper Template

```bash
vim templates/_helpers.tpl
```

---

## Lint Helm Chart

```bash
helm lint .
```

---

## Render Kubernetes YAML

```bash
helm template .
```

Render with Release Name:

```bash
helm template demo .
```

---

## Install Helm Chart

```bash
helm install demo . -n helm-labs
```

---

## Check Helm Releases

```bash
helm list -n helm-labs
```

---

## Verify Kubernetes Resources

```bash
kubectl get all -n helm-labs
```

---

## Check Pods

```bash
kubectl get pods -n helm-labs
```