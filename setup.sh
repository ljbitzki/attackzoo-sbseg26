#!/usr/bin/env bash

echo "Installing required packages..."
sudo apt update
sudo DEBIAN_FRONTEND=noninteractive apt install -y tshark tcpdump python3-venv cmake wireshark redis ca-certificates curl
sudo DEBIAN_FRONTEND=noninteractive dpkg-reconfigure wireshark-common
sudo chmod +x /usr/bin/dumpcap
sudo setcap cap_net_raw,cap_net_admin=eip "$(command -v tcpdump)"

echo "Installing tools..."
chmod +x clients.sh docker-install.sh servers.sh build.sh environ.sh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
git clone https://github.com/ahlashkari/NTLFlowLyzer.git
cd NTLFlowLyzer

echo -e "\nsetuptools" >> requirements.txt
pip install -r requirements.txt
python3 setup.py install
rm -rf .git/
cd ../
pip install -r requirements.txt
./docker-install.sh
