#!/usr/bin/env bash

echo "Building containers..."
cd docker/ || exit 1
chmod +x build-images.sh
./build-images.sh

echo "Containers created..."
cd ../
source .venv/bin/activate
exit 0