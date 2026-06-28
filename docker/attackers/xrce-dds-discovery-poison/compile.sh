#!/usr/bin/env bash
mkdir -p bin
mkdir -p logs

C_ATTACKS=(
    "attack_discovery_poison"
)

DDS_CFLAGS="-Wall -Wextra -O2 -I/usr/local/include -I/usr/local/microcdr-2.0.2/include"
DDS_LIBS="-L/usr/local/lib -L/usr/local/microcdr-2.0.2/lib -lmicroxrcedds_client -lmicrocdr -lpthread"

SPECIAL_CFLAGS="-Wall -Wextra -O2"
SPECIAL_LIBS="-lpthread"

for attack in "${C_ATTACKS[@]}"; do
    if [ -f "${attack}.c" ]; then
        gcc ${attack}.c -o bin/$attack ${DDS_CFLAGS} ${DDS_LIBS}
        if [ $? -eq 0 ]; then
            chmod +x bin/$attack
        fi
    fi
done
