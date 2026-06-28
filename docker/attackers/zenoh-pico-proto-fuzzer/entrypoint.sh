#!/usr/bin/env bash
if [ "${#}" -eq 2 ]; then
	TARGET="${1}"
    PORT="${2}"
    COUNT="${COUNT:-1000}"
    DURATION_S="${DURATION_S:-0}"
    if [ "${DURATION_S}" -gt 0 ]; then
        timeout "${DURATION_S}" /usr/local/bin/proto_fuzzer "${TARGET}" "${PORT}" "${COUNT}"
    else
        /usr/local/bin/proto_fuzzer "${TARGET}" "${PORT}" "${COUNT}"
    fi
fi
