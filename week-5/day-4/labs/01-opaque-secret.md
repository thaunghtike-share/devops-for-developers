# Lab 1 - Opaque Secret

## Create Namespace

```bash
kubectl create namespace secret-lab
```

---

## Imperative Method

```bash
kubectl create secret generic app-secret \
  --from-literal=DB_USER=admin \
  --from-literal=DB_PASSWORD=password123 \
  --from-literal=JWT_SECRET=my-secret \
  -n secret-lab
```

## Verify

```bash
kubectl get secret -n secret-lab

kubectl describe secret app-secret -n secret-lab

kubectl get secret app-secret -n secret-lab

kubectl get secret app-secret -o yaml -n secret-lab

echo "cGFzc3dvcmQxMjM=" | base64 
-d; echo

echo "bXktc2VjcmV0" | base64 -d; 
echo

kubectl get secret app-secret \
-o jsonpath="{.data.DB_PASSWORD}" \
-n secret-lab | base64 -d
```

---

## Declarative Method (stringData)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret-stringdata
  namespace: secret-lab
type: Opaque
stringData:
  DB_USER: admin
  DB_PASSWORD: password123
  JWT_SECRET: my-secret
```

```bash
vim secret-stringdata.yaml
kubectl apply -f secret-stringdata.yaml
```

## Verify

```bash
kubectl get secret -n secret-lab
kubectl get secret app-secret-stringdata -o yaml -n secret-lab
```

---

## Declarative Method (data)

### Encode Values

```bash
echo -n admin | base64

echo -n password123 | base64

echo -n my-secret | base64
```

### Secret YAML

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret-data
  namespace: secret-lab
type: Opaque
data:
  DB_USER: YWRtaW4=
  DB_PASSWORD: cGFzc3dvcmQxMjM=
  JWT_SECRET: bXktc2VjcmV0
```

```bash
kubectl apply -f secret-data.yaml
```

## Verify

```bash
echo -n "password123" | base64
echo -n "admin" | base64

kubectl get secret -n secret-lab

kubectl describe secret app-secret-data -n secret-lab

kubectl get secret app-secret-data \
-o yaml -n secret-lab

kubectl get secret app-secret-data \
-o jsonpath="{.data.DB_PASSWORD}" \
-n secret-lab | base64 -d
```