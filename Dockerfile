FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 1000 user

USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    SOURCE_DIR=/home/user/app/source

WORKDIR $HOME/app

COPY --chown=user requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

ARG SOURCE_REPO_URL=https://github.com/hexsecteam/HexSecGPT.git
RUN git clone --depth 1 "$SOURCE_REPO_URL" source \
    && if [ -f source/requirements.txt ]; then pip install --no-cache-dir -r source/requirements.txt; fi

COPY --chown=user wrapper ./wrapper
COPY --chown=user README.md DEPLOY.md .env.example ./

EXPOSE 7860
CMD ["uvicorn", "wrapper.server:app", "--host", "0.0.0.0", "--port", "7860"]
