#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

PROFILE="${ATTACKZOO_PROFILE:-redux}"
LINE="══════════════════════════════════════════════════════════════"

docker_status="indisponível"
server_status="não iniciado"
attack_started="não"
attack_finished="não"
result="FALHOU"

print_summary() {
    printf '%s\n' "${LINE}"
    printf 'Claim 2 — Execução contra servidor Docker\n'
    printf 'Docker disponível   : %s\n' "${docker_status}"
    printf 'Servidor HTTP       : %s\n' "${server_status}"
    printf 'Ataque iniciado     : %s\n' "${attack_started}"
    printf 'Ataque finalizado   : %s\n' "${attack_finished}"
    printf 'Resultado esperado  : Docker + HTTP ativo + ataque executado → %s\n' "${result}"
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

if [[ -z "${VIRTUAL_ENV:-}" && -f ".venv/bin/activate" ]]; then
    source ".venv/bin/activate"
fi

docker version >/dev/null 2>&1 || fail "Docker não está acessível para o usuário atual."
docker_status="sim"

require_image "server-http-server"
require_image "attack-dos-http-simple"

mkdir -p ".tmp"
./servers.sh start "${PROFILE}" > ".tmp/claim2-servers.log" 2>&1 || \
    fail "Não foi possível iniciar os servidores. Consulte .tmp/claim2-servers.log."

for _ in $(seq 1 20); do
    if docker ps --format '{{.Names}}' | grep -qx "server-http-server" && \
       curl -fsS "http://127.0.0.1:8080/" >/dev/null 2>&1; then
        server_status="Up"
        break
    fi
    sleep 1
done

[[ "${server_status}" == "Up" ]] || fail "server-http-server não ficou acessível em http://127.0.0.1:8080/."

HTTP_IP="$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' server-http-server)"
[[ -n "${HTTP_IP}" ]] || fail "Não foi possível resolver o IP do container server-http-server."

set +e
attack_output="$(
    python3 attackzoo.py run dos_http_simple \
        --target "${HTTP_IP}" \
        --port 80 \
        --duration 3 \
        --count 500 \
        --concurrency 4 \
        --delay_ms 50 2>&1
)"
attack_rc=$?
set -e
printf '%s\n' "${attack_output}" > ".tmp/claim2-attack.log"

if [[ "${attack_rc}" -ne 0 ]]; then
    fail "A execução do ataque falhou. Consulte .tmp/claim2-attack.log."
fi
if grep -q '\[OK\] Container started' ".tmp/claim2-attack.log"; then
    attack_started="sim"
else
    fail "A CLI não confirmou a criação do container de ataque."
fi

python3 attackzoo.py stop dos_http_simple >/dev/null 2>&1 || true
attack_finished="sim"

result="OK"
print_summary
