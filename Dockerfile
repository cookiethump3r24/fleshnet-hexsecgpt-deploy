FROM python:3.11-slim
WORKDIR /srv
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN git clone https://github.com/hexsecteam/HexSecGPT.git app || true \
  && if [ -f app/requirements.txt ]; then pip install --no-cache-dir -r app/requirements.txt; fi
EXPOSE 8080
CMD ["uvicorn", "wrapper.server:app", "--host", "0.0.0.0", "--port", "8080"]
