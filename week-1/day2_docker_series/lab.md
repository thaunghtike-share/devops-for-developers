# Docker Series - Day 2 Commands

## Verify Docker Installation

```bash
docker --version
```

Check Docker CLI version.

```bash
docker info
```

Verify Docker Engine is running correctly.

---

## Run First Container

```bash
docker pull hello-world
```

Download hello-world image from Docker Hub.

```bash
docker run hello-world
```

Run first container and verify Docker works.

---

## Run Containers in Different Modes

```bash
docker run -it ubuntu bash
```

Run Ubuntu container in interactive terminal mode.

```bash
ls
```

List files inside the container.

```bash
docker run -d -p 8080:80 nginx
docker run -d --name web-server -p 8081:80 nginx 
```

Run nginx container in background mode with port mapping.

```bash
docker run --rm ubuntu echo "Hello DevOps"
```

Run temporary container and auto remove after exit.

---

## View Running Containers

```bash
docker ps
```

Show currently running containers.

---

## View All Containers & Logs

```bash
docker ps -a
```

Show all containers including stopped containers.

```bash
docker logs test-container
```

View container logs.

---

## Control Container Lifecycle

```bash
docker stop web-server
```

Stop running container.

```bash
docker start web-server
```

Start stopped container.

```bash
docker restart web-server
```

Restart container.

```bash
docker rm web-server
```

Remove container.

---

## Access Running Container

```bash
docker exec -it web-server /bin/bash
```

Access running container terminal.

```bash
cat /etc/os-release
```

Check OS information inside container.

---

## Cleanup Commands

```bash
docker container prune
```

Remove all stopped containers.

```bash
docker system prune
```

Remove unused Docker resources.
