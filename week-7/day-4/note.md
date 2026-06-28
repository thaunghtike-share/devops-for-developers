````markdown
# Kubernetes ConfigMap Lab

## 🎯 Lab Objectives

In this lab, you will learn:

- Create ConfigMap (Imperative)
- Create ConfigMap (Declarative)
- Use ConfigMap as Environment Variables
- Use ConfigMap using envFrom
- Mount an Nginx Configuration File using subPath
- Update ConfigMap
- Understand ConfigMap refresh behavior
- Cleanup

---

# 1. Create Namespace

```bash
kubectl create namespace configmap-lab
```

Verify

```bash
kubectl get ns
```

---

# 2. Create ConfigMap (Imperative)

```bash
kubectl create configmap app-config \
--from-literal=APP_NAME=myapp \
--from-literal=APP_ENV=dev \
--from-literal=APP_PORT=3000 \
-n configmap-lab
```

Verify

```bash
kubectl get configmap -n configmap-lab
```

Describe

```bash
kubectl describe configmap app-config -n configmap-lab
```

View YAML

```bash
kubectl get configmap app-config -o yaml -n configmap-lab
```

---

# 3. Create ConfigMap (Declarative)

Create

```bash
vim backend-config.yaml
```

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: backend-config
  namespace: configmap-lab
data:
  APP_NAME: backend
  APP_ENV: development
  APP_PORT: "8080"
```

Apply

```bash
kubectl apply -f backend-config.yaml
```

Verify

```bash
kubectl get configmap -n configmap-lab
```

---

# 4. Use ConfigMap as Environment Variables

Create

```bash
vim pod-env.yaml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: env-demo
  namespace: configmap-lab
spec:
  containers:
    - name: app
      image: busybox
      command: ["sleep","3600"]
      env:
        - name: APP_NAME
          valueFrom:
            configMapKeyRef:
              name: backend-config
              key: APP_NAME

        - name: APP_ENV
          valueFrom:
            configMapKeyRef:
              name: backend-config
              key: APP_ENV
```

Apply

```bash
kubectl apply -f pod-env.yaml
```

Verify

```bash
kubectl exec -it env-demo -n configmap-lab -- /bin/sh
```

```bash
env
```

---

# 5. Use envFrom

Create

```bash
vim pod-envfrom.yaml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: envfrom-demo
  namespace: configmap-lab
spec:
  containers:
    - name: app
      image: busybox
      command: ["sleep","3600"]
      envFrom:
        - configMapRef:
            name: backend-config
```

Apply

```bash
kubectl apply -f pod-envfrom.yaml
```

Verify

```bash
kubectl exec -it envfrom-demo -n configmap-lab -- /bin/sh
```

```bash
env
```

Notice

All ConfigMap keys become environment variables.

---

# 6. Mount Nginx Configuration File using subPath

Create

```bash
vim nginx-config.yaml
```

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
  namespace: configmap-lab
data:
  nginx.conf: |
    worker_processes auto;

    events {
      worker_connections 1024;
    }

    http {
      server {
        listen 80;

        location / {
          return 200 "Hello ConfigMap\n";
        }
      }
    }
```

Apply

```bash
kubectl apply -f nginx-config.yaml
```

Create

```bash
vim nginx-pod.yaml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-demo
  namespace: configmap-lab
spec:
  containers:
    - name: nginx
      image: nginx:latest
      volumeMounts:
        - name: nginx-config
          mountPath: /etc/nginx/nginx.conf
          subPath: nginx.conf
  volumes:
    - name: nginx-config
      configMap:
        name: nginx-config
```

Apply

```bash
kubectl apply -f nginx-pod.yaml
```

Verify

```bash
kubectl exec -it nginx-demo -n configmap-lab -- /bin/bash

cat /etc/nginx/nginx.conf
```

---

# 7. Update ConfigMap

Update the ConfigMap YAML.

```bash
vim nginx-config.yaml
```

Change

```nginx
return 200 "Hello ConfigMap\n";
```

To

```nginx
return 200 "ConfigMap Updated\n";
```

Apply again

```bash
kubectl apply -f nginx-config.yaml
```

---

# 8. Verify Update Behavior

## subPath

```bash
kubectl exec -it nginx-demo -n configmap-lab -- /bin/bash
cat /etc/nginx/nginx.conf
```

Notice

The configuration file is **NOT** updated automatically because it is mounted using **subPath**.

Restart the Pod.

```bash
kubectl delete pod nginx-demo -n configmap-lab
kubectl apply -f nginx-pod.yaml
```

Verify again

```bash
kubectl exec -it nginx-demo -n configmap-lab -- /bin/bash
cat /etc/nginx/nginx.conf
```

Now the updated configuration appears.

---

# 9. Important Notes

| Usage | Auto Update |
|--------|-------------|
| env | ❌ No |
| envFrom | ❌ No |
| subPath | ❌ No |

---

# 10. Cleanup

```bash
kubectl delete namespace configmap-lab
```

---

# Summary

In this lab, you learned:

- Imperative ConfigMap
- Declarative ConfigMap
- Environment Variables
- envFrom
- Nginx Configuration File using subPath
- Updating ConfigMaps
- ConfigMap refresh behavior
- ConfigMap limitations
````
