# Kustomize Generators Lab — Video 3

Continue from the previous Base / Overlay + Patch lessons. Only **dev** and **production** are included.

## What was added

- `configMapGenerator` with demo `APP_ENV` and `LOG_LEVEL` variables in each overlay
- `secretGenerator` with **fake, disposable credentials** in each overlay
- `patch-env.yaml` to connect the generated ConfigMap and Secret to the existing Nginx Deployment via `envFrom`
- Previous resource patch, replica count, image tag, and namespace configurations are preserved

**Important:** The Nginx image doesn't use these variables; this lab shows Kubernetes injection and Kustomize reference updates. These Secret values are deliberately fake. Real secrets must not be committed to Git as plain text. Kubernetes Secrets are base64-encoded, not inherently encrypted by that encoding.

## Generate and inspect manifests

From `kustomize-generators-lab/`:

```bash
kubectl kustomize overlays/dev
kubectl kustomize overlays/production
```

Notice generated `app-config-<hash>` and `app-secret-<hash>` names, and the updated references in the Deployment's `envFrom`.

## Deploy

```bash
kubectl create namespace dev --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace production --dry-run=client -o yaml | kubectl apply -f -

kubectl apply -k overlays/dev
kubectl apply -k overlays/production

kubectl rollout status deployment/kustomize-demo-app -n dev
kubectl rollout status deployment/kustomize-demo-app -n production
```

## Verify the generated resources

```bash
kubectl get configmap,secret -n dev
kubectl get configmap,secret -n production
kubectl get deployments -n dev
kubectl get deployments -n production

# Confirm variables exist inside the container (avoid printing actual secrets in real environments)
kubectl exec -n dev deployment/kustomize-demo-app -- printenv APP_ENV
kubectl exec -n dev deployment/kustomize-demo-app -- printenv LOG_LEVEL
kubectl exec -n production deployment/kustomize-demo-app -- printenv APP_ENV
kubectl exec -n production deployment/kustomize-demo-app -- printenv LOG_LEVEL
```

## Hash / rollout demo

Change `LOG_LEVEL` in `overlays/dev/kustomization.yaml` from `debug` to `info`, then run `kubectl kustomize overlays/dev` again. The generated ConfigMap name and its Deployment reference should change. `kubectl apply -k overlays/dev` updates the Deployment's pod template and starts a rolling update. Restore it to `debug` afterward if desired.

**Notes:** Kustomize automatically updates supported ConfigMap/Secret reference fields such as `envFrom[].configMapRef.name` / `envFrom[].secretRef.name` in generated manifests. The overlay `namespace:` sets resource namespaces but does not create Namespace objects. Repeated configuration edits may leave older generated ConfigMaps/Secrets until cleaned up.
