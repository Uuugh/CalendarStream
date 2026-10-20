#!/bin/sh
# Reads the Docker secrets while still root, then drops to PUID:PGID to run the app.
# All project data lives in Postgres, so the container itself keeps nothing.
set -e

PUID="${PUID:-1000}"
PGID="${PGID:-100}"

if [ "$(id -u)" = "0" ]; then
    # *_FILE variables (set in docker-compose.yml) point at Docker secrets. Read them while still
    # root (host secret files are often root-only) and pass the values on as plain variables.
    load_secret() {  # $1 = variable name, $2 = default secret path
        eval "file=\${${1}_FILE:-$2}"
        if [ -f "$file" ]; then
            eval "$1=\$(tr -d '\r\n' < \"\$file\")"; export "$1"
        else
            eval "set_by_compose=\${${1}_FILE:-}"
            [ -n "$set_by_compose" ] && echo "WARNING: ${1}_FILE=$file not found; is that secret mounted?" >&2
        fi
        return 0
    }
    load_secret CCS_USERNAME /run/secrets/CCS_USER
    load_secret CCS_PASSWORD /run/secrets/CCS_PASSWORD
    load_secret GUI_USERNAME /run/secrets/GUI_USER
    load_secret GUI_PASSWORD /run/secrets/GUI_PASSWORD
    load_secret DB_PASSWORD  /run/secrets/DB_PASSWORD
    load_secret GOOGLE_CLIENT_ID     /run/secrets/GOOGLE_CLIENT_ID
    load_secret GOOGLE_CLIENT_SECRET /run/secrets/GOOGLE_CLIENT_SECRET

    export HOME=/tmp
    exec setpriv --reuid="$PUID" --regid="$PGID" --clear-groups -- "$@"
fi

# Already started as a non-root user (e.g. `user:` set in compose): just run.
export HOME="${HOME:-/tmp}"
exec "$@"
