# Space Invaders

**Download:** https://lively-smoke-01b8a7b1e.6.azurestaticapps.net

A classic Space Invaders game built with Python and Pygame.

**Course:** CSD-4503 - DevOps Tools and Practices

## Team

| Name | Student ID |
|------|------------|
| Ami Valand | C0956779 |
| Nikita Nikita | C0958762 |
| Deadeepya Koganti | C0959068 |
| Qi Chen | C0944666 |
| Anmol Kaur | C0949650 |
| Payal Patel | C0959412 |

## Gameplay

- Defeat all enemies before they reach the bottom
- Collect cyan power-ups for a 5-second wide-beam shot
- 3 lives per game

| Key | Action |
|-----|--------|
| `←` `→` | Move |
| `Space` | Shoot |
| `P` | Pause / Resume |
| `R` | Restart (after Game Over) |

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Run locally

```bash
uv sync
uv run python main.py
```

## Build executable

```bash
uv sync --all-groups
uv run pyinstaller space_invader.spec
```

Output is written to `dist/`. The executable bundles all game assets and runs without Python installed.

## Deploy

Deployment is automated via GitHub Actions on every push to `main`.

The workflow:
1. Builds executables for Windows, macOS, and Linux in parallel
2. Publishes them to **GitHub Releases** (tag: `latest`)
3. Deploys the download landing page to **Azure Static Web Apps**

**One-time setup:**

1. Create an Azure Static Web App (Free tier, deployment source: *Other*)
2. Copy the deployment token from **Azure Portal → your app → Manage deployment token**
3. Add it to GitHub: **Settings → Secrets → Actions → `AZURE_STATIC_WEB_APPS_API_TOKEN`**
