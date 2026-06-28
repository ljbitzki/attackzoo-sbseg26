#!/bin/sh
if [ "${#}" -eq 2 ]; then
	TARGET="${1}"
    PORT="${2}"
    set -e
    exec python3 /ralmqtt/ralmqtt.py -m bruteforce -a "${TARGET}" -p "${PORT}" -w /ralmqtt/passwords.txt
fi