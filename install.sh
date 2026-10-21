#!/usr/bin/env bash
# CalendarStream: install it, or update an existing install (safe to run again).
#   bash <(curl -fsSL https://raw.githubusercontent.com/Uuugh/CalendarStream/main/install.sh)
# Needs Docker with Compose. Works on Linux, on macOS (Docker Desktop) and on Windows inside WSL.
# If your user isn't allowed to run docker, use: sudo bash -c "$(curl -fsSL <the URL above>)"
# Every question shows its default in [brackets]; press Enter to keep it. On a later run the
# defaults are your current settings, so pressing Enter all the way just updates CalendarStream.
set -euo pipefail
REPO=https://raw.githubusercontent.com/Uuugh/CalendarStream/main

ask() {   # $1 = question, $2 = default; prints the answer (or the default)
  local answer
  read -rp "$1 [$2]: " answer </dev/tty
  printf '%s' "${answer:-$2}"
}
absolute() {   # ~ and relative paths -> absolute (portable: macOS has no "realpath -m")
  local p="${1/#\~/$HOME}"
  case "$p" in /*) ;; *) p="$PWD/$p" ;; esac
  printf '%s' "${p%/}"
}
env_value() {   # $1 = file, $2 = name: the value in a .env file, without quotes
  [ -f "$1" ] && sed -n "s/^$2=//p" "$1" | tail -1 | tr -d '"'"'" || true
}
this_ip() {   # this computer's address on the network (Linux, then macOS)
  local ip
  ip="$(hostname -I 2>/dev/null | awk '{print $1}' || true)"   # macOS has no "hostname -I"
  [ -n "$ip" ] || ip="$(ipconfig getifaddr en0 2>/dev/null || true)"
  printf '%s' "$ip"
}

# Where an earlier install is: the current folder if it holds CalendarStream, else the usual place.
if [ -f docker-compose.yml ] && grep -q calendarstream docker-compose.yml 2>/dev/null; then
  OLD_DIR="$PWD"
else
  OLD_DIR="$HOME/stacks/calendarstream"
fi
OLD_ENV="$OLD_DIR/.env"

# 1. Which release: stable (the "latest" image, the default) or beta (the newest, still being tested).
CURRENT="$(env_value "$OLD_ENV" IMAGE_TAG)"
case "$CURRENT" in beta) DEFAULT=beta ;; ""|latest) DEFAULT=stable ;; *) DEFAULT="$CURRENT" ;; esac
CHANNEL="$(ask "Which release would you like to install, latest (stable) or beta" "$DEFAULT" | tr '[:upper:]' '[:lower:]')"
case "$CHANNEL" in
  stable|latest) IMAGE_TAG=latest ;;
  beta) IMAGE_TAG=beta ;;
  [0-9]*.[0-9]*.[0-9]*) IMAGE_TAG="$CHANNEL" ;;    # an exact version, e.g. 0.1.9
  *) echo "Please answer latest (stable) or beta." >&2; exit 1 ;;
esac

# 2. The stack folder: where docker-compose.yml and .env go.
DIR="$(absolute "$(ask "Folder for docker-compose.yml and .env" "$OLD_DIR")")"
mkdir -p "$DIR"
cd "$DIR"

# 3. The config and data folder (MNT_DOCKER): the database (calendar_stream/postgres) and .secrets/.
#    Always asked, so you can confirm it; the default is the current one, or the stack folder.
CURRENT_DATA="${MNT_DOCKER:-$(env_value .env MNT_DOCKER)}"
MNT_DOCKER="$(absolute "$(ask "Folder for CalendarStream's config and data (database, .secrets)" "${CURRENT_DATA:-$DIR}")")"
mkdir -p "$MNT_DOCKER/.secrets"

# 4. The public address: the https:// address people (and Google) reach the status page at, e.g.
#    https://cal.example.com. Leave it empty if you don't have one yet: the page then uses the address
#    it's opened at, and it can be set later in ☰ Settings → Public address (which takes priority).
#    "-" clears an earlier answer.
IP="$(this_ip)"
CURRENT_URL="$(env_value .env PUBLIC_URL)"
case "$CURRENT_URL" in http://[0-9]*:8080|http://localhost:8080) CURRENT_URL="" ;; esac   # old defaults (http://<IP or localhost>:8080) aren't public addresses
PUBLIC_URL="$(ask "Public https:// address, if you have one (Enter to skip; may be set later in Settings)" "${CURRENT_URL}")"
[ "$PUBLIC_URL" = "-" ] && PUBLIC_URL=""

# The only two files the server needs; the app itself is a ready-made image.
# docker-compose.yml is always refreshed; an existing .env (your settings) is kept, apart from the
# answers above, which are written into it.
curl -fsSL "$REPO/docker-compose.yml" -o docker-compose.yml
[ -f .env ] || curl -fsSL "$REPO/.env.default" -o .env
chmod 600 .env   # it can hold secrets (e.g. FEED_TOKEN)
set_env() {   # $1 = name, $2 = value ("sed -i.bak" works with both GNU and macOS sed)
  local v; v="$(printf '%s' "$2" | sed 's/[\\|&]/\\&/g')"   # escape \ | & for the replacement
  if grep -q "^#\{0,1\}$1=" .env; then
    sed -i.bak "s|^#\{0,1\}$1=.*|$1=$v|" .env && rm -f .env.bak
  else
    printf '\n%s=%s\n' "$1" "$2" >> .env
  fi
}
set_env IMAGE_TAG "$IMAGE_TAG"
set_env MNT_DOCKER "$MNT_DOCKER"
set_env PUBLIC_URL "$PUBLIC_URL"

# The database password, made once at random. It also encrypts the passwords CalendarStream
# stores (CCS+, Google): keep this file, back it up, and don't change it.
if [ ! -s "$MNT_DOCKER/.secrets/DB_PASSWORD.txt" ]; then
  (umask 077; head -c 32 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 32 > "$MNT_DOCKER/.secrets/DB_PASSWORD.txt")
fi

# Start it, or update it to the newest image of the chosen release.
docker compose up -d

# First install only: the status page asks for this code before you create your login.
echo "Waiting for CalendarStream to start…"
code=""
for _ in $(seq 30); do
  code=$(docker compose logs 2>/dev/null | grep -o 'setup code [A-F0-9-]*' | tail -1 || true)
  [ -n "$code" ] && break
  docker compose logs 2>/dev/null | grep -q 'Application startup complete' && break
  sleep 3
done
echo
echo "CalendarStream ($([ "$IMAGE_TAG" = latest ] && echo stable || echo "$IMAGE_TAG")): docker-compose.yml and .env in $DIR, config and data in $MNT_DOCKER"
echo "Open ${PUBLIC_URL:-http://${IP:-localhost}:8080}"
if [ -n "$code" ]; then
  echo "New install: enter the ${code} there to create your login."
fi
