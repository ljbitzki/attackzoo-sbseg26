#!/usr/bin/env bash

PROFILE="${1:-full}"
INSTALLED=0
MIN_DOCKER_VERSION="29.5"

case "${PROFILE}" in
    full|redux)
        ;;
    *)
        echo "Usage: $0 [full|redux]"
        exit 1
        ;;
esac

DOCKER_VERSION=$(docker version --format '{{.Server.Version}}' 2>/dev/null)
if [ -z "$DOCKER_VERSION" ]; then
    INSTALLED=0
fi

COMPARE() {
    if [[ $1 == $2 ]]; then
        return 0
    fi
    local IFS=.
    local i ver1=($1) ver2=($2)
    for ((i=${#ver1[@]}; i<${#ver2[@]}; i++)); do
        ver1[i]=0
    done
    for ((i=0; i<${#ver1[@]}; i++)); do
        if [[ -z ${ver2[i]} ]]; then
            ver2[i]=0
        fi
        if ((10#${ver1[i]} > 10#${ver2[i]})); then
            return 0
        fi
        if ((10#${ver1[i]} < 10#${ver2[i]})); then
            return 1
        fi
    done
    return 0
}

if COMPARE "${DOCKER_VERSION}" "${MIN_DOCKER_VERSION}"; then
    INSTALLED=1
else
    INSTALLED=0
fi

if [ "${INSTALLED}" -eq 0 ]; then
    echo "Docker not found. Installing..."
    sudo apt remove "$( dpkg --get-selections docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc | cut -f1 )"
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF
    sudo apt update
    sudo DEBIAN_FRONTEND=noninteractive apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    sudo usermod -aG docker "${USER}"
    if [ "${PROFILE}" = "redux" ]; then
        echo -e "Dependency installation complete.\nStarting the reduced image build with sudo for this first run."
        sudo ./build.sh "${PROFILE}"
        echo -e "Before future Docker commands, run \"\e[33mnewgrp docker\e[0m\" or log out and back in."
    else
        echo -e "Dependency installation complete.\nNow run \"\e[33mnewgrp docker\e[0m\" and then start the image build with \"\e[32m./build.sh ${PROFILE}\e[0m\""
    fi
else
    echo "Docker is installed and meets the minimum version."
    echo -e "Starting the image build with \"\e[32m./build.sh ${PROFILE}\e[0m\""
    ./build.sh "${PROFILE}"
fi
exit 0
