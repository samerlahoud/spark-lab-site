#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REMOTE_NAME="${REMOTE_NAME:-origin}"
BRANCH_NAME="${BRANCH_NAME:-$(git -C "$ROOT_DIR" branch --show-current)}"
COMMIT_MESSAGE="${COMMIT_MESSAGE:-Update rendered website}"

cd "$ROOT_DIR"

mkdir -p .home .cache .config .local/share .deno
export HOME="$ROOT_DIR/.home"
export XDG_CACHE_HOME="$ROOT_DIR/.cache"
export XDG_CONFIG_HOME="$ROOT_DIR/.config"
export XDG_DATA_HOME="$ROOT_DIR/.local/share"
export DENO_DIR="$ROOT_DIR/.deno"

quarto render

git add -A

if git diff --cached --quiet; then
  echo "No changes to commit after rendering."
  exit 0
fi

git commit -m "$COMMIT_MESSAGE"
git push "$REMOTE_NAME" "$BRANCH_NAME"

echo "Pushed rendered site to ${REMOTE_NAME}/${BRANCH_NAME}."
