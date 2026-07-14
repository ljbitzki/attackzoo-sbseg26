#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

FIGSHARE_ARTICLE_ID="${FIGSHARE_ARTICLE_ID:-32900828}"
FIGSHARE_DOI="${FIGSHARE_DOI:-10.6084/m9.figshare.32900828}"
FIGSHARE_API="https://api.figshare.com/v2/articles/${FIGSHARE_ARTICLE_ID}"
DATA_DIR="${ATTACKZOO_FIGSHARE_DIR:-downloads/figshare}"
EXTRACT_DIR="${DATA_DIR}/extracted"
REPORT_NAME="${ATTACKZOO_FIGURES_REPORT:-paper_figures}"
REPORT_DIR="contrib/reports/${REPORT_NAME}"
REQUIRED_FREE_GB="${ATTACKZOO_FIGSHARE_MIN_FREE_GB:-260}"
LINE="══════════════════════════════════════════════════════════════"

archive_name=""
archive_size="0"
archive_md5=""
download_url=""
campaign_dir=""
attacks_done="0"
pcaps_done="0"
pcaps_ok="0"
figures_done="0"
traffic_gib="0.0"
result="FAILED"

print_summary() {
    printf '%s\n' "${LINE}"
    printf 'Claim 3 — Full paper figure reproduction\n'
    printf 'DOI Figshare        : %s\n' "${FIGSHARE_DOI}"
    printf 'Compressed archive  : %s\n' "${archive_name:-not resolved}"
    printf 'Attacks             : %s\n' "${attacks_done}"
    printf 'PCAPs processed     : %s/%s\n' "${pcaps_ok}" "${pcaps_done}"
    printf 'Traffic counted     : %s GiB\n' "${traffic_gib}"
    printf 'Figures generated   : %s\n' "${figures_done}"
    printf 'Report              : %s\n' "${REPORT_DIR}"
    printf 'Expected result     : 60 attacks / 1200 PCAPs / 8 figures / manifest OK → %s\n' "${result}"
    printf '%s\n' "${LINE}"
}

fail() {
    printf '[ERROR] %s\n' "$*" >&2
    print_summary
    exit 1
}

require_command() {
    command -v "$1" >/dev/null 2>&1 || fail "Required command is missing: $1"
}

free_gib() {
    local path="$1"
    df -Pk "${path}" | awk 'NR == 2 { printf "%.0f", $4 / 1024 / 1024 }'
}

check_free_space() {
    mkdir -p "${DATA_DIR}"
    local available_gib
    available_gib="$(free_gib "${DATA_DIR}")"
    if (( available_gib < REQUIRED_FREE_GB )); then
        fail "Not enough free space under ${DATA_DIR}: ${available_gib} GiB available; ${REQUIRED_FREE_GB} GiB recommended."
    fi
}

resolve_figshare_metadata() {
    mapfile -t metadata < <(python3 - "${FIGSHARE_API}" <<'PY'
import json
import sys
import urllib.request

url = sys.argv[1]
with urllib.request.urlopen(url, timeout=60) as response:
    payload = json.load(response)

files = payload.get("files") or []
if not files:
    raise SystemExit("Figshare article has no files")

file_info = files[0]
print(file_info.get("name", ""))
print(file_info.get("size", 0))
print(file_info.get("supplied_md5") or file_info.get("computed_md5") or "")
print(file_info.get("download_url", ""))
PY
    )
    archive_name="${metadata[0]}"
    archive_size="${metadata[1]}"
    archive_md5="${metadata[2]}"
    download_url="${metadata[3]}"

    [[ -n "${archive_name}" ]] || fail "Figshare file name was not resolved."
    [[ -n "${download_url}" ]] || fail "Figshare download URL was not resolved."
}

download_archive() {
    local archive_path="${DATA_DIR}/${archive_name}"
    if [[ "${ATTACKZOO_CONFIRM_LARGE_DOWNLOAD:-0}" != "1" && ! -f "${archive_path}" ]]; then
        fail "This step downloads 16.9 GB and may unpack more than 225 GB. Run it with ATTACKZOO_CONFIRM_LARGE_DOWNLOAD=1."
    fi

    check_free_space

    if [[ -f "${archive_path}" ]] && [[ "$(stat -c '%s' "${archive_path}")" == "${archive_size}" ]]; then
        printf '[INFO] Reusing existing archive: %s\n' "${archive_path}"
    else
        printf '[INFO] Downloading %s from Figshare...\n' "${archive_name}"
        curl -L --fail --continue-at - --output "${archive_path}" "${download_url}"
    fi

    if [[ -n "${archive_md5}" ]]; then
        printf '%s  %s\n' "${archive_md5}" "${archive_path}" | md5sum -c - >/dev/null || \
            fail "MD5 verification failed for ${archive_path}."
    fi
}

find_campaign_dir() {
    campaign_dir="$(
        find "${EXTRACT_DIR}" -type d -name "60att_5runs_l0l1l2l3" -print -quit 2>/dev/null
    )"
}

extract_archive_if_needed() {
    local archive_path="${DATA_DIR}/${archive_name}"
    mkdir -p "${EXTRACT_DIR}"
    find_campaign_dir

    if [[ -n "${campaign_dir}" ]] && [[ "$(find "${campaign_dir}" -type f -name '*.pcap' | wc -l | tr -d ' ')" == "1200" ]]; then
        printf '[INFO] Reusing existing extracted campaign: %s\n' "${campaign_dir}"
        return
    fi

    check_free_space
    printf '[INFO] Extracting %s under %s...\n' "${archive_path}" "${EXTRACT_DIR}"
    tar -xzf "${archive_path}" -C "${EXTRACT_DIR}"
    find_campaign_dir
    [[ -n "${campaign_dir}" ]] || fail "Directory 60att_5runs_l0l1l2l3 was not found after extraction."
}

prepare_campaign() {
    mkdir -p "${EXTRACT_DIR}"
    find_campaign_dir
    if [[ -n "${campaign_dir}" ]] && [[ "$(find "${campaign_dir}" -type f -name '*.pcap' | wc -l | tr -d ' ')" == "1200" ]]; then
        printf '[INFO] Reusing existing extracted campaign: %s\n' "${campaign_dir}"
        return
    fi

    download_archive
    extract_archive_if_needed
}

run_statistics() {
    if [[ -z "${VIRTUAL_ENV:-}" && -f ".venv/bin/activate" ]]; then
        source ".venv/bin/activate"
    fi

    python3 contrib/scripts/campaign_traffic_stats.py \
        --campaign-dir "${campaign_dir}" \
        --reports-root "contrib/reports" \
        --campaign-name "${REPORT_NAME}" \
        --source auto \
        --plots all \
        --progress-interval 25
}

collect_metrics() {
    local manifest="${REPORT_DIR}/manifest.json"
    [[ -f "${manifest}" ]] || fail "Manifest not found: ${manifest}"

    attacks_done="$(find "${campaign_dir}" -mindepth 1 -maxdepth 1 -type d ! -name '_campaign' | wc -l | tr -d ' ')"
    mapfile -t metrics < <(python3 - "${manifest}" <<'PY'
import json
import sys
from pathlib import Path

manifest = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
print(manifest.get("processed_pcap_count", 0))
print(manifest.get("ok_pcap_count", 0))
print(len(manifest.get("plot_outputs") or {}))
print(f"{float(manifest.get('byte_total') or 0) / (1024 ** 3):.1f}")
PY
    )
    pcaps_done="${metrics[0]}"
    pcaps_ok="${metrics[1]}"
    figures_done="${metrics[2]}"
    traffic_gib="${metrics[3]}"
}

require_command curl
require_command tar
require_command md5sum

resolve_figshare_metadata
prepare_campaign
if ! run_statistics; then
    fail "Statistics/figure generation failed. Check the output from contrib/scripts/campaign_traffic_stats.py."
fi
collect_metrics

if [[ "${attacks_done}" != "60" ]]; then
    fail "Unexpected attack count in the dataset: ${attacks_done}."
fi
if [[ "${pcaps_done}" != "1200" || "${pcaps_ok}" != "1200" ]]; then
    fail "Unexpected processed PCAP count: ${pcaps_ok}/${pcaps_done}."
fi
if [[ "${figures_done}" != "8" ]]; then
    fail "Unexpected generated figure count: ${figures_done}."
fi

result="OK"
print_summary
