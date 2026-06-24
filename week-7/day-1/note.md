# Longhorn Dynamic Provisioning with PostgreSQL StatefulSet

# 1. Verify Cluster

```bash
kubectl get nodes -o wide
kubectl get storageclass
```

---

# 2. Install Required Packages on Every Node

Run on ALL nodes.

```bash
sudo apt update
sudo apt install -y open-iscsi nfs-common
sudo systemctl enable --now iscsid
```

Verify:

```bash
sudo systemctl status iscsid
```

---

# 3. Install Longhorn

```bash
kubectl apply -f https://raw.githubusercontent.com/longhorn/longhorn/v1.9.1/deploy/longhorn.yaml
```

Verify:

```bash
kubectl get pods -n longhorn-system
```

Wait until all pods are Running.

---

# 4. Verify StorageClass

```bash
kubectl get storageclass
```

Expected:

```text
NAME                 PROVISIONER
longhorn (default)   driver.longhorn.io
```

---

# 5. Create PostgreSQL StatefulSet

Create file:

```bash
vim postgres.yaml
```

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  replicas: 2
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:17
          ports:
            - name: postgres
              containerPort: 5432
          env:
            - name: POSTGRES_PASSWORD
              value: password123
            - name: PGDATA
              value: /var/lib/postgresql/data/pgdata
          volumeMounts:
            - name: postgres-data
              mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
    - metadata:
        name: postgres-data
      spec:
        accessModes:
          - ReadWriteOnce
        storageClassName: longhorn
        resources:
          requests:
            storage: 1Gi
```

Apply:

```bash
kubectl apply -f postgres.yaml
```

---

# 6. Verify StatefulSet

```bash
kubectl get sts
kubectl get pod -o wide
```

Expected:

```text
postgres-0
postgres-1
```

---

# 7. Verify Dynamic Provisioning

Check PVC:

```bash
kubectl get pvc
```

Expected:

```text
NAME                         STATUS
postgres-data-postgres-0     Bound
postgres-data-postgres-1     Bound
```

Check PV:

```bash
kubectl get pv
```

Expected:

```text
pvc-xxxxxxxx
pvc-yyyyyyyy
```

Notice that we never created any PV manually.

Longhorn automatically created them.

This is Dynamic Provisioning.

---

# 8. Verify Longhorn Volumes

Check Longhorn volumes:

```bash
kubectl get volumes.longhorn.io -n longhorn-system
```

You should see two volumes automatically created.

---

# 9. Access Longhorn UI

```bash
kubectl -n longhorn-system port-forward svc/longhorn-frontend 8081:80 --address 172.20.20.10```

Open Browser:

```text
http://172.20.20.10:8081
```

Navigate to:

```text
Volume
```

You should see:

```text
postgres-data-postgres-0
postgres-data-postgres-1
```

Longhorn created these volumes automatically.

---

# 10. Verify Which Node Hosts Each Pod

```bash
kubectl get pod -o wide
```

Example:

```text
NAME         NODE
postgres-0   worker1
postgres-1   worker2
```

---

# 11. Verify Data Location on Worker Nodes

SSH into worker node:

```bash
vagrant ssh worker1
```

Check Longhorn data:

```bash
sudo ls /var/lib/longhorn
```

Or:

```bash
sudo find /var/lib/longhorn -type d | head -20
```

You will see Longhorn volume data stored on the worker node disk.

Exit:

```bash
exit
```

Repeat for another worker node if required.

---

# 12. Create Sample Data

Connect to postgres-0:

```bash
kubectl exec -it postgres-0 -- psql -U admin -d appdb
```

Create table:

```sql
CREATE TABLE users(
  id SERIAL PRIMARY KEY,
  name VARCHAR(100)
);

INSERT INTO users(name)
VALUES ('thaung');
```

Verify:

```sql
SELECT * FROM users;
```

Exit:

```sql
\q
```

---

# 13. Check postgres-1

Connect:

```bash
kubectl exec -it postgres-1 -- psql -U admin -d appdb
```

Run:

```sql
SELECT * FROM users;
```

Expected:

```text
ERROR: relation "users" does not exist
```

Or no data exists.

---

# 14. Important Observation

Even though we have:

```text
postgres-0
postgres-1
```

Both pods have different PVCs.

```text
postgres-data-postgres-0
postgres-data-postgres-1
```

Both pods have different Longhorn volumes.

```text
Volume A
└── postgres-0

Volume B
└── postgres-1
```

Longhorn replicates storage.

PostgreSQL data is NOT replicated.

StatefulSet does not automatically provide database replication.

---

# 15. Scale StatefulSet

Scale to 3 replicas:

```bash
kubectl scale sts postgres --replicas=3
```

Verify:

```bash
kubectl get pod
```

Expected:

```text
postgres-0
postgres-1
postgres-2
```

---

# 16. Verify New PVC

```bash
kubectl get pvc
```

Expected:

```text
postgres-data-postgres-0
postgres-data-postgres-1
postgres-data-postgres-2
```

Verify PV:

```bash
kubectl get pv
```

Verify Longhorn volumes:

```bash
kubectl get volumes.longhorn.io -n longhorn-system
```

Longhorn automatically created another volume.

---

# 17. Important Production Note

Having:

```text
postgres-0
postgres-1
postgres-2
```

does NOT mean PostgreSQL High Availability.

Each PostgreSQL pod owns its own volume.

Without PostgreSQL replication technologies such as:

- Streaming Replication
- Patroni
- CloudNativePG
- CrunchyData PostgreSQL Operator
- Bitnami PostgreSQL Replication

multiple PostgreSQL replicas should not be used in production.

---

# 18. Cleanup

```bash
kubectl delete -f postgres.yaml
```

Verify:

```bash
kubectl get pod
kubectl get pvc
kubectl get pv
```

---

# Dynamic Provisioning Flow

```text
StatefulSet
      ↓
VolumeClaimTemplate
      ↓
PVC Created Automatically
      ↓
Longhorn CSI Driver
      ↓
PV Created Automatically
      ↓
Longhorn Volume Created
      ↓
Mounted to PostgreSQL Pod
      ↓
Stored on Worker Node Local Disk
```