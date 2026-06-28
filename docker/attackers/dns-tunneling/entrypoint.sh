#!/usr/bin/env bash
DOMAIN=$( cat /dev/urandom | tr -dc "0-9a-fA-F" | fold -w 8 | head -n 1 )
DNS_SERVERS=("1.1.1.1" "1.0.0.1" "8.8.8.8" "8.8.4.4" "9.9.9.9" "149.112.112.112")
LENGHT=${#DNS_SERVERS[@]}
DOMAIN=$( cat /dev/urandom | tr -dc "0-9a-fA-F" | fold -w 8 | head -n 1 )
COUNT="${COUNT:-200}"
DELAY_MS="${DELAY_MS:-200}"
DURATION_S="${DURATION_S:-0}"
PAYLOAD_SIZE="${PAYLOAD_SIZE:-0}"

function delay() {
  if [ "${DELAY_MS}" -gt 0 ]; then
    sleep "$(printf "%d.%03d" $((DELAY_MS / 1000)) $((DELAY_MS % 1000)))"
  fi
}

function DNS_RESOLVE() {
  DNS="${DNS_SERVERS[$((RANDOM % LENGHT))]}"
  if [ "${PAYLOAD_SIZE}" -gt 0 ]; then
    RANGE="${PAYLOAD_SIZE}"
  else
    RANGE=$(( 12 + $RANDOM % 50 ))
  fi
  SUBDOMAIN=$( cat /dev/urandom | tr -dc "0-9a-fA-F" | fold -w "${RANGE}" | head -n 1 )
  dig @$DNS +time=1 +tries=1 +short "${SUBDOMAIN}.${DOMAIN}.com" 2>&1 | head -1
}
started_at="${SECONDS}"
for i in $( seq 1 "${COUNT}" ); do
  if [ "${DURATION_S}" -gt 0 ] && [ $((SECONDS - started_at)) -ge "${DURATION_S}" ]; then
    break
  fi
  DNS_RESOLVE &
  delay
done
