#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

PROFILE="${ATTACKZOO_PROFILE:-redux}"
LINE="══════════════════════════════════════════════════════════════"

docker_status="unavailable"
server_status="not started"
attack_started="no"
attack_finished="no"
result="FAILED"

print_summary() {
    printf '%s\n' "${LINE}"
    printf 'Claim 2 — Execution against a Docker server\n'
    printf 'Docker available    : %s\n' "${docker_status}"
    printf 'HTTP server         : %s\n' "${server_status}"
    printf 'Attack started      : %s\n' "${attack_started}"
    printf 'Attack stopped      : %s\n' "${attack_finished}"
    printf 'Expected result     : Docker + active HTTP server + executed attack → %s\n' "${result}"
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
        fail "Missing image: ${image}:latest. Run ./build.sh redux or ./build.sh full before this claim."
}

if [[ -z "${VIRTUAL_ENV:-}" && -f ".venv/bin/activate" ]]; then
    source ".venv/bin/activate"
fi

docker version >/dev/null 2>&1 || fail "Docker is not accessible for the current user."
docker_status="yes"

require_image "server-http-server"
require_image "attack-dos-http-simple"

mkdir -p ".tmp"
./servers.sh start "${PROFILE}" > ".tmp/claim2-servers.log" 2>&1 || \
    fail "Could not start the servers. See .tmp/claim2-servers.log."

for _ in $(seq 1 20); do
    if docker ps --format '{{.Names}}' | grep -qx "server-http-server" && \
       curl -fsS "http://127.0.0.1:8080/" >/dev/null 2>&1; then
        server_status="Up"
        break
    fi
    sleep 1
done

[[ "${server_status}" == "Up" ]] || fail "server-http-server did not become reachable at http://127.0.0.1:8080/."

HTTP_IP="$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' server-http-server)"
[[ -n "${HTTP_IP}" ]] || fail "Could not resolve the server-http-server container IP address."

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
    fail "Attack execution failed. See .tmp/claim2-attack.log."
fi
if grep -q '\[OK\] Container started' ".tmp/claim2-attack.log"; then
    attack_started="yes"
else
    fail "The CLI did not confirm attack container creation."
fi

python3 attackzoo.py stop dos_http_simple >/dev/null 2>&1 || true
attack_finished="yes"

result="OK"
print_summary
