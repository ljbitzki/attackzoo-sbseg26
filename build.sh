#!/usr/bin/env bash
set -euo pipefail

PROFILE="${1}"

case "${PROFILE}" in
    full|redux)
        ;;
    *)
        echo "Usage: $0 [full|redux]"
        exit 1
        ;;
esac

echo "Building containers..."
cd docker/ || exit 1
chmod +x build-images.sh
./build-images.sh "${PROFILE}"

echo "Containers created..."
cd ../
source .venv/bin/activate
exit 0
