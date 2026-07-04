# Kubernetes Job & CronJob Lab - PSQL Backup to AWS S3

## Goal

Create a PostgreSQL database in Kubernetes, then back it up to AWS S3.

The backup flow is:

1. One container runs `pg_dump`.
2. The same container uploads the backup file to S3.

The Job and CronJob use the same logic.

---

# 1. Set AWS Values

Do not write real AWS keys into YAML files.

```bash
export AWS_ACCESS_KEY_ID="<ACCESS_KEY_ID>"
export AWS_SECRET_ACCESS_KEY="<SECRET_ACCESS_KEY>"
export AWS_DEFAULT_REGION="ap-southeast-1"
export S3_BUCKET="psql-backup-demo-$(date +%s)"
```

Create the S3 bucket:

```bash
aws s3api create-bucket \
  --bucket "$S3_BUCKET" \
  --region "$AWS_DEFAULT_REGION" \
  --create-bucket-configuration LocationConstraint="$AWS_DEFAULT_REGION"
```

Check:

```bash
aws s3 ls "s3://$S3_BUCKET"
```

---

# 2. Create Namespaces

```bash
kubectl create namespace database
kubectl create namespace backup
```

---

# 3. Create PSQL Secret

Secret name: `psql`

```bash
cat > psql-secret.yaml <<'EOF'
apiVersion: v1
kind: Secret
metadata:
  name: psql
  namespace: database
type: Opaque
stringData:
  POSTGRES_USER: admin
  POSTGRES_PASSWORD: password123
  POSTGRES_DB: app
EOF

kubectl apply -f psql-secret.yaml
```

---

# 4. Create PSQL Database

File: `psql.yaml`

```bash
cat > psql.yaml <<'EOF'
apiVersion: v1
kind: Service
metadata:
  name: psql
  namespace: database
spec:
  selector:
    app: psql
  ports:
    - port: 5432
      targetPort: 5432
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: psql
  namespace: database
spec:
  serviceName: psql
  replicas: 1
  selector:
    matchLabels:
      app: psql
  template:
    metadata:
      labels:
        app: psql
    spec:
      containers:
        - name: psql
          image: postgres:16.1
          envFrom:
            - secretRef:
                name: psql
          env:
            - name: PGDATA
              value: /var/lib/postgresql/data/pgdata
          ports:
            - containerPort: 5432
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes:
          - ReadWriteOnce
        resources:
          requests:
            storage: 5Gi
EOF

kubectl apply -f psql.yaml
kubectl rollout status statefulset/psql -n database
```

---

# 5. Insert Sample Data

Open PSQL:

```bash
kubectl exec -it psql-0 -n database -- psql -U admin -d app
```

Run SQL:

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name TEXT
);

INSERT INTO users(name) VALUES ('Mg Mg'), ('Aung Aung');

SELECT * FROM users;

\q
```

---

# 6. Create AWS Secret

Secret name: `aws`

```bash
kubectl create secret generic aws \
  -n backup \
  --from-literal=AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
  --from-literal=AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
  --from-literal=AWS_DEFAULT_REGION="$AWS_DEFAULT_REGION" \
  --from-literal=S3_BUCKET="$S3_BUCKET"
```

---

# 7. Backup Job

File: `psql-backup-job.yaml`

```bash
cat > psql-backup-job.yaml <<'EOF'
apiVersion: batch/v1
kind: Job
metadata:
  name: psql-backup
  namespace: backup
spec:
  backoffLimit: 3
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: backup
          image: postgres:16.1
          envFrom:
            - secretRef:
                name: aws
          env:
            - name: DB_HOST
              value: psql.database.svc.cluster.local
            - name: DB_PORT
              value: "5432"
            - name: DB_USER
              value: admin
            - name: PGPASSWORD
              value: password123
            - name: DB_NAME
              value: app
          command:
            - sh
            - -c
            - |
              apt-get update
              apt-get install -y awscli

              DATE=$(date +%Y-%m-%d-%H-%M-%S)
              FILE="/tmp/app-${DATE}.sql.gz"

              pg_dump \
                -h "$DB_HOST" \
                -p "$DB_PORT" \
                -U "$DB_USER" \
                -d "$DB_NAME" \
                | gzip > "$FILE"

              aws s3 cp \
                "$FILE" \
                "s3://$S3_BUCKET/psql/job/app-${DATE}.sql.gz"
EOF

kubectl apply -f psql-backup-job.yaml
```

Check:

```bash
kubectl get pods -n backup
kubectl logs -f job/psql-backup -n backup
aws s3 ls "s3://$S3_BUCKET/psql/job/"
```

Retry:

```bash
kubectl delete job psql-backup -n backup
kubectl apply -f psql-backup-job.yaml
```

---

# 8. Backup CronJob

File: `psql-backup-cronjob.yaml`

```bash
cat > psql-backup-cronjob.yaml <<'EOF'
apiVersion: batch/v1
kind: CronJob
metadata:
  name: psql-backup
  namespace: backup
spec:
  schedule: "*/3 * * * *"
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 3
  jobTemplate:
    spec:
      backoffLimit: 3
      template:
        spec:
          restartPolicy: Never
          containers:
            - name: backup
              image: postgres:16.1
              envFrom:
                - secretRef:
                    name: aws
              env:
                - name: DB_HOST
                  value: psql.database.svc.cluster.local
                - name: DB_PORT
                  value: "5432"
                - name: DB_USER
                  value: admin
                - name: PGPASSWORD
                  value: password123
                - name: DB_NAME
                  value: app
              command:
                - sh
                - -c
                - |
                  apt-get update
                  apt-get install -y awscli

                  DATE=$(date +%Y-%m-%d-%H-%M-%S)
                  FILE="/tmp/app-${DATE}.sql.gz"

                  pg_dump \
                    -h "$DB_HOST" \
                    -p "$DB_PORT" \
                    -U "$DB_USER" \
                    -d "$DB_NAME" \
                    | gzip > "$FILE"

                  aws s3 cp \
                    "$FILE" \
                    "s3://$S3_BUCKET/psql/cronjob/app-${DATE}.sql.gz"
EOF

kubectl apply -f psql-backup-cronjob.yaml
```

Check:

```bash
kubectl get cronjob -n backup
kubectl get jobs -n backup
aws s3 ls "s3://$S3_BUCKET/psql/cronjob/"
```

---

# 9. Run CronJob Manually

```bash
kubectl create job \
  --from=cronjob/psql-backup \
  psql-backup-manual \
  -n backup
```

Check:

```bash
kubectl get jobs -n backup
kubectl logs job/psql-backup-manual -n backup
```

---

# 10. Suspend CronJob

```bash
kubectl patch cronjob psql-backup \
  -n backup \
  -p '{"spec":{"suspend":true}}'
```

---

# 11. Resume CronJob

```bash
kubectl patch cronjob psql-backup \
  -n backup \
  -p '{"spec":{"suspend":false}}'
```

---

# 12. Cleanup

```bash
kubectl delete namespace backup
kubectl delete namespace database

aws s3 rm "s3://$S3_BUCKET" --recursive
aws s3api delete-bucket \
  --bucket "$S3_BUCKET" \
  --region "$AWS_DEFAULT_REGION"
```
