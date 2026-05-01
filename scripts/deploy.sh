#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REMOTE_HOST="${REMOTE_HOST:-timberlea.cs.dal.ca}"
REMOTE_USER="${REMOTE_USER:-lahoud}"
REMOTE_PATH="${REMOTE_PATH:-public_html/}"
RSYNC_RSH="${RSYNC_RSH:-ssh}"

cd "$ROOT_DIR"

mkdir -p .home .cache .config .local/share .deno
export HOME="$ROOT_DIR/.home"
export XDG_CACHE_HOME="$ROOT_DIR/.cache"
export XDG_CONFIG_HOME="$ROOT_DIR/.config"
export XDG_DATA_HOME="$ROOT_DIR/.local/share"
export DENO_DIR="$ROOT_DIR/.deno"

quarto render

rsync -avz --delete -e "$RSYNC_RSH" _site/ "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}"

echo "Deployment complete: ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}"
