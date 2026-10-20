#!/usr/bin/env bash
# CalendarStream: install it, or update an existing install (safe to run again).
#   bash <(curl -fsSL https://raw.githubusercontent.com/Uuugh/CalendarStream/main/install.sh)
# Needs Docker with Compose. If your user isn't in the docker group, run it with sudo.
set -euo pipefail
REPO=https://raw.githubusercontent.com/Uuugh/CalendarStream/main

# 1. The stack folder: where docker-compose.yml and .env go (asked every time; press Enter to keep it).
read -rp "Folder for docker-compose.yml and .env [$HOME/stacks/calendarstream]: " DIR </dev/tty
DIR="${DIR:-$HOME/stacks/calendarstream}"
DIR="$(realpath -m "${DIR/#\~/$HOME}")"
mkdir -p "$DIR"
cd "$DIR"

# 2. The data folder (MNT_DOCKER): where CalendarStream keeps its config and data, the database
#    (calendar_stream/postgres) and .secrets/. It's saved in .env, so it's only asked once; set it
#    beforehand to skip the question (MNT_DOCKER=/mnt/SSD/docker bash install.sh).
if [ -z "${MNT_DOCKER:-}" ] && [ -f .env ]; then
  MNT_DOCKER="$(sed -n 's/^MNT_DOCKER=//p' .env | tail -1 | tr -d '"'"'")"
fi
if [ -z "${MNT_DOCKER:-}" ]; then
  read -rp "Folder for CalendarStream's config and data (database, .secrets) [$DIR]: " MNT_DOCKER </dev/tty
  MNT_DOCKER="${MNT_DOCKER:-$DIR}"
fi
MNT_DOCKER="$(realpath -m "${MNT_DOCKER/#\~/$HOME}")"
DATA="$MNT_DOCKER"
mkdir -p "$DATA/.secrets"

# The only two files the server needs; the app itself is a ready-made image.
# docker-compose.yml is always refreshed; an existing .env (your settings) is kept.
curl -fsSL "$REPO/docker-compose.yml" -o docker-compose.yml
[ -f .env ] || curl -fsSL "$REPO/.env.default" -o .env
# Remember the data folder in .env, so docker compose (and the next run) use it.
if grep -q '^#\{0,1\}MNT_DOCKER=' .env; then
  sed -i "s|^#\{0,1\}MNT_DOCKER=.*|MNT_DOCKER=$MNT_DOCKER|" .env
else
  printf '\nMNT_DOCKER=%s\n' "$MNT_DOCKER" >> .env
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
echo "CalendarStream: docker-compose.yml and .env in $DIR, config and data in $DATA"
echo "Open http://${ip:-<this server>}:8080"
if [ -n "$code" ]; then
  echo "New install: enter the ${code} there to create your login."
fi
