# Advanced GitHub Actions Workflows - Day 11 Labs

This repo contains the demo labs used in the slides.

## Labs Included

| Lab | Topic | Workflow File |
|---|---|---|
| 01 | Manual `workflow_dispatch` + Docker Buildx | `.github/workflows/01-manual-docker-build.yml` |
| 02 | Release Tags + GitHub Release trigger | `.github/workflows/02-release-tags.yml` |
| 03 | Branch Filters + Path Filters | `.github/workflows/03-branch-path-filters.yml` |
| 04 | Conditional Jobs + Workflow Dependencies | `.github/workflows/04-conditional-dependencies.yml` |
| 05 | Artifacts + Cache Optimization | `.github/workflows/05-artifacts-cache.yml` |
| 06 | Schedule Trigger / Cron Workflow | `.github/workflows/06-schedule-cron.yml` |

## Demo Order

1. Push this repo to GitHub.
2. Go to **Actions** tab.
3. Open each workflow.
4. Run manual workflows using **Run workflow**.
5. For release/tag demo, create and push a tag.
6. For path filters, change only files under `apps/frontend`, `apps/backend`, or `docs`.

## Required Secrets for Docker Push

For ACR demo:

```text
ACR_USERNAME
ACR_PASSWORD
```

The registry name is configured in the workflow as:

```text
ACR_REGISTRY=learndevopsnow.azurecr.io
```

You can change it to your own ACR registry.
