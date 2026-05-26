# Docker Day 4 - Full CLI Testing Guide

## Step 1 - Go To Project

```bash
cd python-docker-app
```

---

## Step 2 - Verify Files

```bash
ls
```

Expected:

```text
app.py
requirements.txt
Dockerfile
.dockerignore
README.md
```

---

## Step 3 - Build Docker Image

```bash
docker build -t python-flask-app:1.0 .
```

---

## Step 4 - Verify Docker Image

```bash
docker images
```

---

## Step 5 - Run Container

```bash
docker run -d \
  --name flask-app \
  -p 8000:5000 \
  python-flask-app:1.0
```

---

## Step 6 - Verify Running Container

```bash
docker ps
```

---

## Step 7 - Test Application In Browser

```text
http://localhost:8000
```

---

## Step 8 - Test Using Curl

```bash
curl http://localhost:8000
```

---

## Step 9 - View Container Logs

```bash
docker logs flask-app
```

---

## Step 10 - Enter Running Container

```bash
docker exec -it flask-app /bin/bash
```

If bash does not exist:

```bash
docker exec -it flask-app /bin/sh
```

---

## Step 11 - Verify Files Inside Container

```bash
ls
```

---

## Step 12 - Verify Environment Variables

```bash
printenv

echo $APP_NAME
```

---

## Step 13 - Exit Container

```bash
exit
```

---

## Step 14 - Test ENV Variable Override

```bash
docker run -d \
  --name flask-app-prod \
  -p 8001:5000 \
  -e APP_NAME="Production App" \
  python-flask-app:1.0
```

---

## Step 15 - Verify ENV Override

```bash
curl http://localhost:8001
```

Expected:

```text
Production App
```

---

## Step 16 - Stop Container

```bash
docker stop flask-app
```

---

## Step 17 - Start Container Again

```bash
docker start flask-app
```

---

## Step 18 - Restart Container

```bash
docker restart flask-app
```

---

## Step 19 - Remove Container

```bash
docker stop flask-app

docker rm flask-app
```

## Step 20 - Inspect Running Container

```bash
docker inspect flask-app-prod
```

---

## Step 21 - Tag Docker Image

```bash
docker tag python-flask-app:1.0 yourdockerhub/python-flask-app:1.0
```

---

## Step 22 - Login To Docker Hub

```bash
docker login
```

---

## Step 23 - Push Image To Docker Hub

```bash
docker push yourdockerhub/python-flask-app:1.0
```

---

## Step 24 - Pull Image From Docker Hub

```bash
docker pull yourdockerhub/python-flask-app:1.0
```

---

## Step 25 - Remove Docker Image

```bash
docker rmi python-flask-app:1.0
```

---

## Step 26 - Cleanup Everything

```bash
docker stop flask-app-prod

docker rm flask-app-prod
```
