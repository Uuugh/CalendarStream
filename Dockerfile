# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=60 PIP_RETRIES=10 PIP_DISABLE_PIP_VERSION_CHECK=1

LABEL org.opencontainers.image.source="https://github.com/Uuugh/CalendarStream" \
      org.opencontainers.image.description="Republishes a United CCS+ Calendar Sync schedule as a Google Calendar feed"

# curl does the downloads from CCS+ (United's Akamai protection answers curl normally)
# Debian's security fixes are applied at every build (I2, 0.2.8-beta.17), not only when the base image is renewed
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
# pip itself is upgraded first: the base image's pip had known vulnerabilities (trivy, 0.2.8-beta.16). Once the
# app is installed, pip and setuptools are removed (0.2.8-beta.17): the app never needs them, and trivy found
# High vulnerabilities in setuptools and in the msgpack and urllib3 copies pip carries.
RUN --mount=type=cache,target=/root/.cache/pip pip install --upgrade "pip>=26.1.2" && pip install -r requirements.txt \
 && pip uninstall -y pip setuptools

COPY VERSION ./VERSION
COPY app ./app
COPY entrypoint.sh /entrypoint.sh
# The entrypoint reads the Docker secrets as root, then drops to PUID:PGID (default 1000:100).
RUN sed -i 's/\r$//' /entrypoint.sh && chmod 755 /entrypoint.sh && chmod -R a+rX /app

EXPOSE 8080
HEALTHCHECK --interval=60s --timeout=5s CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8080/healthz')"
ENTRYPOINT ["/entrypoint.sh"]
# Forwarded headers (the visitor's address and https) are only trusted from these addresses. Behind a
# reverse proxy, set FORWARDED_ALLOW_IPS in .env to the proxy's address or network (e.g. 172.18.0.0/16).
ENV FORWARDED_ALLOW_IPS="127.0.0.1"
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port 8080 --proxy-headers --forwarded-allow-ips \"$FORWARDED_ALLOW_IPS\""]
