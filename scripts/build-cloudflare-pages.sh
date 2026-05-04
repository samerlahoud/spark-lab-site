#!/usr/bin/env bash
set -euo pipefail

QUARTO_URL="${QUARTO_URL:-https://quarto.org/download/latest/quarto-linux-amd64.deb}"
QUARTO_DIR="${PWD}/.cloudflare/quarto"
QUARTO_DEB="${PWD}/.cloudflare/quarto-linux-amd64.deb"

mkdir -p .home .cache .config .local/share .deno
export HOME="${PWD}/.home"
export XDG_CACHE_HOME="${PWD}/.cache"
export XDG_CONFIG_HOME="${PWD}/.config"
export XDG_DATA_HOME="${PWD}/.local/share"
export DENO_DIR="${PWD}/.deno"

if ! command -v quarto >/dev/null 2>&1; then
  mkdir -p "${PWD}/.cloudflare"
  curl -L "${QUARTO_URL}" -o "${QUARTO_DEB}"
  rm -rf "${QUARTO_DIR}"
  mkdir -p "${QUARTO_DIR}"
  dpkg -x "${QUARTO_DEB}" "${QUARTO_DIR}"
  export PATH="${QUARTO_DIR}/opt/quarto/bin:${PATH}"
fi

python3 -m pip install --user -r requirements.txt
export PATH="${HOME}/.local/bin:${PATH}"

quarto render
