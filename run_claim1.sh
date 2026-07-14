#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

CATALOG_JSON=".tmp/claim1-catalog.json"
LINE="══════════════════════════════════════════════════════════════"

attacks="0"
categories="0"
json_fields="não"
result="FALHOU"

print_summary() {
    printf '%s\n' "${LINE}"
    printf 'Claim 1 — Catálogo de ataques\n'
    printf 'Ataques no catálogo : %s\n' "${attacks}"
    printf 'Categorias          : %s\n' "${categories}"
    printf 'Campos JSON         : %s\n' "${json_fields}"
    printf 'Resultado esperado  : 60 ataques / 7 categorias / campos JSON → %s\n' "${result}"
    printf '%s\n' "${LINE}"
}

fail() {
    printf '[ERROR] %s\n' "$*" >&2
    print_summary
    exit 1
}

if [[ -z "${VIRTUAL_ENV:-}" && -f ".venv/bin/activate" ]]; then
    source ".venv/bin/activate"
fi

mkdir -p ".tmp"
python3 attackzoo.py list --json > "${CATALOG_JSON}" || fail "Não foi possível executar: python3 attackzoo.py list --json"

mapfile -t metrics < <(python3 - "${CATALOG_JSON}" <<'PY'
import json
import sys
from pathlib import Path

payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
required = {"id", "name", "image", "container", "params", "mitre", "max_runtime_s"}

missing = []
for items in payload.values():
    for item in items:
        missing_keys = sorted(required - set(item))
        if missing_keys:
            missing.append(f"{item.get('id', '<unknown>')}:{','.join(missing_keys)}")

print(sum(len(items) for items in payload.values()))
print(len(payload))
print("sim" if not missing else "não")
print("; ".join(missing[:5]))
PY
)

attacks="${metrics[0]}"
categories="${metrics[1]}"
json_fields="${metrics[2]}"
missing_fields="${metrics[3]:-}"

if [[ "${attacks}" != "60" ]]; then
    fail "Quantidade de ataques inesperada: ${attacks}"
fi
if [[ "${categories}" != "7" ]]; then
    fail "Quantidade de categorias inesperada: ${categories}"
fi
if [[ "${json_fields}" != "sim" ]]; then
    fail "Campos obrigatórios ausentes no JSON: ${missing_fields}"
fi

result="OK"
print_summary
