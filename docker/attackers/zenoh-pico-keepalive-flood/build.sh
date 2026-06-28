#!/usr/bin/env bash
attacks=(
    "attack_dos_keepalive_flood:attack_keepalive"
)

for attack in "${attacks[@]}"; do
    IFS=':' read -r source binary <<< "${attack}"
    gcc -o "${binary}" "${source}.c" -pthread -O2 2>/dev/null
    chmod +x "${binary}"
done