#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

PROFILE="${ATTACKZOO_PROFILE:-redux}"
CLAIM_OUT="claim3_http"
EXPERIMENT_DIR="experiments/${CLAIM_OUT}"
LINE="══════════════════════════════════════════════════════════════"

runs_done="0"
pcaps_valid="0"
features_valid="0"
datasets_valid="0"
reports_status="não"
result="FALHOU"

print_summary() {
    printf '%s\n' "${LINE}"
    printf 'Claim 3 — Evidências, features e datasets\n'
    printf 'Execuções concluídas: %s\n' "${runs_done}"
    printf 'PCAPs válidos       : %s\n' "${pcaps_valid}"
    printf 'Features Scapy      : %s\n' "${features_valid}"
    printf 'Datasets            : %s\n' "${datasets_valid}"
    printf 'Relatórios          : %s\n' "${reports_status}"
    printf 'Resultado esperado  : 2 runs / PCAPs / features / datasets / relatórios → %s\n' "${result}"
    printf '%s\n' "${LINE}"
}

fail() {
    printf '[ERROR] %s\n' "$*" >&2
    print_summary
    exit 1
}

require_image() {
    local image="$1"
    docker image inspect "${image}:latest" >/dev/null 2>&1 || \
        fail "Imagem ausente: ${image}:latest. Execute ./build.sh redux ou ./build.sh full antes deste claim."
}

collect_metrics() {
    if [[ -d "${EXPERIMENT_DIR}/dos_http_simple" ]]; then
        runs_done="$(find "${EXPERIMENT_DIR}/dos_http_simple" -mindepth 2 -maxdepth 2 -type d -name 'run*' | wc -l | tr -d ' ')"
        pcaps_valid="$(find "${EXPERIMENT_DIR}/dos_http_simple" -type f -name '*.pcap' -size +24c | wc -l | tr -d ' ')"
    fi

    features_valid="$(
        python3 - <<'PY'
from pathlib import Path

valid = 0
for path in Path("features").glob("scapy-claim3_http-dos_http_simple-*.csv"):
    try:
        rows = max(sum(1 for _ in path.open(encoding="utf-8")) - 1, 0)
    except OSError:
        rows = 0
    if rows > 0:
        valid += 1
print(valid)
PY
    )"

    datasets_valid="$(
        python3 - <<'PY'
from pathlib import Path

valid = 0
for path in Path("datasets").glob("unsupervised-claim3_http-dos_http_simple-*.csv"):
    try:
        rows = max(sum(1 for _ in path.open(encoding="utf-8")) - 1, 0)
    except OSError:
        rows = 0
    if rows > 0:
        valid += 1
print(valid)
PY
    )"

    if [[ -d "${EXPERIMENT_DIR}/reports" ]] && [[ "$(find "${EXPERIMENT_DIR}/reports" -type f | wc -l | tr -d ' ')" -gt 0 ]]; then
        reports_status="sim"
    fi
}

if [[ -z "${VIRTUAL_ENV:-}" && -f ".venv/bin/activate" ]]; then
    source ".venv/bin/activate"
fi

docker version >/dev/null 2>&1 || fail "Docker não está acessível para o usuário atual."
command -v tcpdump >/dev/null 2>&1 || fail "tcpdump não está disponível no PATH."

require_image "server-http-server"
require_image "attack-dos-http-simple"

mkdir -p ".tmp" "features" "datasets"
./servers.sh start "${PROFILE}" > ".tmp/claim3-servers.log" 2>&1 || \
    fail "Não foi possível iniciar os servidores. Consulte .tmp/claim3-servers.log."

for _ in $(seq 1 20); do
    if docker ps --format '{{.Names}}' | grep -qx "server-http-server" && \
       curl -fsS "http://127.0.0.1:8080/" >/dev/null 2>&1; then
        break
    fi
    sleep 1
done
curl -fsS "http://127.0.0.1:8080/" >/dev/null 2>&1 || \
    fail "server-http-server não ficou acessível em http://127.0.0.1:8080/."

HTTP_IP="$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' server-http-server)"
[[ -n "${HTTP_IP}" ]] || fail "Não foi possível resolver o IP do container server-http-server."

rm -rf "${EXPERIMENT_DIR}"
rm -f features/scapy-claim3_http-dos_http_simple-*.csv
rm -f datasets/unsupervised-claim3_http-dos_http_simple-*.csv

set +e
experiment_output="$(
    python3 attackzoo.py experiment \
        --attack-id dos_http_simple \
        --out "${CLAIM_OUT}" \
        --service "${CLAIM_OUT}" \
        --runs 1 \
        --levels L0,L1 \
        --warmup 2 \
        --attack 3 \
        --cooldown 2 \
        --interval 0.5 \
        --probe-timeout 1 \
        --probes http \
        --http-url "http://127.0.0.1:8080/" \
        --host "${HTTP_IP}" \
        --port 80 \
        --iface lo \
        --bpf "tcp port 8080" \
        --extract-features \
        --build-dataset \
        --tools-scapy \
        --attack-start-hook "python3 attackzoo.py run dos_http_simple --target {host} --port {port} --duration_s {duration_s} --count 500 --concurrency 4 --delay_ms 10" \
        --attack-stop-hook "python3 attackzoo.py stop dos_http_simple" 2>&1
)"
experiment_rc=$?
set -e
printf '%s\n' "${experiment_output}" > ".tmp/claim3-experiment.log"

collect_metrics

if [[ "${experiment_rc}" -ne 0 ]]; then
    fail "O experimento falhou. Consulte .tmp/claim3-experiment.log."
fi
if [[ "${runs_done}" != "2" ]]; then
    fail "Quantidade inesperada de runs concluídas: ${runs_done}."
fi
if [[ "${pcaps_valid}" != "2" ]]; then
    fail "Quantidade inesperada de PCAPs válidos: ${pcaps_valid}."
fi
if [[ "${features_valid}" != "2" ]]; then
    fail "Quantidade inesperada de arquivos de features válidos: ${features_valid}."
fi
if [[ "${datasets_valid}" != "2" ]]; then
    fail "Quantidade inesperada de datasets válidos: ${datasets_valid}."
fi
if [[ "${reports_status}" != "sim" ]]; then
    fail "Relatórios não foram gerados em ${EXPERIMENT_DIR}/reports."
fi

python3 attackzoo.py stop dos_http_simple >/dev/null 2>&1 || true

result="OK"
print_summary
