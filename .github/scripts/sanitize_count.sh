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

# Cuenta resultados SARIF usando security-severity o niveles SARIF/Semgrep.
# Semgrep suele emitir ERROR/WARNING/NOTE en result.level.
count_sarif_by_severity() {
  local band="${1:-all}"
  local file="${2:-semgrep-results.sarif}"

  python3 - "$band" "$file" <<'PY'
import json
import sys

band = sys.argv[1]
path = sys.argv[2]

try:
    with open(path, encoding="utf-8") as stream:
        data = json.load(stream)
except (OSError, json.JSONDecodeError):
    print(0)
    raise SystemExit(0)

def score(result):
    properties = result.get("properties") or {}
    raw_score = properties.get("security-severity")
    try:
        if raw_score is not None:
            return float(raw_score)
    except (TypeError, ValueError):
        pass

    label = str(
        properties.get("issue_severity")
        or result.get("level")
        or "medium"
    ).strip().lower()

    if label in {"critical", "crit"}:
        return 10.0
    if label in {"high", "error"}:
        return 8.0
    if label in {"medium", "warning"}:
        return 5.0
    if label in {"low", "note", "info"}:
        return 2.0
    return 5.0

results = [
    result
    for run in data.get("runs", [])
    for result in run.get("results", [])
]

count = 0
for result in results:
    value = score(result)
    matches = (
        band == "all"
        or (band == "critical" and value >= 9)
        or (band == "high" and 7 <= value < 9)
        or (band == "medium" and 4 <= value < 7)
        or (band == "low" and value < 4)
    )
    if matches:
        count += 1

print(count)
PY
}