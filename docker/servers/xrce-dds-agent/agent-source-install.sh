#!/usr/bin/env bash
cd /tmp || exit 1
git clone https://github.com/eProsima/Micro-XRCE-DDS-Agent.git
cd /tmp/Micro-XRCE-DDS-Agent || exit 1
docker build -t server-xrce-dds-agent -f Dockerfile .
cd /tmp/ || exit 1
rm -rf "/tmp/Micro-XRCE-DDS-Agent"