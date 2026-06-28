#!/usr/bin/env bash
attacks=(
    "attack_memory_exhaustion:attack_memory"
)

for attack in "${attacks[@]}"; do
    IFS=':' read -r source binary <<< "${attack}"
    gcc -o "${binary}" "${source}.c" -pthread -O2 2>/dev/null
    chmod +x "${binary}"
done