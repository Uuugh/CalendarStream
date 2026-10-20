#!/usr/bin/env bash
# CalendarStream: install it, or update an existing install (safe to run again).
#   bash <(curl -fsSL https://raw.githubusercontent.com/Uuugh/CalendarStream/main/install.sh)
# Needs Docker with Compose. If your user isn't in the docker group, run it with sudo.
set -euo pipefail
REPO=https://raw.githubusercontent.com/Uuugh/CalendarStream/main

# Where to install. If MNT_DOCKER is set (export MNT_DOCKER=/mnt/SSD/docker before running, or in
# .env), the database and .secrets/ go there and the stack files in $MNT_DOCKER/calendarstream.
# Otherwise you're asked for a folder and everything goes in it.
if [ -n "${MNT_DOCKER:-}" ]; then
  DIR="$MNT_DOCKER/calendarstream"
else
  read -rp "Install CalendarStream in [$HOME/stacks/calendarstream]: " DIR </dev/tty
  DIR="${DIR:-$HOME/stacks/calendarstream}"
fi
DATA="${MNT_DOCKER:-$DIR}"
mkdir -p "$DIR" "$DATA/.secrets"
cd "$DIR"

# The only two files the server needs; the app itself is a ready-made image.
# docker-compose.yml is always refreshed; an existing .env (your settings) is kept.
curl -fsSL "$REPO/docker-compose.yml" -o docker-compose.yml
[ -f .env ] || curl -fsSL "$REPO/.env.default" -o .env
if [ -n "${MNT_DOCKER:-}" ]; then
  sed -i "s|^#\{0,1\}MNT_DOCKER=.*|MNT_DOCKER=$MNT_DOCKER|" .env
fi

# The database password, made once at random. It also encrypts the passwords CalendarStream
# stores (CCS+, Google): keep this file, back it up, and don't change it.
if [ ! -s "$DATA/.secrets/DB_PASSWORD.txt" ]; then
  (umask 077; head -c 32 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 32 > "$DATA/.secrets/DB_PASSWORD.txt")
fi

# Start it, or update it to the newest image for IMAGE_TAG in .env (latest = stable, beta = newest).
docker compose up -d

# First install only: the status page asks for this code before you create your login.
echo "Waiting for CalendarStream to start…"
for _ in $(seq 30); do
  code=$(docker compose logs calendar_stream 2>/dev/null | grep -o 'setup code [A-F0-9-]*' | tail -1 || true)
  [ -n "$code" ] && break
  docker compose logs calendar_stream 2>/dev/null | grep -q 'Application startup complete' && break
  sleep 3
done
ip=$(hostname -I 2>/dev/null | awk '{print $1}' || true)
echo
echo "CalendarStream is in $DIR"
echo "Open http://${ip:-<this server>}:8080"
if [ -n "$code" ]; then
  echo "New install: enter the ${code} there to create your login."
fi
