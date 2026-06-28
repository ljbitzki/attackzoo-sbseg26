#!/usr/bin/env bash
set -euo pipefail

ATTACK_ID="$2"
LEVEL="$1"
python attackzoo.py stop "$ATTACK_ID"
