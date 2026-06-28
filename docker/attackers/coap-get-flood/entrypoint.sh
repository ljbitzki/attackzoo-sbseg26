#!/bin/sh
set -eu

if [ "${#}" -ne 2 ]; then
    echo "Usage: $0 <target_ip_or_fqdn> <target_port>" >&2
    exit 2
fi

TARGET="${1}"
PORT="${2}"

COUNT="${COUNT:-1000}"
DELAY_MS="${DELAY_MS:-0}"
DURATION_S="${DURATION_S:-0}"
REQUEST_TIMEOUT_S="${REQUEST_TIMEOUT_S:-2.0}"
export COUNT DELAY_MS DURATION_S REQUEST_TIMEOUT_S

exec python3 /tmp/client.py "${TARGET}" "${PORT}"
