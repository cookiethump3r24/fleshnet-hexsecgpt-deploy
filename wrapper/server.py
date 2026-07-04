"""OpenAI-compatible adapter that shells out to the source repo's CLI.

Exposes:
  GET  /health
  POST /v1/chat/completions

For each chat request the latest user message is written to the CLI's stdin
and its stdout is returned as the assistant reply. No repo code runs at
import time — CLI_COMMAND is only executed here, on Render, at request time.
"""
import os, shlex, asyncio, time, uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

CLI_COMMAND = os.environ.get("CLI_COMMAND", "python")
WORKING_DIR = os.environ.get("WORKING_DIR", "app")
TIMEOUT_S = float(os.environ.get("CLI_TIMEOUT", "120"))

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True, "cli": CLI_COMMAND, "cwd": WORKING_DIR}

def _extract_user_message(body: dict) -> str:
    msgs = body.get("messages") or []
    for m in reversed(msgs):
        if isinstance(m, dict) and m.get("role") == "user":
            c = m.get("content")
            if isinstance(c, str):
                return c
            if isinstance(c, list):
                return "".join(p.get("text", "") for p in c if isinstance(p, dict))
    if isinstance(body.get("prompt"), str):
        return body["prompt"]
    return ""

@app.post("/v1/chat/completions")
async def chat(req: Request):
    try:
        body = await req.json()
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": {"message": f"invalid json: {e}"}})

    user_msg = _extract_user_message(body)
    if not user_msg:
        return JSONResponse(status_code=400, content={"error": {"message": "no user message found in request"}})

    try:
        argv = shlex.split(CLI_COMMAND)
        proc = await asyncio.create_subprocess_exec(
            *argv,
            cwd=WORKING_DIR if os.path.isdir(WORKING_DIR) else None,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(input=user_msg.encode("utf-8")), timeout=TIMEOUT_S,
            )
        except asyncio.TimeoutError:
            proc.kill()
            return JSONResponse(status_code=504, content={"error": {"message": f"CLI timed out after {TIMEOUT_S}s"}})
    except FileNotFoundError as e:
        return JSONResponse(status_code=500, content={"error": {"message": f"CLI not found: {e}", "cli": CLI_COMMAND}})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": {"message": f"CLI spawn failed: {e}"}})

    if proc.returncode != 0:
        return JSONResponse(status_code=502, content={"error": {
            "message": f"CLI exited with code {proc.returncode}",
            "stderr": stderr.decode("utf-8", errors="replace")[-2000:],
        }})

    content = stdout.decode("utf-8", errors="replace").strip()
    return {
        "id": f"chatcmpl-{uuid.uuid4().hex[:24]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": body.get("model") or "cli-wrapper",
        "choices": [{"index": 0, "message": {"role": "assistant", "content": content}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }
