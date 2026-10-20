# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PIP_DEFAULT_TIMEOUT=60 PIP_RETRIES=10 PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# 1) Playwright + Chromium: the big, slow step. It has its own layer so changing the other
#    requirements doesn't re-download it. Keep the version in sync with requirements.txt.
#    The pip cache mount keeps downloaded packages between builds.
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install "playwright==1.64.0" \
 && playwright install --with-deps --only-shell chromium \
 && rm -rf /var/lib/apt/lists/*

# 2) Everything else (small and quick)
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY VERSION ./VERSION
COPY app ./app
COPY entrypoint.sh /entrypoint.sh
# The entrypoint reads the Docker secrets as root, then drops to PUID:PGID (default 1000:100).
RUN sed -i 's/\r$//' /entrypoint.sh && chmod 755 /entrypoint.sh \
 && chmod -R a+rX /ms-playwright /app

EXPOSE 8080
HEALTHCHECK --interval=60s --timeout=5s CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8080/healthz')"
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers", "--forwarded-allow-ips=*"]
