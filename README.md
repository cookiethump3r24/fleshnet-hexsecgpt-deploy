# fleshnet-hexsecgpt-deploy

Auto-generated deployment package produced by **Flesh•Net** for
[hexsecteam/HexSecGPT](https://github.com/hexsecteam/HexSecGPT).
No repository code was executed to build this ZIP.

## Contents
- `wrapper/server.py` — OpenAI-compatible HTTP adapter that
  shells out to the original CLI (`CLI_COMMAND`) and returns its stdout.
- `requirements.txt` — wrapper runtime deps.
- `render.yaml` — Render service definition (free plan).
- `Dockerfile` — optional container build.
- `.env.example` — required and optional environment variables.
- `DEPLOY.md` — step-by-step Render deployment guide.

## How it works
On Render, the build clones the original repo into `app/` and installs its
dependencies alongside the wrapper's. At request time the wrapper spawns
`CLI_COMMAND` inside `WORKING_DIR` (default `app`), pipes the latest user
message to stdin, and returns stdout as an OpenAI-compatible response.

## Endpoint
After deploy: `https://YOUR-RENDER-APP.onrender.com/v1/chat/completions`

Paste this URL into Flesh•Net → **Settings → GitHub QuickConnect** → Save & test.
