# LoadBalancer Service Demo (Imperative)

## Create Deployment

```bash
kubectl create deployment nginx \
  --image=nginx:1.29 \
  --replicas=3
```

---

## Expose Deployment as LoadBalancer

```bash
kubectl expose deployment nginx \
  --type=LoadBalancer \
  --port=80 \
  --target-port=80 \
  --name=nginx-lb
```

---

## Verify Pods

```bash
kubectl get pods
```

---

## Verify Service

```bash
kubectl get svc
```

Initially, the external endpoint may still be provisioning.

```text
NAME       TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)
nginx-lb   LoadBalancer   10.100.20.15    <pending>     80:xxxxx/TCP
```

Wait for a minute and check again.

```bash
kubectl get svc
```

On EKS, you'll typically see an AWS ELB DNS name.

```text
NAME       TYPE           CLUSTER-IP      EXTERNAL-IP
nginx-lb   LoadBalancer   10.100.20.15    a1b2c3d4e5f6.us-east-1.elb.amazonaws.com
```

On AKS, you'll typically see a Public IP address instead.

---

## Test from Browser

Open the external endpoint in your browser.

```text
http://<external-endpoint>
```

Or test with curl.

```bash
curl http://<external-endpoint>
```

You should see the default **NGINX Welcome Page**.