# Docker Swarm 3-Node Lab

**Goal:** Build a simple Docker Swarm cluster with **1 manager node** and **2 worker nodes**, then test service deployment, scaling, routing mesh, rolling updates, and Docker Stack.

> This lab is for learning Docker Swarm basics. For modern production-grade orchestration, Kubernetes is usually the industry standard.

---

## 0. Lab Architecture

```text
+-------------------+        +-------------------+
|  worker-1         |        |  worker-2         |
|  10.20.1.6        |        |  10.20.1.7        |
+---------^---------+        +---------^---------+
          |                            |
          +------------+---------------+
                       |
              +--------+--------+
              |  manager-1      |
              |  10.20.1.5      |
              +-----------------+
```

Recommended VM setup:

| Node | Hostname | Example IP | Role |
|---|---|---:|---|
| Node 1 | `manager-1` | `10.20.1.5` | Swarm Manager |
| Node 2 | `worker-1`  | `10.20.1.6` | Swarm Worker |
| Node 3 | `worker-2`  | `10.20.1.7` | Swarm Worker |

You can use VirtualBox, VMware, Multipass, Proxmox, Azure VMs, or any 3 Linux machines.

---

## 1. Prerequisites

Use Ubuntu 22.04/24.04 or any Linux server with Docker installed.

Each node should be able to reach each other by IP.

Check connectivity from manager:

```bash
ping 10.20.1.6
ping 10.20.1.7
```

Check Docker:

```bash
docker version
docker info
```

---

## 2. Install Docker on All 3 Nodes

Run this on **manager-1**, **worker-1**, and **worker-2**.

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo usermod -aG docker $USER
newgrp docker
```

Verify:

```bash
docker run hello-world
```

---

## 3. Required Swarm Network Ports

Make sure these ports are open between all Swarm nodes:

| Port | Protocol | Purpose |
|---:|---|---|
| `2377` | TCP | Cluster management communication |
| `7946` | TCP/UDP | Node discovery and gossip |
| `4789` | UDP | Overlay network traffic |

If you use UFW:

```bash
sudo ufw allow 2377/tcp
sudo ufw allow 7946/tcp
sudo ufw allow 7946/udp
sudo ufw allow 4789/udp
```

---

## 4. Initialize Docker Swarm on Manager

Run this only on **manager-1**.

```bash
docker swarm init --advertise-addr 10.20.1.5 
```

You should see output like this:

```text
Swarm initialized: current node is now a manager.

To add a worker to this swarm, run the following command:

docker swarm join --token SWMTKN-1-xxxxx 10.20.1.5:2377
```

Copy the `docker swarm join` command.

Check manager node:

```bash
docker node ls
```

---

## 5. Join Worker Nodes

Run the join command on **worker-1** and **worker-2**.

Example:

```bash
docker swarm join --token SWMTKN-1-xxxxx 10.20.1.5:2377
```

Back on **manager-1**, check cluster nodes:

```bash
docker node ls
```

Expected output:

```text
ID        HOSTNAME    STATUS    AVAILABILITY   MANAGER STATUS
xxxx      manager-1   Ready     Active         Leader
xxxx      worker-1    Ready     Active
xxxx      worker-2    Ready     Active
```

If you lost the worker join command, run this on the manager:

```bash
docker swarm join-token worker
```

---

## 6. Deploy Your First Service

Run on **manager-1**.

```bash
docker service create \
  --name my-web \
  --replicas 3 \
  --publish 8080:80 \
  nginx:alpine
```

Check service:

```bash
docker service ls
docker service ps my-web
```

Access from browser or curl:

```bash
curl http://10.20.1.5:8080
curl http://10.20.1.6:8080
curl http://10.20.1.7:8080
```

Important: `8080` is available on **all Swarm nodes** because of Swarm **routing mesh**.

Even if a container is not running on a specific node, that node can still receive traffic on port `8080` and forward it to a running task.

---

## 7. Scale the Service

Scale up to 5 replicas:

```bash
docker service scale my-web=5
```

Check tasks:

```bash
docker service ps my-web
```

Scale down to 2 replicas:

```bash
docker service scale my-web=2
```

Check again:

```bash
docker service ps my-web
```

---

## 8. Test Self-Healing

Find where tasks are running:

```bash
docker service ps my-web
```

On one worker node, stop/remove one running container manually:

```bash
docker ps

docker rm -f <container_id>
```

Back on manager:

```bash
docker service ps my-web
```

Docker Swarm should automatically create a replacement task to maintain the desired replica count.

---

## 9. Rolling Update Test

Update the service image:

```bash
docker service update \
  --image nginx:1.25-alpine \
  --update-parallelism 1 \
  --update-delay 10s \
  my-web
```

Watch the update:

```bash
docker service ps my-web
```

Rollback if needed:

```bash
docker service rollback my-web
```

---

## 10. Create Overlay Network

Create an overlay network for multi-service communication:

```bash
docker network create \
  --driver overlay \
  app-net
```

Check network:

```bash
docker network ls
docker network inspect app-net
```

---

## 11. Deploy a Multi-Service Stack

Docker Stack uses a Compose-style YAML file to deploy multi-service apps into Swarm.

Important Swarm notes:

- Use `deploy.replicas` to define replicas.
- Avoid `container_name` in Swarm because replicas need unique task names.
- `docker stack deploy` does not build images from `build:`. Use prebuilt images from Docker Hub/private registry, or build and push your image first.
- For a real backend app, publish your backend image first, then reference it with `image:`.

Create a folder:

```bash
mkdir swarm-stack-lab
cd swarm-stack-lab
```

Create `docker-compose.yml`:

```yaml
version: "3.8"

services:
  backend:
    image: your-dockerhub-username/compose-backend:1.0.0 ## Backend Application Image we used in docker compose lab 
    ports:
      - "5001:5000"
    networks:
      - compose-net
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure

  mysql:
    image: mysql:8.0
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: compose_demo
      MYSQL_USER: appuser
      MYSQL_PASSWORD: apppassword
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - compose-net
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - compose-net
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure

networks:
  compose-net:
    driver: overlay ## Don't Use Bridge 

volumes:
  mysql_data:
```

Deploy the stack:

```bash
docker stack deploy -c docker-compose.yml myapp
```

Check stack:

```bash
docker stack ls
docker stack services myapp
docker stack ps myapp
```

Access backend service:

```bash
curl http://10.20.1.5:5001
curl http://10.20.1.6:5001
curl http://10.20.1.7:5001
```

Because of routing mesh, port `5001` works from **any node IP**.

Connect to MySQL:

```bash
mysql -h 10.20.1.5 -P 3306 -u appuser -papppassword compose_demo
```

Connect to Redis:

```bash
redis-cli -h 10.20.1.5 -p 6379
```

Scale backend service to 5 replicas:

```bash
docker service scale myapp_backend=5
```

Check replicas:

```bash
docker stack services myapp
docker service ps myapp_backend
```

---

## 12. Useful Swarm Commands

```bash
# Cluster nodes
docker node ls

# Services
docker service ls
docker service ps <service_name>
docker service inspect <service_name>
docker service logs <service_name>

# Scale service
docker service scale myapp_backend=5

# Update service image
docker service update --image nginx:1.25-alpine myapp_backend

# Stacks
docker stack ls
docker stack services myapp
docker stack ps myapp

# Remove stack
docker stack rm myapp

# Remove service
docker service rm my-web

# Leave swarm from worker
docker swarm leave

# Leave swarm from manager
docker swarm leave --force
```

---

## 13. Clean Up

Remove service:

```bash
docker service rm my-web
```

Remove stack:

```bash
docker stack rm myapp
```

Remove overlay network if still exists:

```bash
docker network rm app-net
```

Worker nodes leave swarm:

```bash
docker swarm leave
```

Manager leaves swarm:

```bash
docker swarm leave --force
```

---

## 14. Key Takeaways

- Docker Swarm turns multiple Docker hosts into one cluster.
- Manager nodes control scheduling and cluster state.
- Worker nodes run containers/tasks.
- Services define desired state.
- Replicas define how many tasks should run.
- Routing mesh exposes published ports on every node.
- Docker Stack lets you deploy multi-service apps using a Compose-style file.
- Swarm is simple and useful for learning, labs, small clusters, and lightweight use cases.
- Kubernetes is usually better for large-scale, cloud-native, production-grade platforms.
