---
title: FleshNet HexSecGPT
emoji: 🕸️
colorFrom: red
colorTo: black
sdk: docker
app_port: 7860
pinned: false
---

# FleshNet HexSecGPT Adapter

A Docker Space that exposes the public `hexsecteam/HexSecGPT` framework through an OpenAI-compatible HTTP endpoint.

The source repository is cloned during the Docker build. The adapter loads the repository's public provider configuration and system prompt, but avoids its interactive terminal menu.

## Required Space secret

Open **Settings → Variables and secrets → New secret** and add:

- `HEXSECGPT_API_KEY` — an API key for the selected provider.

## Optional Space variables

- `HEXSECGPT_PROVIDER` — `openrouter` (default) or `deepseek`
- `HEXSECGPT_MODEL` — overrides the model in the source repository
- `HEXSECGPT_BASE_URL` — optional OpenAI-compatible base URL override
- `HEXSECGPT_TIMEOUT_SECONDS` — defaults to `120`

## Endpoints

- `GET /health`
- `GET /v1/models`
- `POST /v1/chat/completions`

For this Space, the expected FleshNet endpoint is:

`https://nussy24-fleshnet-hexsecgpt.hf.space/v1/chat/completions`

The public GitHub repository is a framework that calls an external model provider; it is not the team's private model. Provider rules and availability still apply.
