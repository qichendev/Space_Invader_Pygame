# Space Invaders

A classic Space Invaders game built with Python and Pygame, deployable as a web app via Pygbag.

**Course:** CSD-4503 - DevOps Tools and Practices

## Team

| Name | Student ID |
|------|------------|
| Ami Valand | C0956779 |
| Nikita Nikita | C0958762 |
| Deadeepya Kognati | C0959068 |
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

## Run locally (desktop)

```bash
uv sync
uv run python main.py
```

## Run locally (web preview)

```bash
uv sync --all-groups
uv run dev
```

Then open `http://localhost:8000` in your browser.

## Build static web files

```bash
uv run build
```

Output is written to `build/web/`. Deploy that directory to any static host.

## Deploy to Azure Static Web Apps

Deployment is automated via GitHub Actions on every push to `main`.

**One-time setup:**

1. Create an Azure Static Web App (Free tier, deployment source: *Other*)
2. Copy the deployment token from **Azure Portal → your app → Manage deployment token**
3. Add it to GitHub: **Settings → Secrets → Actions → `AZURE_STATIC_WEB_APPS_API_TOKEN`**

The workflow (`.github/workflows/deploy.yml`) will then:
- Build the web app with Pygbag on every push to `main`
- Deploy to production automatically
- Create a preview environment for each pull request
