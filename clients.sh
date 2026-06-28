#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"
TARGET="${2:-all}"

RANDOM_IMAGE="client-random:latest"
SUPER_IMAGE="client-super:latest"
RANDOM_PREFIX="client-random-"
SUPER_PREFIX="client-super-"

SUPER_SERVICE="${CLIENT_SUPER_SERVICE:-web}"
SUPER_COUNT="${CLIENT_SUPER_COUNT:-10}"
SUPER_INTERVAL="${CLIENT_SUPER_INTERVAL:-1}"
SUPER_TOTAL="${CLIENT_SUPER_TOTAL:-15}"
SUPER_TARGET_IP="${CLIENT_SUPER_TARGET_IP:-}"
SUPER_TARGET_PORT="${CLIENT_SUPER_TARGET_PORT:-0}"

usage() {
    cat <<'EOF'
Usage:
  ./clients.sh start [all|random|super]
  ./clients.sh stop [all|random|super]
  ./clients.sh restart [all|random|super]

Aliases:
  iniciar=start, parar=stop, reiniciar=restart

client-super can be customized with:
  CLIENT_SUPER_SERVICE   default: web
  CLIENT_SUPER_TARGET_IP default: inferred from the matching server container
  CLIENT_SUPER_TARGET_PORT default: service default inside client-super
  CLIENT_SUPER_COUNT     default: 10
  CLIENT_SUPER_INTERVAL  default: 1
  CLIENT_SUPER_TOTAL     default: 15
EOF
}

normalize_action() {
    case "${1}" in
        start|iniciar) echo "start" ;;
        stop|parar) echo "stop" ;;
        restart|reiniciar) echo "restart" ;;
        *) return 1 ;;
    esac
}

normalize_target() {
    case "${1}" in
        all|"") echo "all" ;;
        random|client-random) echo "random" ;;
        super|client-super) echo "super" ;;
        *) return 1 ;;
    esac
}

require_image() {
    local image="$1"
    if [ "$(docker images -q "${image}" | wc -l)" -eq 0 ]; then
        echo "Missing client image: ${image}. Run cd docker && ./build-images.sh to rebuild the images."
        exit 1
    fi
}

container_ip() {
    docker container inspect "$1" --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
}

require_server() {
    local server="$1"
    if [ "$(docker ps --format '{{.Names}}' | grep -xc "${server}" || true)" -eq 0 ]; then
        echo "Required server is not running: ${server}. Run ./servers.sh start"
        exit 1
    fi
}

next_number_for_prefix() {
    local prefix="$1"
    local max_n=0
    local name suffix
    while read -r name; do
        [ -n "${name}" ] || continue
        suffix="${name#${prefix}}"
        if [[ "${suffix}" =~ ^[0-9]+$ ]] && [ "${suffix}" -gt "${max_n}" ]; then
            max_n="${suffix}"
        fi
    done < <(docker ps -a --format '{{.Names}}' | grep -E "^${prefix}[0-9]+$" || true)
    echo $((max_n + 1))
}

stop_random() {
    local clients=()
    mapfile -t clients < <(docker ps -a --format '{{.Names}}' | grep -E "^${RANDOM_PREFIX}[0-9]+$" || true)
    if [ "${#clients[@]}" -gt 0 ]; then
        docker rm -f "${clients[@]}"
    fi
}

stop_super() {
    local clients=()
    mapfile -t clients < <(docker ps -a --format '{{.Names}}' | grep -E "^${SUPER_PREFIX}[0-9]+$" || true)
    if [ "${#clients[@]}" -gt 0 ]; then
        docker rm -f "${clients[@]}"
    fi
}

start_random() {
    require_image "${RANDOM_IMAGE}"

    local required_servers=(
        server-http-server
        server-ssh-server
        server-smb-server
        server-mqtt-broker
        server-coap-server
        server-telnet-server
        server-ssl-heartbleed
    )
    local server
    for server in "${required_servers[@]}"; do
        require_server "${server}"
    done

    local web_ip ssh_ip smb_ip mqtt_ip coap_ip telnet_ip ssl_ip next name
    web_ip="$(container_ip server-http-server)"
    ssh_ip="$(container_ip server-ssh-server)"
    smb_ip="$(container_ip server-smb-server)"
    mqtt_ip="$(container_ip server-mqtt-broker)"
    coap_ip="$(container_ip server-coap-server)"
    telnet_ip="$(container_ip server-telnet-server)"
    ssl_ip="$(container_ip server-ssl-heartbleed)"

    next="$(next_number_for_prefix "${RANDOM_PREFIX}")"
    name="${RANDOM_PREFIX}${next}"
    docker run -d --rm --name "${name}" "${RANDOM_IMAGE}" \
        "${web_ip}" "${ssh_ip}" "${smb_ip}" "${mqtt_ip}" "${coap_ip}" "${telnet_ip}" "${ssl_ip}"
}

default_super_server_for_service() {
    case "${1}" in
        web|http|https) echo "server-http-server" ;;
        smb) echo "server-smb-server" ;;
        ssh) echo "server-ssh-server" ;;
        telnet) echo "server-telnet-server" ;;
        coap) echo "server-coap-server" ;;
        mqtt) echo "server-mqtt-broker" ;;
        zenoh|zenoh-pico) echo "server-zenoh-router" ;;
        xrce-dds|uxrce-dds) echo "server-xrce-dds-agent" ;;
        *) echo "" ;;
    esac
}

start_super() {
    require_image "${SUPER_IMAGE}"

    local service target_ip target_port server next name
    service="${SUPER_SERVICE,,}"
    target_ip="${SUPER_TARGET_IP}"
    target_port="${SUPER_TARGET_PORT}"

    if [ -z "${target_ip}" ]; then
        server="$(default_super_server_for_service "${service}")"
        if [ -z "${server}" ]; then
            echo "No default server mapping for client-super service '${service}'. Set CLIENT_SUPER_TARGET_IP."
            exit 1
        fi
        require_server "${server}"
        target_ip="$(container_ip "${server}")"
    fi

    next="$(next_number_for_prefix "${SUPER_PREFIX}")"
    name="${SUPER_PREFIX}${next}"
    docker run -d --rm --name "${name}" "${SUPER_IMAGE}" \
        "${service}" "${target_ip}" "${target_port}" "${SUPER_COUNT}" "${SUPER_INTERVAL}" "${SUPER_TOTAL}"
}

ACTION="$(normalize_action "${ACTION}")" || {
    usage
    exit 1
}

TARGET="$(normalize_target "${TARGET}")" || {
    usage
    exit 1
}

case "${ACTION}:${TARGET}" in
    stop:all)
        stop_random
        stop_super
        ;;
    stop:random)
        stop_random
        ;;
    stop:super)
        stop_super
        ;;
    start:all)
        start_random
        start_super
        ;;
    start:random)
        start_random
        ;;
    start:super)
        start_super
        ;;
    restart:all)
        stop_random
        stop_super
        start_random
        start_super
        ;;
    restart:random)
        stop_random
        start_random
        ;;
    restart:super)
        stop_super
        start_super
        ;;
esac
exit 0