# Deploy — fleshnet-hexsecgpt-deploy

## 1. Upload to GitHub
- https://github.com/new → create empty repo `fleshnet-hexsecgpt-deploy`
- Unzip this package and upload every file (keep folder structure)
- Commit to `main`

## 2. Create Render Web Service
- https://dashboard.render.com/select-repo?type=web → pick the new repo
- Render detects `render.yaml` and pre-fills:
  - Build: `git clone https://github.com/hexsecteam/HexSecGPT.git app || true && pip install -r requirements.txt && (test -f app/requirements.txt && pip install -r app/requirements.txt || true)`
  - Start: `uvicorn wrapper.server:app --host 0.0.0.0 --port $PORT`
- Plan: **Free**

## 3. Environment variables
- `OPENAI_API_KEY` — required
- `CLI_COMMAND` — required
- `WORKING_DIR` — required

Never commit real secrets. Set them in **Render → Environment**.

## 4. Wait for **Live**, then copy the URL
Append `/v1/chat/completions` and paste into Flesh•Net.
