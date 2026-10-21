# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=60 PIP_RETRIES=10 PIP_DISABLE_PIP_VERSION_CHECK=1

LABEL org.opencontainers.image.source="https://github.com/Uuugh/CalendarStream" \
      org.opencontainers.image.description="Republishes a United CCS+ Calendar Sync schedule as a Google Calendar feed"

# curl does the downloads from CCS+ (United's Akamai protection answers curl normally)
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY VERSION ./VERSION
COPY app ./app
COPY entrypoint.sh /entrypoint.sh
# The entrypoint reads the Docker secrets as root, then drops to PUID:PGID (default 1000:100).
RUN sed -i 's/\r$//' /entrypoint.sh && chmod 755 /entrypoint.sh && chmod -R a+rX /app

EXPOSE 8080
HEALTHCHECK --interval=60s --timeout=5s CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8080/healthz')"
ENTRYPOINT ["/entrypoint.sh"]
# Forwarded headers (the visitor's address and https) are only trusted from proxies on private networks
# (a reverse proxy in Docker or on the LAN). Set FORWARDED_ALLOW_IPS to your proxy's address to narrow it.
ENV FORWARDED_ALLOW_IPS="127.0.0.1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,fc00::/7"
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port 8080 --proxy-headers --forwarded-allow-ips \"$FORWARDED_ALLOW_IPS\""]
