#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

REPORT_NAME="${ATTACKZOO_FIGURES_REPORT:-claim3_figshare_dataset}"

printf '[INFO] The Figshare artifact contains generated dataset CSVs, not raw PCAP captures.\n'
printf '[INFO] Delegating to run_claim3.sh to validate the published dataset inventory.\n'

ATTACKZOO_CLAIM3_MODE=figshare ATTACKZOO_CLAIM3_REPORT="${REPORT_NAME}" bash run_claim3.sh
