#!/usr/bin/env bash
# Normaliza salidas de jq/wc a un entero de una sola linea.
# Evita errores "integer expression expected" y fallos al escribir en GITHUB_ENV.
sanitize_count() {
  local value="${1:-0}"
  value=$(printf '%s\n' "$value" | head -1 | tr -d '[:space:]')
  if [[ "$value" =~ ^[0-9]+$ ]]; then
    echo "$value"
  else
    echo "0"
  fi
}
