# Day 11 - Advanced GitHub Actions Workflows Labs

## Lab 01 - Manual Workflow Dispatch + Docker Buildx

### Goal
Manually trigger a workflow and choose which Docker service to build.

### Files

```text
.github/workflows/01-manual-docker-build.yml
apps/frontend/Dockerfile
apps/backend/Dockerfile
apps/integration/Dockerfile
```

### Demo Steps

```bash
git add .
git commit -m "add day 11 advanced github actions labs"
git push origin main
```

Then go to:

```text
GitHub Repo > Actions > Manual Docker Build > Run workflow
```

Choose service:

```text
frontend
backend
integration
```

---

## Lab 02 - Release Tags + GitHub Release Trigger

### Goal
Trigger workflow when a version tag or GitHub Release is created.

### Tag Demo

```bash
git tag v1.0.0
git push origin v1.0.0
```

### GitHub Release Demo

```text
GitHub Repo > Releases > Draft a new release > Tag v1.0.1 > Publish release
```

---

## Lab 03 - Branch Filters + Path Filters

### Goal
Run workflows only when specific branches and folders are changed.

### Frontend Change Demo

```bash
echo "frontend update" >> apps/frontend/index.html
git add .
git commit -m "update frontend"
git push origin main
```

### Backend Change Demo

```bash
echo "backend update" >> apps/backend/app.py
git add .
git commit -m "update backend"
git push origin main
```

### Docs Change Demo

```bash
echo "docs update" >> docs/readme.md
git add .
git commit -m "update docs"
git push origin main
```

---

## Lab 04 - Conditional Jobs + Workflow Dependencies

### Goal
Use `needs`, `if`, and job outputs to control pipeline flow.

### Demo

```text
GitHub Repo > Actions > Conditional Jobs and Dependencies > Run workflow
```

Try both values:

```text
run_deploy = true
run_deploy = false
```

---

## Lab 05 - Artifacts + Cache Optimization

### Goal
Upload build output as artifact and speed up dependency installation using cache.

### Demo

```bash
echo "artifact demo" >> apps/frontend/index.html
git add .
git commit -m "test artifact and cache"
git push origin main
```

After workflow finishes:

```text
GitHub Repo > Actions > Workflow Run > Artifacts
```

---

## Lab 06 - Schedule Trigger / Cron Workflow

### Goal
Run a workflow automatically using cron schedule.

### Manual Test

```text
GitHub Repo > Actions > Scheduled Health Check > Run workflow
```

### Cron Example

```yaml
schedule:
  - cron: "0 1 * * *"
```

This means the workflow runs every day at 01:00 UTC.
