#!/usr/bin/env bash
set -euo pipefail

DURATION_S="${DURATION_S:-0}"
ACTIVE_S="${ACTIVE_S:-5}"
NICE_LEVEL="${NICE_LEVEL:-10}"
HOLD_GRACE_S="${HOLD_GRACE_S:-5}"

if [ "${DURATION_S}" -gt 0 ] && [ "${ACTIVE_S}" -gt "${DURATION_S}" ]; then
  ACTIVE_S="${DURATION_S}"
fi
if [ "${ACTIVE_S}" -le 0 ]; then
  ACTIVE_S=5
fi

started_at="${SECONDS}"

set +e
timeout "${ACTIVE_S}s" nice -n "${NICE_LEVEL}" /usr/local/bin/flood_mld6 eth0
status="$?"
set -e

hold_until_duration() {
  if [ "${DURATION_S}" -gt 0 ]; then
    elapsed=$((SECONDS - started_at))
    remaining=$((DURATION_S + HOLD_GRACE_S - elapsed))
    if [ "${remaining}" -gt 0 ]; then
      sleep "${remaining}"
    fi
  fi
}

if [ "${status}" -eq 0 ] || [ "${status}" -eq 124 ] || [ "${status}" -eq 143 ]; then
  hold_until_duration
  exit 0
fi
exit "${status}"
