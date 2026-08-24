# Port Forward Lab

## Docker 
docker run -d --name nginx-app -p 8080:80 nginx

# Create Deployment with 2 replicas
kubectl create deployment whoami \
  --image=traefik/whoami \
  --replicas=2

# Check
kubectl get deployment
kubectl get pods -l app=whoami

# Create ClusterIP Service
kubectl expose deployment whoami \
  --name=whoami-service \
  --type=ClusterIP \
  --port=80 \
  --target-port=80

# Check Service
kubectl get svc whoami-service
kubectl get endpoints whoami-service

# -------------------------
# Pod Port Forward
# -------------------------

kubectl get pods -l app=whoami

kubectl port-forward pod/whoami-5cbdff98fc-lmxrz 8080:80

# Test from another terminal
curl http://localhost:8080


# -------------------------
# Service Port Forward
# -------------------------

kubectl port-forward service/whoami-service 8080:80

# Test from another terminal
curl http://localhost:8080

# Create NodePort Service
kubectl expose deployment whoami \
  --name=whoami-nodeport \
  --type=NodePort \
  --port=80 \
  --target-port=80


# -------------------------
# Cleanup
# -------------------------

kubectl delete service whoami-service
kubectl delete deployment whoami