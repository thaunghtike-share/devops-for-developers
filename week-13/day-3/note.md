## Update Argocd Server
kubectl patch svc argocd-server -n argocd \
  -p '{"spec":{"type":"LoadBalancer"}}'

## List Secrets
kubectl get secrets -n argocd

## Get Password
kubectl get secrets argocd-initial-admin-secret -n argocd -o yaml

## Decode Password

echo "" | base64 -d; echo