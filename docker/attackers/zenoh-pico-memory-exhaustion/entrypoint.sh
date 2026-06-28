#!/usr/bin/env bash
if [ "${#}" -eq 2 ]; then
	TARGET="${1}"
    PORT="${2}"
    THREADS="${THREADS:-4}"
    DURATION_S="${DURATION_S:-10}"
    timeout --preserve-status -s INT "${DURATION_S}" /usr/local/bin/attack_memory "${TARGET}" "${PORT}" "${THREADS}"
fi
