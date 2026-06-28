#!/usr/bin/env bash
set -euo pipefail

SERVICE="$1"
ATTACK_ID="$2"
LEVEL="$3"
HOST="$4"
PORT="$5"
DURATION="$6"

case "$LEVEL" in
  L0) exit 0 ;;
  L1) RATE=2000 ;;
  L2) RATE=7500 ;;
  L3) RATE=15000 ;;
  L4) RATE=50000 ;;
  *)  RATE=1000 ;;
esac

exec python attackzoo.py run "$ATTACK_ID" --target "$HOST" --target-port "$PORT" --rate "$RATE" --duration "$DURATION"
