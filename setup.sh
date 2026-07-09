#!/usr/bin/env bash

PROFILE="${1}"

case "${PROFILE}" in
    full|redux|dependencies)
        ;;
    *)
        echo "Usage: $0 [full|redux|dependencies]"
        echo "Make sure you have ran at least ./setup.sh dependencies one time."
        exit 1
        ;;
esac

if [ "${1}" == "dependencies" ]; then
    echo "Installing required packages..."
    sudo apt update
    sudo DEBIAN_FRONTEND=noninteractive apt install -y tshark tcpdump python3-venv cmake wireshark redis ca-certificates curl git
    sudo DEBIAN_FRONTEND=noninteractive dpkg-reconfigure wireshark-common
    sudo chmod +x /usr/bin/dumpcap
    sudo setcap cap_net_raw,cap_net_admin=eip "$(command -v tcpdump)"

    echo "Installing tools..."
    chmod +x clients.sh docker-install.sh servers.sh build.sh environment.sh
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    git clone https://github.com/ahlashkari/NTLFlowLyzer.git
    cd NTLFlowLyzer || exit 1

    echo -e "\nsetuptools" >> requirements.txt
    pip install -r requirements.txt
    python3 setup.py install
    rm -rf .git/
    cd ../ || exit 1
    pip install -r requirements.txt
    echo -e "All dependencies satisfied.\nNow execute \e[92mnewgrp docker\e[0m to reload this shell session and then continue the procedure."
    exit 0
fi

if [ "${1}" == "redux" ] || [ "${1}" == "full" ]; then
    ./docker-install.sh "${PROFILE}"
fi